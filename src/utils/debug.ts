/**
 * Debug Utilities for Marketing Portfolio
 *
 * Centralized logging and debugging utilities for the Astro project.
 * Provides structured logging, performance timing, and error tracking.
 */

// Log Levels (ordered by priority)
export const LOG_LEVELS = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3,
  TRACE: 4,
} as const;

export type LogLevel = (typeof LOG_LEVELS)[keyof typeof LOG_LEVELS];

// Current log level (can be set via environment variable)
const CURRENT_LOG_LEVEL = parseInt(process.env.LOG_LEVEL || String(LOG_LEVELS.INFO), 10);

// Service identifier for all logs
const SERVICE_NAME = 'marketing-portfolio';

/**
 * Check if a log level should be output
 */
const shouldLog = (level: LogLevel): boolean => {
  return level <= CURRENT_LOG_LEVEL;
};

/**
 * Create a structured log entry
 */
interface StructuredLog {
  timestamp: string;
  level: string;
  message: string;
  context?: Record<string, unknown>;
  service: string;
  requestId?: string;
  performance?: {
    duration: number;
    unit: string;
  };
}

const createStructuredLog = (
  level: string,
  message: string,
  context?: Record<string, unknown>,
  requestId?: string
): StructuredLog => {
  return {
    timestamp: new Date().toISOString(),
    level,
    message,
    context,
    service: SERVICE_NAME,
    requestId,
  };
};

/**
 * Format error for logging
 */
interface LoggedError {
  message: string;
  stack?: string;
  name: string;
  code?: string;
}

const formatError = (error: unknown): LoggedError => {
  if (error instanceof Error) {
    return {
      message: error.message,
      stack: error.stack,
      name: error.name,
      // @ts-expect-error - Node.js error code property
      code: error.code,
    };
  }

  return {
    message: String(error),
    name: 'UnknownError',
  };
};

/**
 * Generate a unique request ID for tracing
 */
export const generateRequestId = (): string => {
  return `req_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
};

// Console logging functions (can be replaced with actual logger in production)
const logToConsole = (log: StructuredLog): void => {
  const { level, message, context, requestId } = log;
  const prefix = requestId ? `[${requestId}]` : '';
  const contextStr = context ? ` ${JSON.stringify(context)}` : '';

  switch (level) {
    case 'error':
      console.error(`${prefix}[ERROR] ${message}${contextStr}`);
      break;
    case 'warn':
      console.warn(`${prefix}[WARN] ${message}${contextStr}`);
      break;
    case 'debug':
      console.debug(`${prefix}[DEBUG] ${message}${contextStr}`);
      break;
    case 'trace':
      console.trace(`${prefix}[TRACE] ${message}${contextStr}`);
      break;
    default:
      console.log(`${prefix}[INFO] ${message}${contextStr}`);
  }
};

/**
 * Logger instance with methods for each log level
 */
export const logger = {
  error: (message: string, context?: Record<string, unknown>, requestId?: string): void => {
    if (shouldLog(LOG_LEVELS.ERROR)) {
      const errorContext = context
        ? { ...context, error: formatError(context.error as unknown) }
        : undefined;
      logToConsole(createStructuredLog('error', message, errorContext, requestId));
    }
  },

  warn: (message: string, context?: Record<string, unknown>, requestId?: string): void => {
    if (shouldLog(LOG_LEVELS.WARN)) {
      logToConsole(createStructuredLog('warn', message, context, requestId));
    }
  },

  info: (message: string, context?: Record<string, unknown>, requestId?: string): void => {
    if (shouldLog(LOG_LEVELS.INFO)) {
      logToConsole(createStructuredLog('info', message, context, requestId));
    }
  },

  debug: (message: string, context?: Record<string, unknown>, requestId?: string): void => {
    if (shouldLog(LOG_LEVELS.DEBUG)) {
      logToConsole(createStructuredLog('debug', message, context, requestId));
    }
  },

  trace: (message: string, context?: Record<string, unknown>, requestId?: string): void => {
    if (shouldLog(LOG_LEVELS.TRACE)) {
      logToConsole(createStructuredLog('trace', message, context, requestId));
    }
  },
};

/**
 * Performance timer utility
 */
export class PerformanceTimer {
  private startTime: number;
  private label: string;

  constructor(label: string = 'timer') {
    this.startTime = Date.now();
    this.label = label;
  }

  /**
   * Stop the timer and return duration in milliseconds
   */
  stop(): number {
    const duration = Date.now() - this.startTime;
    logger.debug(`Timer '${this.label}' completed`, { duration: `${duration}ms` });
    return duration;
  }

  /**
   * Get current elapsed time without stopping
   */
  getElapsed(): number {
    return Date.now() - this.startTime;
  }

  /**
   * Format duration for human readability
   */
  static formatDuration(ms: number): string {
    if (ms < 1000) {
      return `${Math.round(ms)}ms`;
    }
    if (ms < 60000) {
      return `${(ms / 1000).toFixed(2)}s`;
    }
    return `${(ms / 60000).toFixed(2)}m`;
  }
}

/**
 * Assert utility for development debugging
 */
export function assert(
  condition: unknown,
  message: string,
  context?: Record<string, unknown>
): asserts condition {
  if (!condition) {
    logger.error(`Assertion failed: ${message}`, context);
    throw new Error(`Assertion failed: ${message}`);
  }
}

/**
 * Debounce utility for function calls
 * @param fn - Function to debounce
 * @param delay - Delay in milliseconds
 * @returns Debounced function
 */
export function debounce(fn: (...args: unknown[]) => void, delay: number): typeof fn {
  let timeoutId: ReturnType<typeof setTimeout>;
  return function (this: unknown, ...args: unknown[]) {
    void this;
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  } as typeof fn;
}

/**
 * Throttle utility for function calls
 * @param fn - Function to throttle
 * @param limit - Time limit in milliseconds
 * @returns Throttled function
 */
export function throttle(fn: (...args: unknown[]) => void, limit: number): typeof fn {
  let inThrottle = false;
  return function (this: unknown, ...args: unknown[]) {
    void this;
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  } as typeof fn;
}

/**
 * Safe async wrapper with error logging
 */
export async function safeAsync<T>(
  fn: () => Promise<T>,
  context?: Record<string, unknown>
): Promise<{ success: true; data: T } | { success: false; error: string }> {
  try {
    const data = await fn();
    return { success: true, data };
  } catch (error) {
    logger.error('Async operation failed', { ...context, error: formatError(error) });
    return { success: false, error: formatError(error).message };
  }
}

/**
 * Environment helpers for debugging
 */
export const env = {
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isTest: process.env.NODE_ENV === 'test',
  isDebugEnabled: process.env.DEBUG === 'true',

  get: (key: string, defaultValue?: string): string | undefined => {
    return process.env[key] || defaultValue;
  },
};

export default {
  logger,
  LOG_LEVELS,
  generateRequestId,
  PerformanceTimer,
  assert,
  debounce,
  throttle,
  safeAsync,
  env,
};

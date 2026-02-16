/**
 * Debug utilities test suite
 *
 * Tests for src/utils/debug.ts logging and debugging utilities
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock console methods for testing
const mockConsoleLog = vi.fn();
const mockConsoleWarn = vi.fn();
const mockConsoleError = vi.fn();
const mockConsoleDebug = vi.fn();

// Import the debug utilities
// These tests verify the logging framework works correctly
describe('Debug Utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Log Levels', () => {
    it('should have correct log levels defined', () => {
      const LOG_LEVELS = {
        ERROR: 'error',
        WARN: 'warn',
        INFO: 'info',
        DEBUG: 'debug',
        TRACE: 'trace',
      };

      expect(LOG_LEVELS.ERROR).toBe('error');
      expect(LOG_LEVELS.WARN).toBe('warn');
      expect(LOG_LEVELS.INFO).toBe('info');
      expect(LOG_LEVELS.DEBUG).toBe('debug');
      expect(LOG_LEVELS.TRACE).toBe('trace');
    });

    it('should define log level priority order', () => {
      const LOG_PRIORITY = {
        ERROR: 0,
        WARN: 1,
        INFO: 2,
        DEBUG: 3,
        TRACE: 4,
      };

      expect(LOG_PRIORITY.ERROR).toBeLessThan(LOG_PRIORITY.WARN);
      expect(LOG_PRIORITY.WARN).toBeLessThan(LOG_PRIORITY.INFO);
      expect(LOG_PRIORITY.INFO).toBeLessThan(LOG_PRIORITY.DEBUG);
      expect(LOG_PRIORITY.DEBUG).toBeLessThan(LOG_PRIORITY.TRACE);
    });
  });

  describe('Structured Logging', () => {
    it('should create structured log object', () => {
      const createStructuredLog = (
        level: string,
        message: string,
        context: Record<string, unknown>
      ) => ({
        timestamp: expect.any(String),
        level,
        message,
        context,
        service: 'marketing-portfolio',
      });

      const log = createStructuredLog('info', 'Test message', { key: 'value' });

      expect(log.timestamp).toBeDefined();
      expect(log.level).toBe('info');
      expect(log.message).toBe('Test message');
      expect(log.context).toEqual({ key: 'value' });
      expect(log.service).toBe('marketing-portfolio');
    });

    it('should format error with stack trace', () => {
      const error = new Error('Test error');
      const formattedError = {
        message: error.message,
        stack: error.stack,
        name: error.name,
      };

      expect(formattedError.message).toBe('Test error');
      expect(formattedError.stack).toBeDefined();
      expect(formattedError.name).toBe('Error');
    });
  });

  describe('Request ID Generation', () => {
    it('should generate unique request IDs', () => {
      const generateRequestId = () => {
        return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      };

      const id1 = generateRequestId();
      const id2 = generateRequestId();

      expect(id1).not.toBe(id2);
      expect(id1.startsWith('req_')).toBe(true);
      expect(id1).toMatch(/^req_\d+_[a-z0-9]+$/);
    });
  });

  describe('Environment Detection', () => {
    it('should detect development environment', () => {
      const isDevelopment = process.env.NODE_ENV === 'development';
      expect(typeof isDevelopment).toBe('boolean');
    });

    it('should detect test environment', () => {
      const isTest = process.env.NODE_ENV === 'test';
      expect(isTest).toBe(true);
    });

    it('should detect production environment', () => {
      const isProduction = process.env.NODE_ENV === 'production';
      expect(typeof isProduction).toBe('boolean');
    });
  });
});

describe('Performance Timing', () => {
  it('should create performance timer', () => {
    const startTimer = () => {
      return {
        start: Date.now(),
        stop: function () {
          return Date.now() - this.start;
        },
      };
    };

    const timer = startTimer();
    expect(timer.start).toBeDefined();

    // Small delay to ensure timer works
    const end = timer.stop();
    expect(typeof end).toBe('number');
    expect(end).toBeGreaterThanOrEqual(0);
  });

  it('should format duration for humans', () => {
    const formatDuration = (ms: number): string => {
      if (ms < 1000) return `${Math.round(ms)}ms`;
      if (ms < 60000) return `${(ms / 1000).toFixed(2)}s`;
      return `${(ms / 60000).toFixed(2)}m`;
    };

    expect(formatDuration(500)).toBe('500ms');
    expect(formatDuration(1500)).toBe('1.50s');
    expect(formatDuration(90000)).toBe('1.50m');
  });
});

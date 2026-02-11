/**
 * Interactive Features Module
 * Handles all client-side interactivity: mobile menu, project filtering, scroll behavior
 */

// Mobile Navigation
export function initMobileMenu(): void {
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  
  if (!mobileMenuButton || !mobileMenu) return;
  
  mobileMenuButton.addEventListener('click', () => {
    const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
    
    // Toggle visibility with animation
    if (mobileMenu.classList.contains('hidden')) {
      mobileMenu.classList.remove('hidden');
      mobileMenu.classList.add('animate-slide-in');
      mobileMenuButton.setAttribute('aria-expanded', 'true');
    } else {
      mobileMenu.classList.add('hidden');
      mobileMenu.classList.remove('animate-slide-in');
      mobileMenuButton.setAttribute('aria-expanded', 'false');
    }
  });
  
  // Close mobile menu when clicking on a link
  const mobileLinks = mobileMenu.querySelectorAll('a');
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
      mobileMenu.classList.remove('animate-slide-in');
      mobileMenuButton.setAttribute('aria-expanded', 'false');
    });
  });
}

// Project Filtering
export function initProjectFiltering(): void {
  const filterButtons = document.querySelectorAll<HTMLButtonElement>('.category-btn');
  const projectCards = document.querySelectorAll<HTMLElement>('.project-card');
  
  if (filterButtons.length === 0 || projectCards.length === 0) return;
  
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const category = button.dataset.category;
      
      // Update active button state
      filterButtons.forEach(btn => {
        btn.classList.remove('bg-primary-600', 'text-white', 'dark:bg-primary-500');
        btn.classList.add('bg-gray-200', 'text-gray-700', 'dark:bg-dark-700', 'dark:text-gray-300');
        btn.setAttribute('aria-pressed', 'false');
      });
      
      button.classList.remove('bg-gray-200', 'text-gray-700', 'dark:bg-dark-700', 'dark:text-gray-300');
      button.classList.add('bg-primary-600', 'text-white', 'dark:bg-primary-500');
      button.setAttribute('aria-pressed', 'true');
      
      // Filter projects with animation
      projectCards.forEach(card => {
        const cardCategory = card.dataset.category;
        const shouldShow = category === 'all' || cardCategory === category;
        
        if (shouldShow) {
          card.classList.remove('hidden');
          card.classList.add('animate-fade-in');
        } else {
          card.classList.add('hidden');
          card.classList.remove('animate-fade-in');
        }
      });
    });
  });
}

// Active Section Highlighting
export function initActiveSectionHighlight(): void {
  const sections = document.querySelectorAll<HTMLElement>('section[id]');
  const navLinks = document.querySelectorAll<HTMLAnchorElement>('nav a[href^="#"]');
  
  if (sections.length === 0 || navLinks.length === 0) return;
  
  const observerOptions: IntersectionObserverInit = {
    root: null,
    rootMargin: '-50% 0px -50% 0px',
    threshold: 0
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        
        // Update nav links
        navLinks.forEach(link => {
          link.classList.remove('text-primary-600', 'dark:text-primary-400');
          link.classList.add('text-gray-600', 'dark:text-gray-300');
          
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.remove('text-gray-600', 'dark:text-gray-300');
            link.classList.add('text-primary-600', 'dark:text-primary-400');
          }
        });
      }
    });
  }, observerOptions);
  
  sections.forEach(section => observer.observe(section));
}

// Scroll to Top Button
export function initScrollToTop(): void {
  const scrollButton = document.getElementById('scroll-to-top');
  
  if (!scrollButton) {
    // Create the button if it doesn't exist
    createScrollToTopButton();
    return;
  }
  
  // Show/hide button based on scroll position
  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
      scrollButton.classList.remove('hidden', 'animate-fade-out');
      scrollButton.classList.add('animate-fade-in');
    } else {
      scrollButton.classList.remove('animate-fade-in');
      scrollButton.classList.add('animate-fade-out');
      setTimeout(() => {
        if (window.scrollY <= 500) {
          scrollButton.classList.add('hidden');
        }
      }, 300);
    }
  });
  
  // Scroll to top on click
  scrollButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

function createScrollToTopButton(): void {
  const button = document.createElement('button');
  button.id = 'scroll-to-top';
  button.className = 'fixed bottom-8 right-8 p-3 rounded-full bg-primary-600 text-white shadow-lg transition-all duration-300 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-dark-900 hidden z-50';
  button.setAttribute('aria-label', 'Scroll to top');
  button.innerHTML = `
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
    </svg>
  `;
  
  document.body.appendChild(button);
  
  // Add event listener
  button.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
  
  // Show/hide on scroll
  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
      button.classList.remove('hidden');
    } else {
      button.classList.add('hidden');
    }
  });
}

// Smooth scroll for anchor links
export function initSmoothScroll(): void {
  const anchorLinks = document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]');
  
  anchorLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector<HTMLElement>(targetId);
        
        if (targetElement) {
          e.preventDefault();
          
          const headerHeight = document.querySelector<HTMLElement>('header')?.offsetHeight || 0;
          const targetPosition = targetElement.offsetTop - headerHeight;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      }
    });
  });
}

// Theme toggle (for use by inline onclick)
export function toggleTheme(): void {
  const html = document.documentElement;
  const isDark = html.classList.contains('dark');
  
  localStorage.setItem('theme', isDark ? 'light' : 'dark');
  html.classList.toggle('dark');
}

// Initialize all features
export function initAllFeatures(): void {
  initMobileMenu();
  initProjectFiltering();
  initActiveSectionHighlight();
  initScrollToTop();
  initSmoothScroll();
}

// Run on DOM content loaded
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', initAllFeatures);
}

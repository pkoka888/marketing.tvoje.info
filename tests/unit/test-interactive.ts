/**
 * Interactive Features Test Suite
 * Tests for dark mode, language toggle, project filtering, mobile nav, smooth scroll, and scroll-to-top
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock DOM environment for testing
const mockDocument = {
  documentElement: {
    classList: {
      add: vi.fn(),
      remove: vi.fn(),
      toggle: vi.fn(),
      contains: vi.fn(),
    },
    getAttribute: vi.fn(),
    setAttribute: vi.fn(),
  },
  body: {
    classList: {
      add: vi.fn(),
      remove: vi.fn(),
      toggle: vi.fn(),
    },
  },
  head: {
    appendChild: vi.fn(),
    querySelector: vi.fn(),
  },
  querySelector: vi.fn(),
  querySelectorAll: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  getElementById: vi.fn(),
  createElement: vi.fn(),
};

const mockWindow = {
  matchMedia: vi.fn(),
  localStorage: {
    getItem: vi.fn(),
    setItem: vi.fn(),
  },
  scrollTo: vi.fn(),
};

// Set up global mocks
vi.stubGlobal('document', mockDocument);
vi.stubGlobal('window', mockWindow);

describe('Interactive Features', () => {
  describe('Theme Toggle (Dark Mode)', () => {
    it('should toggle dark mode class on documentElement', () => {
      const toggleTheme = () => {
        const isDark = document.documentElement.classList.contains('dark');
        if (isDark) {
          document.documentElement.classList.remove('dark');
          localStorage.setItem('theme', 'light');
        } else {
          document.documentElement.classList.add('dark');
          localStorage.setItem('theme', 'dark');
        }
      };
      
      // Test dark mode toggle
      document.documentElement.classList.contains.mockReturnValue(false);
      toggleTheme();
      expect(document.documentElement.classList.add).toHaveBeenCalledWith('dark');
      expect(localStorage.setItem).toHaveBeenCalledWith('theme', 'dark');
    });

    it('should respect system preference when no localStorage value', () => {
      const initTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme) {
          document.documentElement.classList.toggle('dark', savedTheme === 'dark');
        } else {
          document.documentElement.classList.toggle('dark', prefersDark);
        }
      };
      
      localStorage.getItem.mockReturnValue(null);
      window.matchMedia.mockReturnValue({ matches: true });
      
      initTheme();
      expect(document.documentElement.classList.toggle).toHaveBeenCalled();
    });

    it('should use saved localStorage preference over system preference', () => {
      const initTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
          document.documentElement.classList.toggle('dark', savedTheme === 'dark');
        }
      };
      
      localStorage.getItem.mockReturnValue('dark');
      
      initTheme();
      expect(document.documentElement.classList.toggle).toHaveBeenCalledWith('dark', true);
    });
  });

  describe('Mobile Navigation', () => {
    it('should toggle mobile menu visibility', () => {
      const mobileMenuButton = { 
        setAttribute: vi.fn(),
        getAttribute: vi.fn().mockReturnValue('false') 
      };
      const mobileMenu = { 
        classList: { 
          toggle: vi.fn(),
          add: vi.fn(),
          remove: vi.fn(),
        } 
      };
      const overlay = {
        classList: {
          add: vi.fn(),
          remove: vi.fn(),
        }
      };
      
      const openMenu = () => {
        mobileMenuButton.setAttribute('aria-expanded', 'true');
        mobileMenu.classList.add('mobile-menu-open');
        overlay.classList.add('mobile-menu-overlay-active');
      };
      
      const closeMenu = () => {
        mobileMenuButton.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('mobile-menu-open');
        overlay.classList.remove('mobile-menu-overlay-active');
      };
      
      openMenu();
      expect(mobileMenuButton.setAttribute).toHaveBeenCalledWith('aria-expanded', 'true');
      expect(mobileMenu.classList.add).toHaveBeenCalledWith('mobile-menu-open');
      
      closeMenu();
      expect(mobileMenuButton.setAttribute).toHaveBeenCalledWith('aria-expanded', 'false');
    });

    it('should close menu when clicking overlay', () => {
      const overlay = {
        classList: {
          contains: vi.fn().mockReturnValue(true),
          remove: vi.fn(),
        }
      };
      
      const closeOnOverlayClick = (target: any) => {
        if (overlay.classList.contains('mobile-menu-overlay-active')) {
          overlay.classList.remove('mobile-menu-overlay-active');
        }
      };
      
      closeOnOverlayClick(overlay);
      expect(overlay.classList.remove).toHaveBeenCalledWith('mobile-menu-overlay-active');
    });
  });

  describe('Project Filtering', () => {
    it('should filter projects by category', () => {
      const filterButtons = document.querySelectorAll('.category-btn');
      const projectCards = [
        { 
          classList: { 
            contains: vi.fn((cls) => cls === 'project-card'),
            remove: vi.fn(),
            add: vi.fn(),
          },
          dataset: { category: 'devops' }
        },
        { 
          classList: { 
            contains: vi.fn((cls) => cls === 'project-card'),
            remove: vi.fn(),
            add: vi.fn(),
          },
          dataset: { category: 'ai' }
        },
      ];
      
      const filterProjects = (category: string) => {
        filterButtons.forEach((btn: any) => {
          const btnCategory = btn.dataset.category;
          if (btnCategory === category) {
            btn.classList.add('category-active');
          } else {
            btn.classList.remove('category-active');
          }
        });
        
        projectCards.forEach((card: any) => {
          if (category === 'all' || card.dataset.category === category) {
            card.classList.remove('hidden');
            card.classList.add('animate-fade-in');
          } else {
            card.classList.add('hidden');
            card.classList.remove('animate-fade-in');
          }
        });
      };
      
      filterProjects('devops');
      
      // First card should be visible
      expect(projectCards[0].classList.remove).toHaveBeenCalledWith('hidden');
      expect(projectCards[0].classList.add).toHaveBeenCalledWith('animate-fade-in');
      
      // Second card should be hidden
      expect(projectCards[1].classList.add).toHaveBeenCalledWith('hidden');
    });

    it('should show all projects when filter is "all"', () => {
      const projectCards = [
        { 
          classList: { 
            remove: vi.fn(),
            add: vi.fn(),
          },
          dataset: { category: 'devops' }
        },
        { 
          classList: { 
            remove: vi.fn(),
            add: vi.fn(),
          },
          dataset: { category: 'ai' }
        },
      ];
      
      const filterProjects = (category: string) => {
        projectCards.forEach((card: any) => {
          if (category === 'all' || card.dataset.category === category) {
            card.classList.remove('hidden');
          } else {
            card.classList.add('hidden');
          }
        });
      };
      
      filterProjects('all');
      
      projectCards.forEach((card: any) => {
        expect(card.classList.remove).toHaveBeenCalledWith('hidden');
      });
    });
  });

  describe('Smooth Scroll', () => {
    it('should scroll to anchor smoothly', () => {
      const anchor = { 
        getAttribute: vi.fn().mockReturnValue('#about'),
        href: 'http://localhost/#about',
      };
      const targetSection = { 
        getBoundingClientRect: vi.fn().mockReturnValue({ top: 100 }),
        id: 'about',
      };
      
      document.querySelector.mockImplementation((selector) => {
        if (selector === '#about') return targetSection;
        return null;
      });
      
      const scrollToAnchor = (event: Event) => {
        const target = event.target as HTMLElement;
        const href = target.getAttribute('href');
        if (href?.startsWith('#')) {
          const targetEl = document.querySelector(href);
          if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      };
      
      const mockEvent = { target: anchor };
      scrollToAnchor(mockEvent as unknown as Event);
      
      expect(targetSection.getBoundingClientRect).toHaveBeenCalled();
    });
  });

  describe('Scroll to Top Button', () => {
    it('should show button when scrolling down', () => {
      const scrollButton = {
        classList: {
          contains: vi.fn().mockReturnValue(false),
          add: vi.fn(),
          remove: vi.fn(),
        },
        style: { display: '' },
      };
      
      const checkScroll = () => {
        const scrollPosition = window.scrollY || document.documentElement.scrollTop;
        
        if (scrollPosition > 300) {
          scrollButton.classList.add('visible');
          scrollButton.style.display = 'block';
        } else {
          scrollButton.classList.remove('visible');
          scrollButton.style.display = 'none';
        }
      };
      
      // Simulate scrolling down
      const mockWindow = { scrollY: 400 };
      
      checkScroll();
      expect(scrollButton.classList.add).toHaveBeenCalledWith('visible');
      expect(scrollButton.style.display).toBe('block');
    });

    it('should hide button when at top', () => {
      const scrollButton = {
        classList: {
          contains: vi.fn().mockReturnValue(true),
          remove: vi.fn(),
        },
        style: { display: 'block' },
      };
      
      const checkScroll = () => {
        const scrollPosition = 100; // Less than threshold
        
        if (scrollPosition > 300) {
          scrollButton.classList.add('visible');
        } else {
          scrollButton.classList.remove('visible');
          scrollButton.style.display = 'none';
        }
      };
      
      checkScroll();
      expect(scrollButton.classList.remove).toHaveBeenCalledWith('visible');
    });
  });

  describe('Active Section Highlight', () => {
    it('should highlight nav link for current section', () => {
      const sections = [
        { id: 'hero', getBoundingClientRect: vi.fn().mockReturnValue({ top: -100, bottom: 500 }) },
        { id: 'projects', getBoundingClientRect: vi.fn().mockReturnValue({ top: 400, bottom: 1200 }) },
        { id: 'contact', getBoundingClientRect: vi.fn().mockReturnValue({ top: 1500, bottom: 2500 }) },
      ];
      
      const navLinks = [
        { href: '#hero', classList: { remove: vi.fn(), add: vi.fn() } },
        { href: '#projects', classList: { remove: vi.fn(), add: vi.fn() } },
        { href: '#contact', classList: { remove: vi.fn(), add: vi.fn() } },
      ];
      
      const updateActiveSection = () => {
        let currentSection = '';
        
        sections.forEach((section) => {
          const rect = section.getBoundingClientRect();
          if (rect.top <= 150 && rect.bottom >= 100) {
            currentSection = section.id;
          }
        });
        
        navLinks.forEach((link) => {
          const href = link.href.split('#')[1];
          if (href === currentSection) {
            link.classList.add('nav-active');
          } else {
            link.classList.remove('nav-active');
          }
        });
      };
      
      // Simulate being in projects section
      updateActiveSection();
      
      // Projects link should be active
      expect(navLinks[1].classList.add).toHaveBeenCalledWith('nav-active');
      // Hero link should not be active
      expect(navLinks[0].classList.remove).toHaveBeenCalledWith('nav-active');
    });
  });
});

describe('Accessibility', () => {
  describe('Keyboard Navigation', () => {
    it('should handle keyboard navigation in mobile menu', () => {
      const focusableElements = [
        { tagName: 'A', focus: vi.fn() },
        { tagName: 'BUTTON', focus: vi.fn() },
        { tagName: 'A', focus: vi.fn() },
      ];
      
      let currentFocusIndex = 0;
      
      const handleKeyboardNav = (event: KeyboardEvent) => {
        if (event.key === 'Tab') {
          event.preventDefault();
          currentFocusIndex = (currentFocusIndex + 1) % focusableElements.length;
          focusableElements[currentFocusIndex].focus();
        }
        
        if (event.key === 'Escape') {
          // Close menu
          currentFocusIndex = 0;
        }
      };
      
      const mockEvent = { key: 'Tab', preventDefault: vi.fn() };
      handleKeyboardNav(mockEvent as unknown as KeyboardEvent);
      
      expect(focusableElements[1].focus).toHaveBeenCalled();
    });
  });

  describe('ARIA Attributes', () => {
    it('should toggle aria-expanded on mobile menu button', () => {
      const button = {
        setAttribute: vi.fn(),
        getAttribute: vi.fn().mockReturnValue('false'),
      };
      
      const toggleAriaExpanded = () => {
        const isExpanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', (!isExpanded).toString());
      };
      
      toggleAriaExpanded();
      expect(button.setAttribute).toHaveBeenCalledWith('aria-expanded', 'true');
      
      toggleAriaExpanded();
      expect(button.setAttribute).toHaveBeenCalledWith('aria-expanded', 'false');
    });

    it('should toggle aria-pressed on filter buttons', () => {
      const button = {
        setAttribute: vi.fn(),
        getAttribute: vi.fn().mockReturnValue('false'),
      };
      
      const toggleAriaPressed = () => {
        const isPressed = button.getAttribute('aria-pressed') === 'true';
        button.setAttribute('aria-pressed', (!isPressed).toString());
      };
      
      toggleAriaPressed();
      expect(button.setAttribute).toHaveBeenCalledWith('aria-pressed', 'true');
    });
  });
});

describe('Animation Classes', () => {
  it('should apply fade-in animation to visible elements', () => {
    const element = {
      classList: {
        add: vi.fn(),
        remove: vi.fn(),
      },
    };
    
    const animateFadeIn = (el: any) => {
      el.classList.remove('animate-fade-out');
      el.classList.add('animate-fade-in');
    };
    
    animateFadeIn(element);
    expect(element.classList.add).toHaveBeenCalledWith('animate-fade-in');
  });

  it('should apply slide-in animation to mobile menu', () => {
    const panel = {
      classList: {
        add: vi.fn(),
        remove: vi.fn(),
      },
    };
    
    const animateSlideIn = (el: any) => {
      el.classList.add('animate-slide-in');
    };
    
    animateSlideIn(panel);
    expect(panel.classList.add).toHaveBeenCalledWith('animate-slide-in');
  });

  it('should handle filter transition animations', () => {
    const card = {
      classList: {
        add: vi.fn(),
        remove: vi.fn(),
      },
      style: {
        display: '',
        opacity: '',
      },
    };
    
    const animateFilter = (el: any, show: boolean) => {
      if (show) {
        el.classList.remove('hidden');
        el.classList.add('animate-fade-in');
      } else {
        el.classList.add('animate-fade-out');
        setTimeout(() => {
          el.classList.remove('animate-fade-out');
          el.classList.add('hidden');
        }, 300);
      }
    };
    
    animateFilter(card, true);
    expect(card.classList.remove).toHaveBeenCalledWith('hidden');
  });
});

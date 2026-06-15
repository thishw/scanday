document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('header');
    const reveals = document.querySelectorAll('.reveal');
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');

    // Header scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Reveal on scroll animation
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, {
        threshold: 0.1
    });

    reveals.forEach(reveal => {
        revealObserver.observe(reveal);
    });

    // Smooth scroll for nav links & Close mobile menu
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            // Close mobile menu if open
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                menuToggle.classList.remove('active');
            }

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Hamburger Menu Toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }
    
    // Auto-Tracking: Event Delegation for All Links and Buttons
    document.addEventListener('click', function(e) {
        const trackElement = e.target.closest('a, button, [data-track]');
        if (!trackElement) return;

        let category = 'interaction';
        let action = 'click';
        let label = trackElement.innerText.trim() || trackElement.getAttribute('aria-label') || trackElement.id || 'unknown';

        const hasExplicitTrack = trackElement.hasAttribute('data-track');

        if (hasExplicitTrack) {
            // Respect explicit tags first
            category = trackElement.getAttribute('data-category') || category;
            action = trackElement.getAttribute('data-action') || action;
            label = trackElement.getAttribute('data-label') || label;
        } else {
            // Auto-infer for untagged elements
            const tagName = trackElement.tagName.toLowerCase();
            if (tagName === 'a') {
                category = 'navigation';
                action = 'click_link';
                const href = trackElement.getAttribute('href');
                if (href) label += ` (${href})`;
            } else if (tagName === 'button') {
                category = 'interaction';
                action = 'click_button';
            }
        }

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: 'user_interaction',
            track_category: category,
            track_action: action,
            track_label: label
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('header');
    const reveals = document.querySelectorAll('.reveal');
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const syncHeader = () => header?.classList.toggle('scrolled', window.scrollY > 50);
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });

    // Content stays readable without JavaScript or animation support.
    if ('IntersectionObserver' in window && !reducedMotion.matches) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    entry.target.classList.remove('reveal-pending');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.05 });
        reveals.forEach(reveal => {
            if (reveal.getBoundingClientRect().top > window.innerHeight) {
                reveal.classList.add('reveal-pending');
                revealObserver.observe(reveal);
            }
        });
    }

    const mobileNav = window.matchMedia('(max-width: 1100px)');
    const setMenu = (open) => {
        if (!menuToggle || !navLinks) return;
        menuToggle.classList.toggle('active', open);
        navLinks.classList.toggle('active', open);
        menuToggle.setAttribute('aria-expanded', String(open));
        menuToggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
        navLinks.inert = mobileNav.matches && !open;
    };
    if (menuToggle && navLinks) {
        header.classList.add('nav-ready');
        setMenu(false);
        menuToggle.addEventListener('click', () => setMenu(menuToggle.getAttribute('aria-expanded') !== 'true'));
        mobileNav.addEventListener('change', () => setMenu(false));
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
                setMenu(false);
                menuToggle.focus();
            }
        });
        document.addEventListener('click', (event) => {
            if (!header.contains(event.target)) setMenu(false);
        });
        header.addEventListener('focusout', (event) => {
            if (!header.contains(event.relatedTarget)) setMenu(false);
        });
        navLinks.addEventListener('click', (event) => {
            if (event.target.closest('a')) setMenu(false);
        });
    }

    // Smooth scroll for nav links & Close mobile menu
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const target = href === '#' ? document.body : document.getElementById(decodeURIComponent(href.slice(1)));
            if (target) {
                e.preventDefault();
                setMenu(false);
                window.scrollTo({
                    top: href === '#' ? 0 : target.getBoundingClientRect().top + window.scrollY - (header?.offsetHeight || 0) - 16,
                    behavior: reducedMotion.matches ? 'auto' : 'smooth'
                });
                if (href !== '#') {
                    history.replaceState(null, '', href);
                    target.setAttribute('tabindex', '-1');
                    target.focus({ preventScroll: true });
                }
            }
        });
    });

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
                if (href?.startsWith('tel:')) {
                    category = 'conversion';
                    action = 'call_store';
                } else if (href?.includes('placePath=/ticket')) {
                    category = 'conversion';
                    action = 'reserve_naver';
                } else if (href?.includes('map.naver.com') || href?.includes('place.naver.com')) {
                    category = 'conversion';
                    action = 'view_directions';
                } else if (href?.includes('price_calculator.html')) {
                    category = 'conversion';
                    action = 'open_calculator';
                }
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

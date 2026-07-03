 document.addEventListener('DOMContentLoaded', function() {
        // ========================================
        // AOS INIT
        // ========================================
        AOS.init({
            duration: 800,
            once: true,
            offset: 50,
            easing: 'ease-out-cubic'
        });

        // ========================================
        // ANIMATED COUNTERS
        // ========================================
        const counters = document.querySelectorAll('.stat-number');
        
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            if (isNaN(target)) return;

            let current = 0;
            const increment = Math.max(1, Math.floor(target / 80));
            let isCounting = false;

            const updateCounter = () => {
                if (current < target) {
                    current = Math.min(current + increment, target);
                    counter.textContent = current;
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !isCounting) {
                        isCounting = true;
                        updateCounter();
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.3 });

            observer.observe(counter);
        });

        // ========================================
        // NAVBAR SCROLL EFFECT
        // ========================================
        const navbar = document.querySelector('.navbar-custom');
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });

        // ========================================
        // SCROLL TO TOP
        // ========================================
        const scrollBtn = document.getElementById('scrollTopBtn');
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
            }
        });

        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // ========================================
        // BUTTON LOADING STATES
        // ========================================
        document.querySelectorAll('.btn[data-loading]').forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (this.classList.contains('loading')) return;
                this.classList.add('loading');
                setTimeout(() => this.classList.remove('loading'), 2000);
            });
        });

        // ========================================
        // TOAST SYSTEM
        // ========================================
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            
            const icons = {
                success: 'fas fa-check-circle',
                error: 'fas fa-exclamation-circle',
                info: 'fas fa-info-circle'
            };

            toast.className = `toast-custom ${type}`;
            toast.innerHTML = `
                <div class="toast-icon"><i class="${icons[type] || icons.info}"></i></div>
                <div class="toast-msg">${message}</div>
                <button class="toast-close">&times;</button>
            `;

            container.appendChild(toast);

            // Auto dismiss
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(50px)';
                setTimeout(() => toast.remove(), 300);
            }, 4000);

            // Manual dismiss
            toast.querySelector('.toast-close').addEventListener('click', () => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(50px)';
                setTimeout(() => toast.remove(), 300);
            });
        }

        // ========================================
        // FORM HANDLING
        // ========================================
        const subscribeBtn = document.getElementById('subscribeBtn');
        if (subscribeBtn) {
            subscribeBtn.addEventListener('click', function(e) {
                const form = this.closest('form');
                const email = form.querySelector('input[type="email"]');
                
                if (!email.value || !email.value.includes('@')) {
                    e.preventDefault();
                    showToast('Please enter a valid email address', 'error');
                    return;
                }

                this.classList.add('loading');
                setTimeout(() => {
                    this.classList.remove('loading');
                    showToast('🎉 Subscribed successfully!', 'success');
                }, 1500);
            });
        }

        // ========================================
        // KEYBOARD SHORTCUTS
        // ========================================
        document.addEventListener('keydown', (e) => {
            // Ctrl + K: Open search (simulate)
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                showToast('🔍 Search feature coming soon!', 'info');
            }
            // Alt + T: Scroll to top
            if (e.altKey && e.key === 't') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            // Escape: Close all toasts
            if (e.key === 'Escape') {
                document.querySelectorAll('.toast-custom').forEach(t => {
                    t.style.opacity = '0';
                    t.style.transform = 'translateX(50px)';
                    setTimeout(() => t.remove(), 300);
                });
            }
        });

        // ========================================
        // INTERACTIVE GRID
        // ========================================
        document.querySelectorAll('.grid-item').forEach((item, index) => {
            item.addEventListener('mouseenter', () => {
                item.style.transform = 'scale(1.1)';
                item.style.background = 'rgba(108, 60, 225, 0.2)';
                item.style.border = '1px solid rgba(108, 60, 225, 0.3)';
            });
            
            item.addEventListener('mouseleave', () => {
                item.style.transform = 'scale(1)';
                if (!item.classList.contains('active')) {
                    item.style.background = 'rgba(255, 255, 255, 0.03)';
                    item.style.border = 'none';
                }
            });

            // Random active states
            if (Math.random() > 0.7) {
                item.classList.add('active');
            }
        });

        // ========================================
        // CONSOLE WELCOME
        // ========================================
        console.log('%c🚀 MySite v3.0', 'font-size: 32px; font-weight: 800; color: #6C3CE1;');
        console.log('%cBuilt with ❤️ for the future of web', 'font-size: 14px; color: rgba(255,255,255,0.5);');

        console.log('%c🔑 Keyboard Shortcuts:', 'font-weight: bold; color: #6C3CE1;');
        console.log('  Ctrl+K  → Open search');
        console.log('  Alt+T   → Scroll to top');
        console.log('  ESC     → Close all notifications');

        // ========================================
        // DYNAMIC YEAR
        // ========================================
        document.querySelectorAll('.current-year').forEach(el => {
            el.textContent = new Date().getFullYear();
        });

        // Show welcome toast after 2s
        setTimeout(() => {
            showToast('👋 Welcome to MySite v3.0!', 'success');
        }, 2000);
    });
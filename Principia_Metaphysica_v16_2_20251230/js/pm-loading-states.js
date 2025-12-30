/**
 * PM Loading States - Loading, Error, and Empty State Components
 * ===============================================================
 *
 * Provides consistent loading, error, and empty state UX across all pages.
 * Includes spinners, skeleton loaders, error messages, and empty states.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

(function(window) {
    'use strict';

    /**
     * PMLoadingStates - Global utility for consistent loading/error/empty states
     */
    const PMLoadingStates = {
        /**
         * Show a loading spinner in a container
         * @param {HTMLElement|string} container - Element or selector
         * @param {Object} options - Configuration options
         * @returns {HTMLElement} The loading container element
         */
        showLoading(container, options = {}) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) {
                console.error('Loading container not found:', container);
                return null;
            }

            const {
                message = 'Loading...',
                size = 'medium', // small, medium, large
                overlay = false
            } = options;

            const sizeClass = size === 'small' ? 'small' : size === 'large' ? 'large' : '';

            const loadingHTML = `
                <div class="loading-container ${overlay ? 'loading-overlay' : ''}" data-pm-loading>
                    <div class="loading-spinner ${sizeClass}"></div>
                    ${message ? `<div class="loading-text">${message}</div>` : ''}
                </div>
            `;

            if (overlay) {
                const overlayDiv = document.createElement('div');
                overlayDiv.className = 'loading-container loading-overlay';
                overlayDiv.setAttribute('data-pm-loading', '');
                overlayDiv.innerHTML = `
                    <div class="loading-spinner ${sizeClass}"></div>
                    ${message ? `<div class="loading-text">${message}</div>` : ''}
                `;
                element.appendChild(overlayDiv);
                return overlayDiv;
            } else {
                element.innerHTML = loadingHTML;
                return element.querySelector('[data-pm-loading]');
            }
        },

        /**
         * Hide loading spinner
         * @param {HTMLElement|string} container - Element or selector
         */
        hideLoading(container) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) return;

            const loadingElement = element.querySelector('[data-pm-loading]');
            if (loadingElement) {
                loadingElement.remove();
            }
        },

        /**
         * Show skeleton loader
         * @param {HTMLElement|string} container - Element or selector
         * @param {Object} options - Configuration options
         */
        showSkeleton(container, options = {}) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) {
                console.error('Skeleton container not found:', container);
                return null;
            }

            const {
                type = 'card', // card, text, list
                count = 1
            } = options;

            let skeletonHTML = '';

            if (type === 'card') {
                for (let i = 0; i < count; i++) {
                    skeletonHTML += `
                        <div class="skeleton skeleton-card" style="margin-bottom: 1rem;">
                            <div class="skeleton skeleton-title"></div>
                            <div class="skeleton skeleton-text"></div>
                            <div class="skeleton skeleton-text" style="width: 80%;"></div>
                            <div class="skeleton skeleton-text" style="width: 60%;"></div>
                        </div>
                    `;
                }
            } else if (type === 'text') {
                for (let i = 0; i < count; i++) {
                    skeletonHTML += `<div class="skeleton skeleton-text"></div>`;
                }
            } else if (type === 'list') {
                for (let i = 0; i < count; i++) {
                    skeletonHTML += `
                        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                            <div class="skeleton" style="width: 40px; height: 40px; border-radius: 50%;"></div>
                            <div style="flex: 1;">
                                <div class="skeleton skeleton-text" style="width: 70%;"></div>
                                <div class="skeleton skeleton-text" style="width: 50%;"></div>
                            </div>
                        </div>
                    `;
                }
            }

            element.innerHTML = `<div data-pm-skeleton>${skeletonHTML}</div>`;
        },

        /**
         * Show error message
         * @param {HTMLElement|string} container - Element or selector
         * @param {Object} options - Configuration options
         */
        showError(container, options = {}) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) {
                console.error('Error container not found:', container);
                return null;
            }

            const {
                title = 'Error',
                message = 'Something went wrong. Please try again.',
                retry = null,
                retryText = 'Retry',
                icon = '⚠️'
            } = options;

            const retryButton = retry
                ? `<button class="btn btn-primary error-action" onclick="${retry}">${retryText}</button>`
                : '';

            const errorHTML = `
                <div class="error-container" data-pm-error>
                    <div class="error-icon">${icon}</div>
                    <h3 class="error-title">${title}</h3>
                    <p class="error-message">${message}</p>
                    ${retryButton}
                </div>
            `;

            element.innerHTML = errorHTML;
            return element.querySelector('[data-pm-error]');
        },

        /**
         * Show inline field error
         * @param {HTMLElement|string} field - Input field or selector
         * @param {string} message - Error message
         */
        showFieldError(field, message) {
            const element = typeof field === 'string'
                ? document.querySelector(field)
                : field;

            if (!element) return;

            // Remove existing error
            this.hideFieldError(element);

            // Add error class to field
            element.classList.add('error');

            // Create error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.setAttribute('data-field-error', '');
            errorDiv.innerHTML = `
                <span>⚠️</span>
                <span>${message}</span>
            `;

            // Insert after field
            element.parentNode.insertBefore(errorDiv, element.nextSibling);
        },

        /**
         * Hide inline field error
         * @param {HTMLElement|string} field - Input field or selector
         */
        hideFieldError(field) {
            const element = typeof field === 'string'
                ? document.querySelector(field)
                : field;

            if (!element) return;

            element.classList.remove('error');

            const errorElement = element.parentNode.querySelector('[data-field-error]');
            if (errorElement) {
                errorElement.remove();
            }
        },

        /**
         * Show empty state
         * @param {HTMLElement|string} container - Element or selector
         * @param {Object} options - Configuration options
         */
        showEmpty(container, options = {}) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) {
                console.error('Empty state container not found:', container);
                return null;
            }

            const {
                title = 'No Data',
                message = 'There is nothing to display yet.',
                action = null,
                actionText = 'Get Started',
                icon = '📭'
            } = options;

            const actionButton = action
                ? `<button class="btn btn-primary empty-action" onclick="${action}">${actionText}</button>`
                : '';

            const emptyHTML = `
                <div class="empty-state" data-pm-empty>
                    <div class="empty-icon">${icon}</div>
                    <h3 class="empty-title">${title}</h3>
                    <p class="empty-message">${message}</p>
                    ${actionButton}
                </div>
            `;

            element.innerHTML = emptyHTML;
            return element.querySelector('[data-pm-empty]');
        },

        /**
         * Show success message
         * @param {HTMLElement|string} container - Element or selector
         * @param {Object} options - Configuration options
         */
        showSuccess(container, options = {}) {
            const element = typeof container === 'string'
                ? document.querySelector(container)
                : container;

            if (!element) return null;

            const {
                title = 'Success',
                message = 'Operation completed successfully.',
                duration = 3000,
                icon = '✓'
            } = options;

            const successHTML = `
                <div class="success-container fade-in" data-pm-success style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 1rem;
                    padding: 2rem;
                    text-align: center;
                ">
                    <div style="
                        width: 64px;
                        height: 64px;
                        background: var(--success-bg);
                        border: 2px solid var(--success);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 2rem;
                        color: var(--success);
                    ">${icon}</div>
                    <h3 style="color: var(--success); margin: 0; font-size: 1.25rem;">${title}</h3>
                    <p style="color: var(--text-secondary); margin: 0;">${message}</p>
                </div>
            `;

            element.innerHTML = successHTML;

            if (duration > 0) {
                setTimeout(() => {
                    const successElement = element.querySelector('[data-pm-success]');
                    if (successElement) {
                        successElement.style.opacity = '0';
                        setTimeout(() => successElement.remove(), 300);
                    }
                }, duration);
            }
        },

        /**
         * Show toast notification
         * @param {string} message - Toast message
         * @param {Object} options - Configuration options
         */
        showToast(message, options = {}) {
            const {
                type = 'info', // info, success, warning, error
                duration = 3000,
                position = 'bottom-right' // top-left, top-right, bottom-left, bottom-right, top-center, bottom-center
            } = options;

            // Create toast container if it doesn't exist
            let toastContainer = document.getElementById('pm-toast-container');
            if (!toastContainer) {
                toastContainer = document.createElement('div');
                toastContainer.id = 'pm-toast-container';
                toastContainer.style.cssText = `
                    position: fixed;
                    z-index: 10000;
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                    pointer-events: none;
                `;

                // Position the container
                const positions = {
                    'top-left': 'top: 1rem; left: 1rem;',
                    'top-right': 'top: 1rem; right: 1rem;',
                    'bottom-left': 'bottom: 1rem; left: 1rem;',
                    'bottom-right': 'bottom: 1rem; right: 1rem;',
                    'top-center': 'top: 1rem; left: 50%; transform: translateX(-50%);',
                    'bottom-center': 'bottom: 1rem; left: 50%; transform: translateX(-50%);'
                };
                toastContainer.style.cssText += positions[position] || positions['bottom-right'];

                document.body.appendChild(toastContainer);
            }

            // Color schemes
            const colors = {
                info: { bg: 'var(--info-bg)', border: 'var(--info)', color: 'var(--info)' },
                success: { bg: 'var(--success-bg)', border: 'var(--success)', color: 'var(--success)' },
                warning: { bg: 'var(--warning-bg)', border: 'var(--warning)', color: 'var(--warning)' },
                error: { bg: 'var(--error-bg)', border: 'var(--error)', color: 'var(--error)' }
            };

            const scheme = colors[type] || colors.info;

            // Create toast element
            const toast = document.createElement('div');
            toast.className = 'pm-toast fade-in';
            toast.style.cssText = `
                background: ${scheme.bg};
                border: 1px solid ${scheme.border};
                border-left: 4px solid ${scheme.border};
                color: ${scheme.color};
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: var(--shadow-lg);
                min-width: 250px;
                max-width: 400px;
                pointer-events: auto;
                cursor: pointer;
                transition: all 0.3s ease;
            `;
            toast.textContent = message;

            // Add hover effect
            toast.addEventListener('mouseenter', () => {
                toast.style.transform = 'translateX(-4px)';
            });
            toast.addEventListener('mouseleave', () => {
                toast.style.transform = 'translateX(0)';
            });

            // Click to dismiss
            toast.addEventListener('click', () => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(20px)';
                setTimeout(() => toast.remove(), 300);
            });

            toastContainer.appendChild(toast);

            // Auto-dismiss
            if (duration > 0) {
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.style.opacity = '0';
                        toast.style.transform = 'translateX(20px)';
                        setTimeout(() => toast.remove(), 300);
                    }
                }, duration);
            }

            return toast;
        }
    };

    // Export to global scope
    window.PMLoadingStates = PMLoadingStates;

    // Add CSS for loading overlay if not already present
    if (!document.getElementById('pm-loading-styles')) {
        const style = document.createElement('style');
        style.id = 'pm-loading-styles';
        style.textContent = `
            .loading-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(10, 10, 15, 0.8);
                backdrop-filter: blur(4px);
                -webkit-backdrop-filter: blur(4px);
                z-index: 100;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }

            input.error,
            select.error,
            textarea.error {
                border-color: var(--error) !important;
                box-shadow: 0 0 0 3px var(--error-bg) !important;
            }
        `;
        document.head.appendChild(style);
    }

    console.log('%cPM Loading States initialized', 'color: #8b7fff; font-weight: bold');

})(window);

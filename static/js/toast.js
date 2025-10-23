// Toast Notification System for AJAX
class ToastManager {
    constructor() {
        this.container = document.querySelector('.toast-container');
        this.template = document.getElementById('toastTemplate');
    }

    show(message, type = 'success', title = null) {
        if (!this.template) {
            console.error('Toast template not found');
            return;
        }

        // Clone the template
        const toastElement = this.template.content.cloneNode(true).querySelector('.toast');
        
        // Set toast type and content
        this.configureToast(toastElement, message, type, title);
        
        // Add to container
        this.container.appendChild(toastElement);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove from DOM after hide
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
        
        return toast;
    }

    configureToast(toastElement, message, type, title) {
        const icon = toastElement.querySelector('.toast-header i');
        const titleElement = toastElement.querySelector('.toast-title');
        const messageElement = toastElement.querySelector('.toast-message');
        const timeElement = toastElement.querySelector('.toast-time');
        
        // Set message
        messageElement.textContent = message;
        
        // Set time
        timeElement.textContent = this.getCurrentTime();
        
        // Configure based on type
        switch (type) {
            case 'success':
                icon.className = 'fas fa-check-circle text-success me-2';
                titleElement.textContent = title || 'Success';
                toastElement.querySelector('.toast-header').classList.add('bg-success', 'text-white');
                break;
                
            case 'error':
                icon.className = 'fas fa-exclamation-triangle text-danger me-2';
                titleElement.textContent = title || 'Error';
                toastElement.querySelector('.toast-header').classList.add('bg-danger', 'text-white');
                break;
                
            case 'warning':
                icon.className = 'fas fa-exclamation-circle text-warning me-2';
                titleElement.textContent = title || 'Warning';
                toastElement.querySelector('.toast-header').classList.add('bg-warning');
                break;
                
            case 'info':
                icon.className = 'fas fa-info-circle text-info me-2';
                titleElement.textContent = title || 'Info';
                toastElement.querySelector('.toast-header').classList.add('bg-info', 'text-white');
                break;
                
            case 'loading':
                icon.className = 'fas fa-spinner fa-spin text-primary me-2';
                titleElement.textContent = title || 'Loading';
                toastElement.querySelector('.toast-header').classList.add('bg-primary', 'text-white');
                break;
        }
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            second: '2-digit'
        });
    }

    // Convenience methods
    success(message, title = null) {
        return this.show(message, 'success', title);
    }

    error(message, title = null) {
        return this.show(message, 'error', title);
    }

    warning(message, title = null) {
        return this.show(message, 'warning', title);
    }

    info(message, title = null) {
        return this.show(message, 'info', title);
    }

    loading(message, title = null) {
        const toast = this.show(message, 'loading', title);
        // Loading toasts don't auto-hide
        toast._config.autohide = false;
        return toast;
    }
}

// Global instance
const toastManager = new ToastManager();

// Function to show toast (for backward compatibility)
function showToast(message, type = 'success', title = null) {
    return toastManager.show(message, type, title);
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { toastManager, showToast };
}
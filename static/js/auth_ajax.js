// AJAX Authentication
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthAJAX();
});

function initializeAuthAJAX() {
    setupCSRFToken();
    setupAuthEventListeners();
}

function setupAuthEventListeners() {
    // Login form
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        loginUser();
    });
    
    // Register form
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        registerUser();
    });
    
    // AJAX Logout
    $('#ajaxLogoutBtn').on('click', function(e) {
        e.preventDefault();
        logoutUser();
    });
}

function setupCSRFToken() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function loginUser() {
    const formData = {
        username: $('#id_username').val(),
        password: $('#id_password').val()
    };
    
    showAuthLoading('login');
    
    $.ajax({
        url: '/ajax/login/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            hideAuthLoading('login');
            if (response.success) {
                showToast(response.message, 'success');
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 1000);
            } else {
                showToast(response.message, 'error');
            }
        },
        error: function(xhr, status, error) {
            hideAuthLoading('login');
            showToast('Network error: ' + error, 'error');
        }
    });
}

function registerUser() {
    const formData = {
        username: $('#id_username').val(),
        password1: $('#id_password1').val(),
        password2: $('#id_password2').val()
    };
    
    showAuthLoading('register');
    
    $.ajax({
        url: '/ajax/register/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            hideAuthLoading('register');
            if (response.success) {
                showToast(response.message, 'success');
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 1000);
            } else {
                if (response.errors) {
                    let errorMessage = '';
                    for (const field in response.errors) {
                        errorMessage += response.errors[field] + ' ';
                    }
                    showToast(errorMessage, 'error');
                } else {
                    showToast(response.message, 'error');
                }
            }
        },
        error: function(xhr, status, error) {
            hideAuthLoading('register');
            showToast('Network error: ' + error, 'error');
        }
    });
}

function logoutUser() {
    $.ajax({
        url: '/ajax/logout/',
        type: 'POST',
        success: function(response) {
            if (response.success) {
                showToast(response.message, 'success');
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 1000);
            } else {
                showToast(response.message, 'error');
            }
        },
        error: function(xhr, status, error) {
            showToast('Network error: ' + error, 'error');
        }
    });
}

function showAuthLoading(formType) {
    $(`#${formType}Form button[type="submit"]`).prop('disabled', true);
    $(`#${formType}Form`).append(`
        <div class="text-center mt-3">
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <small class="text-muted ms-2">Processing...</small>
        </div>
    `);
}

function hideAuthLoading(formType) {
    $(`#${formType}Form button[type="submit"]`).prop('disabled', false);
    $(`#${formType}Form .spinner-border`).parent().remove();
}

function showToast(message, type = 'success') {
    const toastHtml = `
        <div class="toast align-items-center text-bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    $('.toast-container').append(toastHtml);
    const toastElement = $('.toast-container .toast').last()[0];
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    $(toastElement).on('hidden.bs.toast', function() {
        $(this).remove();
    });
}
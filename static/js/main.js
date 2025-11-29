/**
 * Main JavaScript file for LifeLink Blood Bank Management System
 */

// Global variables
let currentUser = null;
let notifications = [];
let emergencyRequests = [];

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserData();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('LifeLink Blood Bank Management System initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize modals
    initializeModals();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize real-time updates
    initializeRealTimeUpdates();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Navigation toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Password toggle
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('lucide-eye');
                icon.classList.add('lucide-eye-off');
            } else {
                input.type = 'password';
                icon.classList.remove('lucide-eye-off');
                icon.classList.add('lucide-eye');
            }
        });
    });
    
    // Form submissions
    setupFormSubmissions();
    
    // Search functionality
    setupSearchFunctionality();
    
    // Emergency request handling
    setupEmergencyHandling();
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = this.getAttribute('data-tooltip');
            showTooltip(this, tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

/**
 * Show tooltip
 */
function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-popup';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: #2d3748;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    const tooltip = document.querySelector('.tooltip-popup');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Initialize modals
 */
function initializeModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalCloses = document.querySelectorAll('[data-modal-close]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            openModal(modalId);
        });
    });
    
    modalCloses.forEach(close => {
        close.addEventListener('click', function() {
            const modal = this.closest('.modal');
            closeModal(modal);
        });
    });
    
    // Close modal on overlay click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal(e.target);
        }
    });
}

/**
 * Open modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        // Focus first input
        const firstInput = modal.querySelector('input, textarea, select');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

/**
 * Close modal
 */
function closeModal(modal) {
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

/**
 * Validate form
 */
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate field
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Remove existing error
    removeFieldError(field);
    
    // Required validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    
    // Phone validation
    if (fieldName === 'phone' && value) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/\D/g, ''))) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    // Age validation
    if (fieldName === 'age' && value) {
        const age = parseInt(value);
        if (isNaN(age) || age < 18 || age > 65) {
            isValid = false;
            errorMessage = 'Age must be between 18 and 65';
        }
    }
    
    // Show error if invalid
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    field.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error text-red-600 text-sm mt-1';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Remove field error
 */
function removeFieldError(field) {
    field.classList.remove('error');
    
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Setup form submissions
 */
function setupFormSubmissions() {
    // Login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Registration form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistration);
    }
    
    // Emergency request form
    const emergencyForm = document.getElementById('emergency-form');
    if (emergencyForm) {
        emergencyForm.addEventListener('submit', handleEmergencyRequest);
    }
}

/**
 * Handle login
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const password = formData.get('password');
    
    try {
        showLoading('Logging in...');
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Simulate successful login
        currentUser = {
            id: 1,
            name: 'John Smith',
            email: email,
            type: 'donor'
        };
        
        localStorage.setItem('user', JSON.stringify(currentUser));
        
        showNotification('Login successful!', 'success');
        
        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = '/dashboard/donor';
        }, 1000);
        
    } catch (error) {
        showNotification('Login failed. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Handle registration
 */
async function handleRegistration(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const userData = Object.fromEntries(formData);
    
    try {
        showLoading('Creating account...');
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        showNotification('Account created successfully!', 'success');
        
        // Redirect to login
        setTimeout(() => {
            window.location.href = '/login';
        }, 1000);
        
    } catch (error) {
        showNotification('Registration failed. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Handle emergency request
 */
async function handleEmergencyRequest(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const requestData = Object.fromEntries(formData);
    
    try {
        showLoading('Submitting emergency request...');
        
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        showNotification('Emergency request submitted successfully!', 'success');
        
        // Reset form
        e.target.reset();
        
    } catch (error) {
        showNotification('Failed to submit emergency request. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Setup search functionality
 */
function setupSearchFunctionality() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                performSearch(query);
            } else {
                clearSearchResults();
            }
        }, 300));
    }
}

/**
 * Perform search
 */
async function performSearch(query) {
    try {
        const response = await fetch(`/api/search/donors?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success) {
            displaySearchResults(data.donors);
        }
    } catch (error) {
        console.error('Search failed:', error);
    }
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = '';
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p class="text-gray-500 p-4">No results found</p>';
        return;
    }
    
    results.forEach(donor => {
        const donorElement = createDonorElement(donor);
        resultsContainer.appendChild(donorElement);
    });
    
    resultsContainer.classList.remove('hidden');
}

/**
 * Create donor element
 */
function createDonorElement(donor) {
    const div = document.createElement('div');
    div.className = 'p-4 border-b hover:bg-gray-50 cursor-pointer';
    div.innerHTML = `
        <div class="flex items-center justify-between">
            <div>
                <h4 class="font-semibold">${donor.name}</h4>
                <p class="text-sm text-gray-600">${donor.city}</p>
            </div>
            <span class="blood-type-badge blood-type-${donor.blood_type.toLowerCase().replace('+', '-positive').replace('-', '-negative')}">
                ${donor.blood_type}
            </span>
        </div>
    `;
    
    div.addEventListener('click', () => {
        window.location.href = `/donors/${donor.id}`;
    });
    
    return div;
}

/**
 * Clear search results
 */
function clearSearchResults() {
    const resultsContainer = document.getElementById('search-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
        resultsContainer.classList.add('hidden');
    }
}

/**
 * Setup emergency handling
 */
function setupEmergencyHandling() {
    const emergencyButtons = document.querySelectorAll('[data-emergency]');
    emergencyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.getAttribute('data-emergency');
            handleEmergencyResponse(requestId);
        });
    });
}

/**
 * Handle emergency response
 */
async function handleEmergencyResponse(requestId) {
    if (!currentUser) {
        showNotification('Please login to respond to emergency requests', 'warning');
        return;
    }
    
    try {
        showLoading('Responding to emergency...');
        
        const response = await fetch(`/emergency/${requestId}/fulfill`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Emergency response submitted successfully!', 'success');
            // Update UI to show fulfilled status
            updateEmergencyStatus(requestId, 'fulfilled');
        } else {
            showNotification(data.message || 'Failed to respond to emergency', 'error');
        }
        
    } catch (error) {
        showNotification('Failed to respond to emergency. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Update emergency status
 */
function updateEmergencyStatus(requestId, status) {
    const emergencyElement = document.querySelector(`[data-emergency-id="${requestId}"]`);
    if (emergencyElement) {
        const statusBadge = emergencyElement.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.textContent = status === 'fulfilled' ? 'Fulfilled' : 'Active';
            statusBadge.className = `status-badge px-2 py-1 rounded-full text-xs font-medium ${
                status === 'fulfilled' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`;
        }
    }
}

/**
 * Initialize real-time updates
 */
function initializeRealTimeUpdates() {
    // Poll for new emergency requests
    setInterval(async () => {
        if (currentUser) {
            await checkNewEmergencies();
        }
    }, 30000); // Check every 30 seconds
    
    // Poll for notifications
    setInterval(async () => {
        if (currentUser) {
            await checkNotifications();
        }
    }, 60000); // Check every minute
}

/**
 * Check for new emergencies
 */
async function checkNewEmergencies() {
    try {
        const response = await fetch('/api/emergency/active');
        const data = await response.json();
        
        if (data.success && data.emergencies.length > 0) {
            // Update emergency count in UI
            updateEmergencyCount(data.emergencies.length);
            
            // Show notification for new emergencies
            const newEmergencies = data.emergencies.filter(e => !emergencyRequests.includes(e.id));
            if (newEmergencies.length > 0) {
                showNotification(`${newEmergencies.length} new emergency request(s)`, 'warning');
            }
            
            emergencyRequests = data.emergencies.map(e => e.id);
        }
    } catch (error) {
        console.error('Failed to check emergencies:', error);
    }
}

/**
 * Check for notifications
 */
async function checkNotifications() {
    try {
        const response = await fetch('/api/notifications');
        const data = await response.json();
        
        if (data.success && data.notifications.length > 0) {
            const unreadCount = data.unread_count;
            updateNotificationCount(unreadCount);
            
            if (unreadCount > 0) {
                showNotification(`${unreadCount} new notification(s)`, 'info');
            }
        }
    } catch (error) {
        console.error('Failed to check notifications:', error);
    }
}

/**
 * Update emergency count
 */
function updateEmergencyCount(count) {
    const countElement = document.getElementById('emergency-count');
    if (countElement) {
        countElement.textContent = count;
        countElement.classList.toggle('hidden', count === 0);
    }
}

/**
 * Update notification count
 */
function updateNotificationCount(count) {
    const countElement = document.getElementById('notification-count');
    if (countElement) {
        countElement.textContent = count;
        countElement.classList.toggle('hidden', count === 0);
    }
}

/**
 * Load user data
 */
function loadUserData() {
    const userData = localStorage.getItem('user');
    if (userData) {
        currentUser = JSON.parse(userData);
        updateUserInterface();
    }
}

/**
 * Update user interface
 */
function updateUserInterface() {
    if (currentUser) {
        // Update user name in header
        const userNameElement = document.getElementById('user-name');
        if (userNameElement) {
            userNameElement.textContent = currentUser.name;
        }
        
        // Show user-specific elements
        const userElements = document.querySelectorAll('.user-only');
        userElements.forEach(element => {
            element.classList.remove('hidden');
        });
        
        // Hide guest elements
        const guestElements = document.querySelectorAll('.guest-only');
        guestElements.forEach(element => {
            element.classList.add('hidden');
        });
    } else {
        // Show guest elements
        const guestElements = document.querySelectorAll('.guest-only');
        guestElements.forEach(element => {
            element.classList.remove('hidden');
        });
        
        // Hide user elements
        const userElements = document.querySelectorAll('.user-only');
        userElements.forEach(element => {
            element.classList.add('hidden');
        });
    }
}

/**
 * Show loading indicator
 */
function showLoading(message = 'Loading...') {
    const loading = document.createElement('div');
    loading.id = 'loading-overlay';
    loading.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    loading.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <div class="spinner mx-auto mb-4"></div>
            <p class="text-center">${message}</p>
        </div>
    `;
    
    document.body.appendChild(loading);
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loading = document.getElementById('loading-overlay');
    if (loading) {
        loading.remove();
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm animate-fade-in`;
    
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    
    notification.className += ` ${colors[type] || colors.info}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format phone number
 */
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3];
    }
    return phone;
}

/**
 * Format date
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Format time ago
 */
function formatTimeAgo(date) {
    const now = new Date();
    const past = new Date(date);
    const diffInSeconds = Math.floor((now - past) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days !== 1 ? 's' : ''} ago`;
    }
}

// Export functions for use in other scripts
window.LifeLink = {
    showNotification,
    showLoading,
    hideLoading,
    formatPhoneNumber,
    formatDate,
    formatTimeAgo,
    openModal,
    closeModal
}; 
/**
 * LifeLink Notification System
 * Handles browser notifications, sound alerts, and notification permissions
 */

class NotificationManager {
    constructor() {
        this.permissionGranted = false;
        this.notificationSound = null;
        this.unreadCount = 0;
        this.init();
    }

    /**
     * Initialize the notification system
     */
    init() {
        // Check if browser supports notifications
        if (!("Notification" in window)) {
            console.warn("This browser does not support desktop notifications");
            return;
        }

        // Check current permission status
        if (Notification.permission === "granted") {
            this.permissionGranted = true;
        } else if (Notification.permission !== "denied") {
            // Request permission automatically on page load
            this.requestPermission();
        }

        // Load notification sound
        this.loadNotificationSound();

        // Update page title with unread count
        this.updateBadge();
    }

    /**
     * Request notification permission from user
     */
    async requestPermission() {
        try {
            const permission = await Notification.requestPermission();
            if (permission === "granted") {
                this.permissionGranted = true;
                console.log("Notification permission granted");
                // Show a test notification
                this.showNotification("Notifications Enabled", {
                    body: "You'll now receive alerts for new messages",
                    icon: "/static/images/logo.png",
                    tag: "permission-granted"
                });
            } else {
                console.log("Notification permission denied");
            }
        } catch (error) {
            console.error("Error requesting notification permission:", error);
        }
    }

    /**
     * Load notification sound
     */
    loadNotificationSound() {
        // Create a simple notification sound using Web Audio API
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn("Web Audio API not supported");
        }
    }

    /**
     * Play notification sound
     */
    playSound() {
        if (!this.audioContext) return;

        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);

            oscillator.frequency.value = 800;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);

            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.5);
        } catch (error) {
            console.error("Error playing notification sound:", error);
        }
    }

    /**
     * Show browser notification
     * @param {string} title - Notification title
     * @param {object} options - Notification options (body, icon, tag, etc.)
     */
    showNotification(title, options = {}) {
        if (!this.permissionGranted) {
            console.log("Notification permission not granted");
            return null;
        }

        const defaultOptions = {
            icon: "/static/images/logo.png",
            badge: "/static/images/badge.png",
            vibrate: [200, 100, 200],
            requireInteraction: false,
            timestamp: Date.now(),
            ...options
        };

        try {
            const notification = new Notification(title, defaultOptions);

            // Auto-close after 10 seconds if not clicked
            setTimeout(() => {
                notification.close();
            }, 10000);

            // Handle notification click
            notification.onclick = function(event) {
                event.preventDefault();
                window.focus();
                if (options.onClick) {
                    options.onClick();
                }
                notification.close();
            };

            return notification;
        } catch (error) {
            console.error("Error showing notification:", error);
            return null;
        }
    }

    /**
     * Show message notification
     * @param {object} messageData - Message data from socket
     */
    showMessageNotification(messageData) {
        const { sender_name, message, sender_type } = messageData;
        
        // Show browser notification
        this.showNotification(`New message from ${sender_name}`, {
            body: message.length > 100 ? message.substring(0, 100) + '...' : message,
            icon: sender_type === 'donor' ? '/static/images/donor-icon.png' : '/static/images/patient-icon.png',
            tag: `message-${sender_name}`,
            data: messageData,
            onClick: () => {
                // Focus on chat if it's open
                const chatModal = document.getElementById('chatModal');
                if (chatModal && !chatModal.classList.contains('hidden')) {
                    chatModal.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });

        // Play sound
        this.playSound();

        // Show toastr notification (in-app)
        if (typeof toastr !== 'undefined') {
            toastr.options = {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: "5000",
                extendedTimeOut: "2000",
                showMethod: 'fadeIn',
                hideMethod: 'fadeOut',
                onclick: function() {
                    // Handle toast click - could open chat
                    console.log('Toast clicked for message from:', sender_name);
                }
            };
            toastr.info(`${message}`, `New message from ${sender_name}`, {
                timeOut: 5000,
                closeButton: true,
                progressBar: true
            });
        }

        // Increment unread count
        this.incrementUnreadCount();

        // Flash the page title
        this.flashTitle(`New message from ${sender_name}`);
    }

    /**
     * Show emergency notification
     * @param {object} emergencyData - Emergency request data
     */
    showEmergencyNotification(emergencyData) {
        const { patient_name, blood_type, hospital, urgency } = emergencyData;
        
        this.showNotification(`🚨 Emergency Blood Request - ${urgency}`, {
            body: `${patient_name} needs ${blood_type} blood at ${hospital}`,
            icon: '/static/images/emergency-icon.png',
            tag: 'emergency-alert',
            requireInteraction: true, // Don't auto-dismiss emergency
            vibrate: [200, 100, 200, 100, 200], // More vibration for emergency
        });

        // Play urgent sound
        this.playUrgentSound();

        // Show urgent toastr
        if (typeof toastr !== 'undefined') {
            toastr.error(`${patient_name} needs ${blood_type} blood urgently at ${hospital}`, '🚨 Emergency Blood Request', {
                timeOut: 0, // Don't auto-close
                closeButton: true,
                extendedTimeOut: 0,
                tapToDismiss: false
            });
        }
    }

    /**
     * Play urgent sound for emergencies
     */
    playUrgentSound() {
        if (!this.audioContext) return;

        try {
            // Play 3 beeps
            for (let i = 0; i < 3; i++) {
                setTimeout(() => {
                    const oscillator = this.audioContext.createOscillator();
                    const gainNode = this.audioContext.createGain();

                    oscillator.connect(gainNode);
                    gainNode.connect(this.audioContext.destination);

                    oscillator.frequency.value = 1000;
                    oscillator.type = 'square';

                    gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);

                    oscillator.start(this.audioContext.currentTime);
                    oscillator.stop(this.audioContext.currentTime + 0.2);
                }, i * 300);
            }
        } catch (error) {
            console.error("Error playing urgent sound:", error);
        }
    }

    /**
     * Increment unread message count
     */
    incrementUnreadCount() {
        this.unreadCount++;
        this.updateBadge();
    }

    /**
     * Reset unread count
     */
    resetUnreadCount() {
        this.unreadCount = 0;
        this.updateBadge();
    }

    /**
     * Update page title and favicon badge
     */
    updateBadge() {
        const originalTitle = document.title.replace(/^\(\d+\)\s*/, '');
        if (this.unreadCount > 0) {
            document.title = `(${this.unreadCount}) ${originalTitle}`;
        } else {
            document.title = originalTitle;
        }

        // Update badge in tab (if supported)
        if ('setAppBadge' in navigator) {
            navigator.setAppBadge(this.unreadCount).catch(err => {
                console.log('Badge API not supported:', err);
            });
        }
    }

    /**
     * Flash page title to grab attention
     * @param {string} message - Message to flash
     */
    flashTitle(message) {
        const originalTitle = document.title;
        let isOriginal = false;
        let flashCount = 0;
        const maxFlashes = 6;

        const flashInterval = setInterval(() => {
            if (flashCount >= maxFlashes) {
                document.title = originalTitle;
                clearInterval(flashInterval);
                return;
            }

            document.title = isOriginal ? originalTitle : `💬 ${message}`;
            isOriginal = !isOriginal;
            flashCount++;
        }, 1000);

        // Stop flashing when user focuses the window
        window.addEventListener('focus', () => {
            clearInterval(flashInterval);
            document.title = originalTitle;
        }, { once: true });
    }

    /**
     * Request permission with a custom UI prompt
     */
    showPermissionPrompt() {
        if (Notification.permission === "granted") {
            return;
        }

        if (Notification.permission === "denied") {
            if (typeof toastr !== 'undefined') {
                toastr.warning(
                    'Please enable notifications in your browser settings to receive alerts',
                    'Notifications Blocked',
                    { timeOut: 7000 }
                );
            }
            return;
        }

        // Show a friendly prompt
        if (typeof toastr !== 'undefined') {
            toastr.info(
                'Stay updated with real-time notifications for new messages and emergency requests',
                'Enable Notifications?',
                {
                    timeOut: 0,
                    closeButton: true,
                    tapToDismiss: false,
                    onclick: () => {
                        this.requestPermission();
                    }
                }
            );
        }
    }
}

// Create global notification manager instance
const notificationManager = new NotificationManager();

// Auto-request permission when user interacts with the page
document.addEventListener('DOMContentLoaded', () => {
    // Show permission prompt after a short delay
    setTimeout(() => {
        if (Notification.permission === "default") {
            notificationManager.showPermissionPrompt();
        }
    }, 3000);

    // Reset unread count when chat is opened
    const chatModal = document.getElementById('chatModal');
    if (chatModal) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'class') {
                    const isHidden = chatModal.classList.contains('hidden');
                    if (!isHidden) {
                        notificationManager.resetUnreadCount();
                    }
                }
            });
        });

        observer.observe(chatModal, { attributes: true });
    }

    // Reset unread count when window gains focus
    window.addEventListener('focus', () => {
        const chatModal = document.getElementById('chatModal');
        if (chatModal && !chatModal.classList.contains('hidden')) {
            notificationManager.resetUnreadCount();
        }
    });
});

// Export for use in other scripts
window.notificationManager = notificationManager;

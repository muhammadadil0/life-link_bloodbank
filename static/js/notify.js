// Simple Browser Notification Helper for LifeLink
// Just include this file in your HTML and call showNotification() when needed

function showNotification(senderName, message) {
    console.log('showNotification called:', senderName, message);

    // 1. Show browser notification
    if ("Notification" in window) {
        console.log('Notification permission:', Notification.permission);

        if (Notification.permission === "granted") {
            try {
                const notification = new Notification('💬 ' + senderName, {
                    body: message,
                    icon: '/static/images/logo.png',
                    tag: 'message-' + senderName,
                    requireInteraction: false
                });

                setTimeout(() => notification.close(), 10000);

                notification.onclick = function () {
                    window.focus();
                    notification.close();
                };

                console.log('Notification shown successfully');
            } catch (e) {
                console.error('Error showing notification:', e);
            }
        } else if (Notification.permission === "default") {
            console.log('Requesting notification permission...');
            Notification.requestPermission().then(function (permission) {
                console.log('Permission result:', permission);
                if (permission === "granted") {
                    showNotification(senderName, message);
                }
            });
        } else {
            console.warn('Notification permission denied');
        }
    } else {
        console.warn('Notifications not supported in this browser');
    }

    // 2. Play sound
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
        console.log('Sound played');
    } catch (e) {
        console.error('Error playing sound:', e);
    }

    // 3. Flash title
    let originalTitle = document.title;
    let flashCount = 0;
    const flashInterval = setInterval(() => {
        if (flashCount >= 6) {
            document.title = originalTitle;
            clearInterval(flashInterval);
            return;
        }
        document.title = flashCount % 2 === 0 ? '💬 New Message!' : originalTitle;
        flashCount++;
    }, 1000);
    console.log('Title flashing started');
}

// Request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    console.log('notify.js loaded');
    if ("Notification" in window) {
        console.log('Initial notification permission:', Notification.permission);
        if (Notification.permission === "default") {
            console.log('Will request permission in 3 seconds...');
            setTimeout(() => {
                Notification.requestPermission().then(function (permission) {
                    console.log('Permission request result:', permission);
                });
            }, 3000);
        }
    }
});

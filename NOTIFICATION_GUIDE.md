# How to Add Browser Notifications to Your Flask Blood Bank App

## Quick Solution (Copy-Paste)

### Step 1: Open `templates/base.html`

Find this section (around line 200-202):
```html
<!-- Toastr JS (must be after jQuery) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
</head>
```

### Step 2: Replace it with this:
```html
<!-- Toastr JS (must be after jQuery) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
<!-- Browser Notification Setup -->
<script>
    // Request notification permission on page load
    document.addEventListener('DOMContentLoaded', function() {
        if ("Notification" in window && Notification.permission === "default") {
            setTimeout(() => {
                Notification.requestPermission();
            }, 3000); // Ask after 3 seconds
        }
    });
</script>
</head>
```

### Step 3: Update the `receive_message` handler in `templates/dashboard/donor.html`

Find this code (around line 295-310):
```javascript
socket.on('receive_message', function(data) {
    console.log('Received message:', data);
    if (myId == data.receiver_id && myType == data.receiver_type) {
        if (typeof toastr !== 'undefined') {
            toastr.options = {
                "closeButton": true,
                "debug": false,
                "positionClass": "toast-top-center",
                "timeOut": "5000"
            };
            toastr.info('New message from ' + data.sender_name + ': ' + data.message);
        }
    }
    // ... rest of code
});
```

### Step 4: Replace with this enhanced version:
```javascript
socket.on('receive_message', function(data) {
    console.log('Received message:', data);
    
    // Only show notification if the current user is the recipient
    if (myId == data.receiver_id && myType == data.receiver_type) {
        
        // 1. Show browser notification (desktop/mobile)
        if ("Notification" in window && Notification.permission === "granted") {
            const notification = new Notification('💬 ' + data.sender_name, {
                body: data.message,
                icon: '/static/images/logo.png',
                badge: '/static/images/badge.png',
                tag: 'message-' + data.sender_id,
                requireInteraction: false
            });
            
            // Auto-close after 10 seconds
            setTimeout(() => notification.close(), 10000);
            
            // Handle click
            notification.onclick = function() {
                window.focus();
                notification.close();
            };
        }
        
        // 2. Play sound alert
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
        } catch(e) {
            console.log('Audio not available');
        }
        
        // 3. Show toastr notification (in-app)
        if (typeof toastr !== 'undefined') {
            toastr.options = {
                "closeButton": true,
                "progressBar": true,
                "positionClass": "toast-top-right",
                "timeOut": "5000"
            };
            toastr.info(data.message, '💬 ' + data.sender_name);
        }
        
        // 4. Flash page title
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
    }
    
    // Add message to chat box (existing code)
    let chatBox = document.getElementById('chatMessages');
    let isMine = (data.sender_id == myId && data.sender_type == myType);
    let align = isMine ? 'text-right' : 'text-left';
    let color = isMine ? 'bg-red-100' : 'bg-gray-200';
    chatBox.innerHTML += `<div class="my-1 ${align}"><span class="inline-block ${color} px-2 py-1 rounded">${data.message}</span><br><span class="text-xs text-gray-400">${data.timestamp}</span></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
});
```

### Step 5: Do the same for `templates/dashboard/patient_landing.html`

Apply the same changes to the `receive_message` handler in the patient dashboard.

## How It Works

1. **Permission Request**: When users first visit, they'll be asked to allow notifications after 3 seconds
2. **Desktop Notifications**: Shows OS-level notifications (Windows/Mac/Linux notification center)
3. **Sound Alert**: Plays a beep sound when message arrives
4. **Toast Notification**: Shows in-app notification (toastr)
5. **Title Flash**: Page title flashes to grab attention

## Testing

1. Open your app in two different browsers (or incognito mode)
2. Login as donor in one, patient in another
3. Send a message
4. You should see:
   - Desktop notification popup
   - Hear a beep sound
   - See toast message in app
   - Page title flashing

## Troubleshooting

**No notifications showing?**
- Check if you clicked "Allow" when browser asked for permission
- Check browser settings: Settings → Privacy → Notifications
- Make sure you're testing with HTTPS (or localhost)

**No sound?**
- Some browsers block auto-play audio
- User must interact with page first (click something)

**Mobile notifications not working?**
- Mobile browser notifications work differently
- For full mobile push notifications, you need Firebase Cloud Messaging (FCM)
- Current solution works for mobile browsers when app is open

## For Production (HTTPS Required)

Browser notifications require either:
- `localhost` (for development) ✅
- `https://` (for production) ✅
- `http://` will NOT work in production ❌

Make sure your production server uses HTTPS!

# SIMPLE IMPLEMENTATION GUIDE - Browser Notifications

## Step 1: Add this ONE line to templates/base.html

Find line 201 (after toastr.js) and add:

```html
<script src="{{ url_for('static', filename='js/notify.js') }}"></script>
```

So it looks like:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
<script src="{{ url_for('static', filename='js/notify.js') }}"></script>
</head>
```

## Step 2: Update donor dashboard (templates/dashboard/donor.html)

Find the `socket.on('receive_message'` section (around line 295) and add this ONE line:

```javascript
socket.on('receive_message', function(data) {
    console.log('Received message:', data);
    
    if (myId == data.receiver_id && myType == data.receiver_type) {
        // ADD THIS LINE:
        showNotification(data.sender_name, data.message);
        
        // Keep existing toastr code:
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
    
    // ... rest of existing code
});
```

## Step 3: Do the same for patient dashboard (templates/dashboard/patient_landing.html)

Add the same `showNotification(data.sender_name, data.message);` line in the patient's receive_message handler.

## That's It!

Now when users receive messages:
✅ Desktop notification will appear
✅ Sound will play
✅ Page title will flash
✅ Toastr notification still works

## Test It

1. Open app in two browsers
2. Login as donor in one, patient in another
3. Send a message
4. Click "Allow" when browser asks for notification permission
5. You should see desktop notification + hear sound!

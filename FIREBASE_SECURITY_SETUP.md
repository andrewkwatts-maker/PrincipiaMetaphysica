# Firebase Security Configuration

## DDoS Protection and Rate Limiting

### 1. Enable App Check (Recommended)

App Check provides attestation that requests come from legitimate sources.

1. Go to Firebase Console > App Check
2. Click "Register" for your web app
3. Choose reCAPTCHA Enterprise (free tier available)
4. Add the reCAPTCHA site key to your app

```javascript
// In firebase-config.js
import { initializeAppCheck, ReCaptchaEnterpriseProvider } from "firebase/app-check";

const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaEnterpriseProvider('YOUR_RECAPTCHA_SITE_KEY'),
  isTokenAutoRefreshEnabled: true
});
```

### 2. Deploy Firestore Security Rules

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize (select Firestore)
firebase init firestore

# Deploy rules
firebase deploy --only firestore:rules
```

### 3. Enable Budget Alerts

1. Go to Firebase Console > Usage and billing
2. Set up budget alerts (e.g., warn at $10, $25, $50)
3. Set hard spending limit if available

### 4. Rate Limiting with Cloud Functions (Advanced)

For stricter rate limiting, deploy a Cloud Function:

```javascript
// functions/index.js
const functions = require('firebase-functions');
const admin = require('firebase-admin');

// Track request counts per IP
exports.rateLimit = functions.https.onRequest(async (req, res) => {
  const ip = req.ip;
  const db = admin.firestore();
  const rateRef = db.collection('rate_limits').doc(ip);
  
  const rateDoc = await rateRef.get();
  const now = Date.now();
  
  if (rateDoc.exists) {
    const data = rateDoc.data();
    const windowStart = data.windowStart || 0;
    const count = data.count || 0;
    
    // 100 requests per minute limit
    if (now - windowStart < 60000 && count >= 100) {
      res.status(429).send('Rate limit exceeded');
      return;
    }
    
    if (now - windowStart >= 60000) {
      await rateRef.set({ windowStart: now, count: 1 });
    } else {
      await rateRef.update({ count: admin.firestore.FieldValue.increment(1) });
    }
  } else {
    await rateRef.set({ windowStart: now, count: 1 });
  }
  
  res.status(200).send('OK');
});
```

### 5. Firestore Usage Limits

Current Firestore free tier limits:
- 50,000 reads/day
- 20,000 writes/day
- 20,000 deletes/day
- 1 GiB storage

With our caching strategy:
- Each user hits Firebase ~once per hour (hourly cache invalidation)
- localStorage caching reduces repeated reads
- Read-only access (no writes from client)

### 6. Monitoring

1. Go to Firebase Console > Firestore > Usage
2. Monitor daily read counts
3. Set up alerts if reads exceed thresholds

## Cache Strategy Summary

| Cache Level | TTL | Purpose |
|-------------|-----|---------|
| Memory cache | 5 min | Reduce Firebase calls during session |
| localStorage | 1 hour | Reduce Firebase calls across page loads |
| Version check | On load | Invalidate when new version uploaded |

## Emergency Disable

If under attack, you can temporarily disable the site:

1. Go to Firebase Console > Firestore > Rules
2. Replace rules with:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```
3. Click "Publish"

This blocks ALL access until you restore the normal rules.

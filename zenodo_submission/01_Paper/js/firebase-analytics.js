/**
 * Firebase Analytics and User Tracking Module
 *
 * Tracks user login events, page views, and session data in Firestore.
 * Uses the free tier without compromising data security.
 *
 * Collections:
 * - user_sessions: Login events with timestamps
 * - page_views: Page view events with user, page, timestamp
 *
 * All reads are authenticated - tracking happens on authenticated reads only.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { getFirestore, collection, addDoc, doc, setDoc, getDoc, serverTimestamp, query, where, orderBy, limit, getDocs } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js";
import { app } from './firebase-config.js';

const db = getFirestore(app);

/**
 * Track user login event
 * Called when user successfully authenticates
 */
export async function trackUserLogin(user) {
  if (!user) return;

  try {
    // Create/update user profile
    const userRef = doc(db, 'users', user.uid);
    await setDoc(userRef, {
      email: user.email,
      displayName: user.displayName || '',
      photoURL: user.photoURL || '',
      lastLogin: serverTimestamp(),
      loginCount: (await getLoginCount(user.uid)) + 1
    }, { merge: true });

    // Log login event
    await addDoc(collection(db, 'user_sessions'), {
      userId: user.uid,
      email: user.email,
      action: 'login',
      timestamp: serverTimestamp(),
      userAgent: navigator.userAgent,
      screenWidth: window.innerWidth,
      screenHeight: window.innerHeight
    });

    console.log('[Analytics] Login tracked for:', user.email);
  } catch (error) {
    console.error('[Analytics] Failed to track login:', error);
  }
}

/**
 * Get login count for a user
 */
async function getLoginCount(userId) {
  try {
    const userRef = doc(db, 'users', userId);
    const userDoc = await getDoc(userRef);
    if (userDoc.exists()) {
      return userDoc.data().loginCount || 0;
    }
  } catch (error) {
    console.error('[Analytics] Failed to get login count:', error);
  }
  return 0;
}

/**
 * Track page view event
 * Called when a page is loaded and data is ready
 */
export async function trackPageView(user, pageId) {
  if (!user || !pageId) return;

  try {
    await addDoc(collection(db, 'page_views'), {
      userId: user.uid,
      email: user.email,
      pageId: pageId,
      pageUrl: window.location.href,
      pageTitle: document.title,
      timestamp: serverTimestamp(),
      referrer: document.referrer || null,
      sessionId: getSessionId()
    });

    console.log('[Analytics] Page view tracked:', pageId);
  } catch (error) {
    console.error('[Analytics] Failed to track page view:', error);
  }
}

/**
 * Track user logout event
 */
export async function trackUserLogout(user) {
  if (!user) return;

  try {
    await addDoc(collection(db, 'user_sessions'), {
      userId: user.uid,
      email: user.email,
      action: 'logout',
      timestamp: serverTimestamp()
    });

    console.log('[Analytics] Logout tracked for:', user.email);
  } catch (error) {
    console.error('[Analytics] Failed to track logout:', error);
  }
}

/**
 * Get or create session ID for this browser session
 */
function getSessionId() {
  let sessionId = sessionStorage.getItem('pm_session_id');
  if (!sessionId) {
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('pm_session_id', sessionId);
  }
  return sessionId;
}

/**
 * Get recent page views for admin dashboard (optional)
 * Only callable by authenticated users
 */
export async function getRecentPageViews(limitCount = 50) {
  try {
    const q = query(
      collection(db, 'page_views'),
      orderBy('timestamp', 'desc'),
      limit(limitCount)
    );
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('[Analytics] Failed to get recent page views:', error);
    return [];
  }
}

/**
 * Get user's own page view history
 */
export async function getUserPageViews(userId, limitCount = 20) {
  try {
    const q = query(
      collection(db, 'page_views'),
      where('userId', '==', userId),
      orderBy('timestamp', 'desc'),
      limit(limitCount)
    );
    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error('[Analytics] Failed to get user page views:', error);
    return [];
  }
}

// Export for use in other modules
export default {
  trackUserLogin,
  trackUserLogout,
  trackPageView,
  getRecentPageViews,
  getUserPageViews
};

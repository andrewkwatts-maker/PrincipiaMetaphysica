/**
 * Firebase Authentication Module for Principia Metaphysica
 *
 * Handles Google authentication, user session management,
 * and auth state changes across the application.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

import { auth, googleProvider } from './firebase-config.js';
import {
  signInWithPopup,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  setPersistence,
  browserLocalPersistence
} from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-auth.js';

// Auth state callbacks registry
const authCallbacks = [];

// Current user reference
let currentUser = null;

// Flag to track if auth has initialized (first state received)
let authInitialized = false;

/**
 * Initialize authentication with persistence
 * Sets up local persistence so users stay logged in across browser sessions
 */
export async function initAuth() {
  try {
    await setPersistence(auth, browserLocalPersistence);
    console.log('[PM Auth] Persistence set to local storage');
  } catch (error) {
    console.error('[PM Auth] Error setting persistence:', error);
  }

  // Set up auth state listener
  onAuthStateChanged(auth, (user) => {
    currentUser = user;
    authInitialized = true;

    if (user) {
      console.log('[PM Auth] User signed in:', user.email);
    } else {
      console.log('[PM Auth] User signed out');
    }

    // Notify all registered callbacks immediately
    authCallbacks.forEach(callback => {
      try {
        callback(user);
      } catch (error) {
        console.error('[PM Auth] Error in auth callback:', error);
      }
    });
  });
}

/**
 * Sign in with Google popup
 * @returns {Promise<User|null>} The signed-in user or null on failure
 */
export async function signInWithGoogle() {
  try {
    console.log('[PM Auth] Initiating Google sign-in...');
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;

    console.log('[PM Auth] Successfully signed in:', user.email);

    return user;
  } catch (error) {
    console.error('[PM Auth] Sign-in error:', error.code, error.message);

    // Handle specific error cases
    switch (error.code) {
      case 'auth/popup-closed-by-user':
        console.log('[PM Auth] Sign-in cancelled by user');
        break;
      case 'auth/popup-blocked':
        alert('Pop-up blocked by browser. Please allow pop-ups for this site.');
        break;
      case 'auth/cancelled-popup-request':
        // Multiple popups opened, ignore
        break;
      default:
        alert('Sign-in failed: ' + error.message);
    }

    return null;
  }
}

/**
 * Sign out the current user
 * @returns {Promise<boolean>} True if sign-out successful
 */
export async function signOutUser() {
  try {
    await firebaseSignOut(auth);
    console.log('[PM Auth] User signed out successfully');
    return true;
  } catch (error) {
    console.error('[PM Auth] Sign-out error:', error);
    return false;
  }
}

/**
 * Register a callback for auth state changes
 * @param {Function} callback - Function to call with user object (or null)
 * @returns {Function} Unsubscribe function
 */
export function onAuthReady(callback) {
  authCallbacks.push(callback);

  // If auth is already initialized, call immediately with current state
  // Note: auth.currentUser can be null (not logged in) or a user object
  // We check if Firebase has finished initializing by seeing if we've received
  // any auth state (currentUser will be set after first onAuthStateChanged fires)
  if (authInitialized) {
    callback(auth.currentUser);
  }

  // Return unsubscribe function
  return () => {
    const index = authCallbacks.indexOf(callback);
    if (index > -1) {
      authCallbacks.splice(index, 1);
    }
  };
}

/**
 * Get the currently signed-in user
 * @returns {User|null} Current user or null if not signed in
 */
export function getCurrentUser() {
  return auth.currentUser;
}

/**
 * Check if a user is currently authenticated
 * @returns {boolean} True if user is signed in
 */
export function isAuthenticated() {
  return auth.currentUser !== null;
}

/**
 * Get user display information
 * @returns {Object|null} User info object or null
 */
export function getUserInfo() {
  const user = auth.currentUser;
  if (!user) return null;

  return {
    uid: user.uid,
    email: user.email,
    displayName: user.displayName,
    photoURL: user.photoURL,
    emailVerified: user.emailVerified
  };
}

// Initialize auth on module load
initAuth();

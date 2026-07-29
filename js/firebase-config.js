/**
 * Firebase Configuration for Principia Metaphysica
 *
 * Central Firebase initialization module using ES modules with CDN imports.
 * All Firebase services are initialized here and exported for use across the application.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

// Firebase SDK imports from CDN (v12.6.0)
import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-app.js';
import { getAuth, GoogleAuthProvider } from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-firestore.js';
import { getAnalytics } from 'https://www.gstatic.com/firebasejs/12.6.0/firebase-analytics.js';

/**
 * Firebase configuration object
 * Project: principia-metaphysica
 */
const firebaseConfig = {
  apiKey: "AIzaSyBfOD3iFdVh0xwG-rDocaRqNte_YxDEVDk",
  authDomain: "principia-metaphysica.firebaseapp.com",
  projectId: "principia-metaphysica",
  storageBucket: "principia-metaphysica.firebasestorage.app",
  messagingSenderId: "842796046956",
  appId: "1:842796046956:web:53828bea0f855de6479649",
  measurementId: "G-ZE4G7BZY79"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
const auth = getAuth(app);
const db = getFirestore(app);
const analytics = getAnalytics(app);

// Configure Google Auth Provider
const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'  // Always show account selector
});

// Export initialized services
export { app, auth, db, analytics, googleProvider, firebaseConfig };

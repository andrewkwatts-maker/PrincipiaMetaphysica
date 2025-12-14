/**
 * validation-utils.js - Utility functions for content validation
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

/**
 * Validates and returns the input string
 * @param {string} input - Input string to validate
 * @returns {string} - The validated input string, or ERROR:: code for specific issues
 */
export function IsValid(input) {
  if (input === null) {
    return "ERROR::NULL";
  }
  if (input === undefined) {
    return "ERROR::UNDEFINED";
  }
  if (typeof input !== 'string') {
    return "ERROR::NOT_STRING";
  }
  if (input === '') {
    return "ERROR::EMPTY_STRING";
  }
  if (input.trim() === '') {
    return "ERROR::WHITESPACE_ONLY";
  }
  return input;
}

/**
 * Check if a value is defined and not empty
 * @param {*} value - Value to check
 * @returns {boolean} - True if value is valid
 */
export function isDefined(value) {
  return value !== undefined && value !== null && value !== '';
}

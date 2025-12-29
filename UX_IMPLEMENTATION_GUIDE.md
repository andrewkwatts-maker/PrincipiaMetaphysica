# UX Implementation Guide

## Quick Start

The UX consistency enhancements are now applied across the entire website. Here's how to use them:

### 1. CSS Files (Already Included)

All pages now automatically include:
```html
<link rel="stylesheet" href="../css/pm-common.css">
<link rel="stylesheet" href="../css/pm-header.css">
<link rel="stylesheet" href="../css/pm-ux-consistency.css">
<link rel="stylesheet" href="../css/mobile-responsive.css">
```

### 2. JavaScript Component (Optional)

Add before closing `</body>` for loading states:
```html
<script src="../js/pm-loading-states.js"></script>
```

## Using Loading States

### Show Loading Spinner

```javascript
// Simple loading spinner
PMLoadingStates.showLoading('#container', {
    message: 'Loading sections...',
    size: 'medium' // small, medium, large
});

// Hide when done
PMLoadingStates.hideLoading('#container');
```

### Show Skeleton Loader

```javascript
// While fetching data
PMLoadingStates.showSkeleton('#card-grid', {
    type: 'card', // card, text, list
    count: 6
});
```

### Show Error Message

```javascript
try {
    const data = await fetchData();
} catch (error) {
    PMLoadingStates.showError('#container', {
        title: 'Failed to Load',
        message: 'Could not fetch data. Please check your connection.',
        retry: 'fetchData()',
        retryText: 'Try Again',
        icon: '⚠️'
    });
}
```

### Show Empty State

```javascript
if (results.length === 0) {
    PMLoadingStates.showEmpty('#results', {
        title: 'No Results Found',
        message: 'Try adjusting your search criteria.',
        action: 'resetFilters()',
        actionText: 'Clear Filters',
        icon: '📭'
    });
}
```

### Show Toast Notification

```javascript
// Success
PMLoadingStates.showToast('Changes saved successfully!', {
    type: 'success',
    duration: 3000,
    position: 'bottom-right'
});

// Error
PMLoadingStates.showToast('Failed to save changes', {
    type: 'error',
    duration: 5000
});

// Info
PMLoadingStates.showToast('Processing your request...', {
    type: 'info',
    duration: 2000
});

// Warning
PMLoadingStates.showToast('This action cannot be undone', {
    type: 'warning',
    duration: 4000
});
```

### Field Validation

```javascript
// Show error
PMLoadingStates.showFieldError('#email', 'Please enter a valid email address');

// Hide error
PMLoadingStates.hideFieldError('#email');
```

## Using CSS Components

### Buttons

```html
<!-- Primary button (default) -->
<button class="btn btn-primary">Save Changes</button>

<!-- Secondary button -->
<button class="btn btn-secondary">Cancel</button>

<!-- Outline button -->
<button class="btn btn-outline">Learn More</button>

<!-- Ghost button -->
<button class="btn btn-ghost">Dismiss</button>

<!-- Small button -->
<button class="btn btn-sm">Small</button>

<!-- Large button -->
<button class="btn btn-lg">Large Action</button>

<!-- Full width button -->
<button class="btn btn-block">Full Width</button>

<!-- Loading state -->
<button class="btn loading">Processing...</button>

<!-- Disabled -->
<button class="btn" disabled>Disabled</button>
```

### Form Controls

```html
<!-- Text input -->
<input type="text" placeholder="Enter your name">

<!-- Input with icon -->
<div class="input-group">
    <span class="input-icon">🔍</span>
    <input type="search" placeholder="Search...">
</div>

<!-- Select dropdown -->
<select>
    <option>Option 1</option>
    <option>Option 2</option>
    <option>Option 3</option>
</select>

<!-- Textarea -->
<textarea placeholder="Enter your message"></textarea>
```

### Dropdowns

```html
<!-- Custom dropdown -->
<div class="dropdown">
    <button class="dropdown-toggle">
        Select Option
        <span>▼</span>
    </button>
    <div class="dropdown-menu">
        <a href="#" class="dropdown-item">Option 1</a>
        <a href="#" class="dropdown-item">Option 2</a>
        <div class="dropdown-divider"></div>
        <a href="#" class="dropdown-item">Option 3</a>
    </div>
</div>
```

### Cards

```html
<!-- Card with hover effect -->
<div class="card">
    <h3>Card Title</h3>
    <p class="description">Card description goes here.</p>
</div>

<!-- Info card -->
<div class="info-card">
    <h4>Information</h4>
    <p>Some helpful information.</p>
</div>
```

### Panels

```html
<!-- Content panel -->
<div class="panel">
    <h2>Panel Title</h2>
    <p>Panel content with dark background.</p>
</div>

<!-- Section panel -->
<div class="section-panel">
    <h3>Section</h3>
    <p>Section content.</p>
</div>
```

## Utility Classes

### Display

```html
<div class="hidden">Hidden element</div>
<div class="block">Block element</div>
<div class="flex">Flex container</div>
<div class="inline-flex">Inline flex</div>
```

### Spacing

```html
<div class="m-0">No margin</div>
<div class="mt-1">Margin top 1rem</div>
<div class="mb-1">Margin bottom 1rem</div>
<div class="p-0">No padding</div>
<div class="p-1">Padding 1rem</div>
```

### Text Alignment

```html
<p class="text-center">Centered text</p>
<p class="text-left">Left aligned</p>
<p class="text-right">Right aligned</p>
```

### Colors

```html
<p class="text-primary">Primary color</p>
<p class="text-secondary">Secondary color</p>
<p class="text-muted">Muted color</p>
<p class="text-accent">Accent color</p>
<p class="text-success">Success color</p>
<p class="text-warning">Warning color</p>
<p class="text-error">Error color</p>
```

### Backgrounds

```html
<div class="bg-elevated">Elevated background</div>
<div class="bg-panel">Panel background</div>
<div class="bg-card">Card background</div>
```

### Borders

```html
<div class="border">With border</div>
<div class="border-0">No border</div>
<div class="rounded">Rounded corners</div>
<div class="rounded-lg">Large rounded corners</div>
```

### Z-index

```html
<div class="z-base">Base layer</div>
<div class="z-dropdown">Dropdown layer</div>
<div class="z-modal">Modal layer</div>
<div class="z-tooltip">Tooltip layer</div>
```

## Real-World Examples

### Example 1: Loading Data with Error Handling

```javascript
async function loadSections() {
    const container = document.getElementById('sections-container');

    // Show loading
    PMLoadingStates.showLoading(container, {
        message: 'Loading sections...',
        size: 'large'
    });

    try {
        const response = await fetch('/api/sections');
        if (!response.ok) throw new Error('Failed to fetch');

        const sections = await response.json();

        if (sections.length === 0) {
            // Show empty state
            PMLoadingStates.showEmpty(container, {
                title: 'No Sections Found',
                message: 'There are no sections available yet.',
                action: 'createSection()',
                actionText: 'Create New Section',
                icon: '📄'
            });
        } else {
            // Render sections
            container.innerHTML = sections.map(s => `
                <div class="card">
                    <h3>${s.title}</h3>
                    <p>${s.description}</p>
                </div>
            `).join('');

            // Show success toast
            PMLoadingStates.showToast(`Loaded ${sections.length} sections`, {
                type: 'success',
                duration: 2000
            });
        }
    } catch (error) {
        // Show error
        PMLoadingStates.showError(container, {
            title: 'Loading Failed',
            message: error.message,
            retry: 'loadSections()',
            retryText: 'Retry'
        });
    }
}
```

### Example 2: Form Validation

```javascript
function validateForm() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');

    let isValid = true;

    // Clear previous errors
    PMLoadingStates.hideFieldError(email);
    PMLoadingStates.hideFieldError(password);

    // Validate email
    if (!email.value.includes('@')) {
        PMLoadingStates.showFieldError(email, 'Please enter a valid email address');
        isValid = false;
    }

    // Validate password
    if (password.value.length < 8) {
        PMLoadingStates.showFieldError(password, 'Password must be at least 8 characters');
        isValid = false;
    }

    return isValid;
}

async function submitForm() {
    if (!validateForm()) return;

    const submitBtn = document.getElementById('submit-btn');
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
        await saveData();

        PMLoadingStates.showToast('Form submitted successfully!', {
            type: 'success'
        });
    } catch (error) {
        PMLoadingStates.showToast('Failed to submit form', {
            type: 'error',
            duration: 5000
        });
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}
```

### Example 3: Search with Skeleton Loader

```javascript
async function searchFormulas(query) {
    const resultsContainer = document.getElementById('results');

    // Show skeleton while searching
    PMLoadingStates.showSkeleton(resultsContainer, {
        type: 'card',
        count: 5
    });

    try {
        const results = await fetch(`/api/search?q=${query}`).then(r => r.json());

        if (results.length === 0) {
            PMLoadingStates.showEmpty(resultsContainer, {
                title: 'No Formulas Found',
                message: `No results for "${query}"`,
                action: 'clearSearch()',
                actionText: 'Clear Search',
                icon: '🔍'
            });
        } else {
            // Render results
            resultsContainer.innerHTML = results.map(formula => `
                <div class="formula-card card">
                    <h4>${formula.name}</h4>
                    <div class="formula-latex">${formula.latex}</div>
                </div>
            `).join('');
        }
    } catch (error) {
        PMLoadingStates.showError(resultsContainer, {
            title: 'Search Failed',
            message: 'Could not complete search. Please try again.',
            retry: `searchFormulas('${query}')`,
            retryText: 'Retry Search'
        });
    }
}
```

## Best Practices

### 1. Always Show Loading States
```javascript
// ❌ Bad - No loading feedback
async function loadData() {
    const data = await fetch('/api/data').then(r => r.json());
    renderData(data);
}

// ✅ Good - Clear loading feedback
async function loadData() {
    PMLoadingStates.showLoading('#container');
    try {
        const data = await fetch('/api/data').then(r => r.json());
        renderData(data);
    } finally {
        PMLoadingStates.hideLoading('#container');
    }
}
```

### 2. Handle Empty States
```javascript
// ❌ Bad - Blank screen
function renderResults(results) {
    container.innerHTML = results.map(r => `...`).join('');
}

// ✅ Good - Helpful empty state
function renderResults(results) {
    if (results.length === 0) {
        PMLoadingStates.showEmpty(container, {
            title: 'No Results',
            message: 'Try different search terms'
        });
    } else {
        container.innerHTML = results.map(r => `...`).join('');
    }
}
```

### 3. Provide Error Context
```javascript
// ❌ Bad - Generic error
catch (error) {
    PMLoadingStates.showError(container);
}

// ✅ Good - Specific error with action
catch (error) {
    PMLoadingStates.showError(container, {
        title: 'Network Error',
        message: 'Could not connect to server. Check your internet connection.',
        retry: 'retryOperation()',
        retryText: 'Retry'
    });
}
```

### 4. Use Appropriate Toast Duration
```javascript
// ❌ Bad - Too short for errors
PMLoadingStates.showToast('Error occurred', { type: 'error', duration: 1000 });

// ✅ Good - Longer duration for important messages
PMLoadingStates.showToast('Error occurred', { type: 'error', duration: 5000 });

// ✅ Good - Short duration for success
PMLoadingStates.showToast('Saved!', { type: 'success', duration: 2000 });
```

### 5. Skeleton vs Spinner
```javascript
// Use skeleton for lists/grids
PMLoadingStates.showSkeleton('#card-grid', { type: 'card', count: 6 });

// Use spinner for single operations
PMLoadingStates.showLoading('#form-container', { message: 'Submitting...' });
```

## Accessibility Considerations

All components are built with accessibility in mind:

1. **Keyboard Navigation**: All interactive elements are keyboard accessible
2. **Focus Indicators**: Visible focus states for keyboard users
3. **ARIA Labels**: Screen reader support
4. **Color Contrast**: WCAG AA compliant
5. **Reduced Motion**: Respects user preferences

```css
/* Automatic accessibility features */
*:focus-visible {
    outline: 2px solid var(--accent-primary);
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Troubleshooting

### Loading state doesn't disappear
```javascript
// Make sure to always hide in finally block
try {
    await operation();
} finally {
    PMLoadingStates.hideLoading('#container'); // Always runs
}
```

### Styles not applying
Check CSS include order:
```html
<!-- Correct order -->
<link rel="stylesheet" href="pm-common.css">
<link rel="stylesheet" href="pm-header.css">
<link rel="stylesheet" href="pm-ux-consistency.css"> <!-- Must come after common -->
```

### Dropdowns not working
Make sure to activate on click:
```javascript
dropdown.addEventListener('click', () => {
    dropdown.classList.toggle('active');
});
```

### Toast notifications stacking incorrectly
Container is auto-created. If issues, check:
```javascript
// Container should exist after first toast
const container = document.getElementById('pm-toast-container');
console.log(container); // Should exist
```

## Support

For issues or questions:
1. Check console for errors
2. Verify CSS files are loaded
3. Check browser compatibility
4. Review this guide for correct usage

## Version History

- **v1.0** (2025-12-29): Initial release
  - Dark theme consistency
  - Loading/error/empty states
  - Form controls and dropdowns
  - Button standardization
  - Accessibility improvements

# Tailwind CSS @theme Directive Reference

## Basic Structure

```css
@import "tailwindcss";

@theme {
  /* Your custom theme tokens */
}
```

## Color Tokens

### Custom Colors

```css
@theme {
  /* Single colors */
  --color-brand: oklch(0.6 0.15 250);
  --color-accent: oklch(0.7 0.2 150);

  /* Color scales */
  --color-primary-50: oklch(0.98 0.01 250);
  --color-primary-100: oklch(0.95 0.03 250);
  --color-primary-500: oklch(0.60 0.16 250);
  --color-primary-900: oklch(0.20 0.05 250);

  /* Semantic colors */
  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.1 0 0);
  --color-muted: oklch(0.95 0 0);
  --color-muted-foreground: oklch(0.45 0 0);
  --color-border: oklch(0.9 0 0);
}
```

Usage:

```html
<div class="bg-brand text-primary-900 border-border">
  Custom colors
</div>
```

### Overriding Default Colors

```css
@theme {
  /* Replace the entire blue palette */
  --color-blue-50: oklch(0.97 0.02 240);
  --color-blue-100: oklch(0.93 0.04 240);
  --color-blue-500: oklch(0.55 0.18 240);
  --color-blue-900: oklch(0.25 0.10 240);
}
```

## Typography Tokens

### Fonts

```css
@theme {
  --font-sans: "Inter", system-ui, sans-serif;
  --font-serif: "Merriweather", Georgia, serif;
  --font-mono: "JetBrains Mono", monospace;
  --font-display: "Cal Sans", sans-serif;
}
```

```html
<h1 class="font-display">Display heading</h1>
<p class="font-sans">Body text</p>
<code class="font-mono">Code</code>
```

### Font Sizes

```css
@theme {
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* With line height */
  --text-hero: 4rem;
  --text-hero--line-height: 1.1;
  --text-hero--letter-spacing: -0.02em;
}
```

### Font Weights

```css
@theme {
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

## Spacing Tokens

```css
@theme {
  /* Add custom spacing values */
  --spacing-18: 4.5rem;
  --spacing-128: 32rem;
  --spacing-screen: 100vh;

  /* Named spacing */
  --spacing-gutter: 1.5rem;
  --spacing-section: 5rem;
}
```

```html
<div class="p-gutter my-section w-128">
  Custom spacing
</div>
```

## Sizing Tokens

```css
@theme {
  /* Custom widths */
  --width-prose: 65ch;
  --width-sidebar: 280px;
  --width-content: 1200px;

  /* Custom heights */
  --height-header: 64px;
  --height-footer: 120px;
}
```

## Border Radius

```css
@theme {
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Named radius */
  --radius-button: 0.5rem;
  --radius-card: 0.75rem;
  --radius-modal: 1rem;
}
```

## Shadows

```css
@theme {
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.07);
  --shadow-lg: 0 10px 15px oklch(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px oklch(0 0 0 / 0.15);

  /* Colored shadows */
  --shadow-primary: 0 4px 14px oklch(0.6 0.15 250 / 0.3);

  /* Inset shadows */
  --shadow-inner: inset 0 2px 4px oklch(0 0 0 / 0.06);
}
```

## Transitions

```css
@theme {
  /* Durations */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;

  /* Easings */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

## Animations

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.4s ease-out;
  --animate-scale-in: scale-in 0.2s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

## Breakpoints

```css
@theme {
  /* Override default breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;

  /* Add custom breakpoints */
  --breakpoint-3xl: 1920px;
  --breakpoint-4xl: 2560px;
}
```

## Z-Index Scale

```css
@theme {
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}
```

## Dark Mode Variants

```css
@theme {
  /* Light mode defaults */
  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.1 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.1 0 0);
  --color-border: oklch(0.9 0 0);

  /* Dark mode overrides */
  @variant dark {
    --color-background: oklch(0.1 0 0);
    --color-foreground: oklch(0.98 0 0);
    --color-card: oklch(0.15 0 0);
    --color-card-foreground: oklch(0.98 0 0);
    --color-border: oklch(0.25 0 0);
  }
}
```

## Complete Theme Example

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: oklch(0.6 0.15 250);
  --color-primary-foreground: oklch(0.98 0 0);
  --color-secondary: oklch(0.95 0.01 250);
  --color-secondary-foreground: oklch(0.2 0.05 250);
  --color-accent: oklch(0.7 0.2 150);
  --color-accent-foreground: oklch(0.15 0.05 150);

  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.1 0 0);
  --color-muted: oklch(0.95 0 0);
  --color-muted-foreground: oklch(0.45 0 0);
  --color-border: oklch(0.9 0 0);
  --color-input: oklch(0.9 0 0);
  --color-ring: oklch(0.6 0.15 250);

  --color-destructive: oklch(0.55 0.2 25);
  --color-destructive-foreground: oklch(0.98 0 0);

  /* Typography */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.1);

  /* Animations */
  --animate-accordion-down: accordion-down 0.2s ease-out;
  --animate-accordion-up: accordion-up 0.2s ease-out;

  /* Dark mode */
  @variant dark {
    --color-background: oklch(0.1 0 0);
    --color-foreground: oklch(0.98 0 0);
    --color-muted: oklch(0.2 0 0);
    --color-muted-foreground: oklch(0.65 0 0);
    --color-border: oklch(0.25 0 0);
    --color-input: oklch(0.25 0 0);
  }
}

@keyframes accordion-down {
  from { height: 0; }
  to { height: var(--radix-accordion-content-height); }
}

@keyframes accordion-up {
  from { height: var(--radix-accordion-content-height); }
  to { height: 0; }
}
```

## Extending vs Overriding

### Extending (Adding New)

```css
@theme {
  /* These ADD to existing utilities */
  --color-brand: oklch(0.6 0.15 250);
  --spacing-18: 4.5rem;
}
```

### Overriding (Replacing)

```css
@theme {
  /* This REPLACES the default blue-500 */
  --color-blue-500: oklch(0.55 0.2 240);
}
```

## Referencing Theme Values

Use CSS `var()` function:

```css
.custom-element {
  background: var(--color-primary);
  padding: var(--spacing-gutter);
  border-radius: var(--radius-lg);
}
```

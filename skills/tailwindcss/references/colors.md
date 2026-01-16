# Tailwind CSS OKLCH Colors Reference

## Understanding OKLCH

OKLCH is a perceptually uniform color space that provides:
- **Consistent perceived lightness** across hues
- **Predictable color manipulation**
- **P3 wide gamut support** on modern displays

Format: `oklch(lightness chroma hue)`

- **Lightness**: 0 (black) to 1 (white)
- **Chroma**: 0 (gray) to ~0.4 (most vivid)
- **Hue**: 0-360 degrees on the color wheel

## Hue Reference

| Color | Hue (degrees) |
|-------|--------------|
| Red | 25 |
| Orange | 50 |
| Yellow | 85 |
| Lime | 115 |
| Green | 145 |
| Teal | 175 |
| Cyan | 200 |
| Sky | 225 |
| Blue | 250 |
| Indigo | 275 |
| Purple | 300 |
| Pink | 350 |

## Creating Color Scales

### Lightness Progression

For a cohesive color scale, vary lightness while keeping chroma and hue consistent:

```css
@theme {
  /* Blue palette - consistent hue (250), varying lightness */
  --color-blue-50: oklch(0.97 0.02 250);   /* Very light */
  --color-blue-100: oklch(0.93 0.04 250);
  --color-blue-200: oklch(0.88 0.08 250);
  --color-blue-300: oklch(0.80 0.12 250);
  --color-blue-400: oklch(0.70 0.16 250);
  --color-blue-500: oklch(0.60 0.18 250);  /* Base */
  --color-blue-600: oklch(0.50 0.16 250);
  --color-blue-700: oklch(0.42 0.14 250);
  --color-blue-800: oklch(0.34 0.12 250);
  --color-blue-900: oklch(0.26 0.08 250);
  --color-blue-950: oklch(0.18 0.05 250);  /* Very dark */
}
```

### Lightness Guidelines

| Shade | Lightness Range | Use Case |
|-------|----------------|----------|
| 50 | 0.96-0.98 | Subtle backgrounds |
| 100 | 0.92-0.95 | Light backgrounds |
| 200 | 0.86-0.90 | Hover states (light) |
| 300 | 0.78-0.84 | Borders (light mode) |
| 400 | 0.68-0.75 | Muted text |
| 500 | 0.55-0.65 | Primary color |
| 600 | 0.48-0.55 | Hover states (dark bg) |
| 700 | 0.40-0.48 | Active states |
| 800 | 0.30-0.38 | Borders (dark mode) |
| 900 | 0.22-0.28 | Dark backgrounds |
| 950 | 0.12-0.18 | Very dark backgrounds |

## Chroma Guidelines

| Chroma | Effect |
|--------|--------|
| 0 | Pure grayscale |
| 0.01-0.03 | Subtle tint (backgrounds) |
| 0.05-0.10 | Muted colors |
| 0.12-0.18 | Balanced saturation |
| 0.20-0.30 | Vibrant colors |
| 0.30+ | Very vivid (may clip on sRGB) |

### Chroma Progression

Adjust chroma across the scale for natural appearance:

```css
@theme {
  /* Chroma peaks in mid-tones, reduces at extremes */
  --color-green-50: oklch(0.97 0.02 145);   /* Low chroma */
  --color-green-200: oklch(0.88 0.10 145);  /* Increasing */
  --color-green-500: oklch(0.60 0.18 145);  /* Peak chroma */
  --color-green-700: oklch(0.42 0.14 145);  /* Decreasing */
  --color-green-950: oklch(0.18 0.04 145);  /* Low chroma */
}
```

## Complete Color Palettes

### Primary (Blue)

```css
@theme {
  --color-primary-50: oklch(0.97 0.02 250);
  --color-primary-100: oklch(0.93 0.04 250);
  --color-primary-200: oklch(0.88 0.08 250);
  --color-primary-300: oklch(0.80 0.12 250);
  --color-primary-400: oklch(0.70 0.16 250);
  --color-primary-500: oklch(0.60 0.18 250);
  --color-primary-600: oklch(0.50 0.16 250);
  --color-primary-700: oklch(0.42 0.14 250);
  --color-primary-800: oklch(0.34 0.12 250);
  --color-primary-900: oklch(0.26 0.08 250);
  --color-primary-950: oklch(0.18 0.05 250);
}
```

### Neutral (Gray)

```css
@theme {
  --color-gray-50: oklch(0.98 0 0);
  --color-gray-100: oklch(0.95 0 0);
  --color-gray-200: oklch(0.90 0 0);
  --color-gray-300: oklch(0.82 0 0);
  --color-gray-400: oklch(0.65 0 0);
  --color-gray-500: oklch(0.50 0 0);
  --color-gray-600: oklch(0.40 0 0);
  --color-gray-700: oklch(0.32 0 0);
  --color-gray-800: oklch(0.24 0 0);
  --color-gray-900: oklch(0.16 0 0);
  --color-gray-950: oklch(0.10 0 0);
}
```

### Success (Green)

```css
@theme {
  --color-success-50: oklch(0.97 0.02 145);
  --color-success-500: oklch(0.65 0.18 145);
  --color-success-700: oklch(0.45 0.14 145);
}
```

### Warning (Amber)

```css
@theme {
  --color-warning-50: oklch(0.97 0.03 85);
  --color-warning-500: oklch(0.75 0.18 85);
  --color-warning-700: oklch(0.55 0.14 85);
}
```

### Error (Red)

```css
@theme {
  --color-error-50: oklch(0.97 0.02 25);
  --color-error-500: oklch(0.55 0.22 25);
  --color-error-700: oklch(0.40 0.18 25);
}
```

## Semantic Colors

```css
@theme {
  /* Backgrounds */
  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.09 0 0);

  /* Cards */
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.09 0 0);

  /* Muted/Secondary */
  --color-muted: oklch(0.96 0.005 250);
  --color-muted-foreground: oklch(0.45 0.01 250);

  /* Borders */
  --color-border: oklch(0.90 0.005 250);
  --color-input: oklch(0.90 0.005 250);

  /* Focus ring */
  --color-ring: oklch(0.60 0.18 250);

  /* Dark mode */
  @variant dark {
    --color-background: oklch(0.09 0 0);
    --color-foreground: oklch(0.98 0 0);
    --color-card: oklch(0.12 0 0);
    --color-card-foreground: oklch(0.98 0 0);
    --color-muted: oklch(0.18 0.005 250);
    --color-muted-foreground: oklch(0.65 0.01 250);
    --color-border: oklch(0.22 0.005 250);
    --color-input: oklch(0.22 0.005 250);
  }
}
```

## Color Manipulation

### Adjusting Lightness

```css
/* Hover state: slightly darker */
.btn {
  background: oklch(0.60 0.18 250);
}
.btn:hover {
  background: oklch(0.55 0.18 250); /* -0.05 lightness */
}
```

### Adjusting Opacity

```css
/* Semi-transparent */
--color-overlay: oklch(0.1 0 0 / 0.5);
--color-shadow: oklch(0 0 0 / 0.1);
```

### Creating Tints

```css
/* Add subtle color to neutrals */
--color-slate-50: oklch(0.98 0.005 250);  /* Slight blue tint */
--color-stone-50: oklch(0.98 0.005 50);   /* Slight warm tint */
```

## Accessibility Considerations

### Contrast Ratios

For WCAG 2.1 AA compliance:
- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio

Use lightness difference as a guide:
- **Minimum**: 0.45 lightness difference
- **Recommended**: 0.55+ lightness difference

```css
/* Good contrast example */
--color-text: oklch(0.15 0 0);       /* Dark text */
--color-background: oklch(0.98 0 0); /* Light background */
/* Difference: 0.83 - excellent contrast */
```

### Color Blindness

- Don't rely on color alone for meaning
- Use icons, patterns, or text labels
- Test with color blindness simulators

## Converting to OKLCH

### From Hex/RGB

Use online converters:
- oklch.com
- colorjs.io

### From HSL

OKLCH hue roughly equals HSL hue, but:
- Lightness is perceptually uniform (HSL is not)
- Chroma replaces saturation (different scale)

## Best Practices

1. **Start with one base hue** and create a full scale
2. **Keep chroma consistent** across similar shades
3. **Reduce chroma at extremes** (very light/dark)
4. **Test in both light and dark modes**
5. **Verify contrast ratios** for accessibility
6. **Use semantic names** for UI colors (background, foreground, etc.)

# shadcn/ui Theming Reference

## CSS Variables

shadcn/ui uses CSS variables for theming. Define them in your `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;

    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;

    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;

    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;

    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;

    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;

    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;

    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;

    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;

    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;

    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;

    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;

    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;

    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;

    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;

    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;

    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
  }
}
```

## Variable Reference

| Variable | Purpose |
|----------|---------|
| `--background` | Page background |
| `--foreground` | Page text color |
| `--card` | Card backgrounds |
| `--card-foreground` | Card text color |
| `--popover` | Popover/dropdown backgrounds |
| `--popover-foreground` | Popover text color |
| `--primary` | Primary button background |
| `--primary-foreground` | Primary button text |
| `--secondary` | Secondary button background |
| `--secondary-foreground` | Secondary button text |
| `--muted` | Muted backgrounds (e.g., disabled) |
| `--muted-foreground` | Muted text color |
| `--accent` | Accent backgrounds (e.g., hover) |
| `--accent-foreground` | Accent text color |
| `--destructive` | Destructive action color |
| `--destructive-foreground` | Destructive action text |
| `--border` | Border color |
| `--input` | Input border color |
| `--ring` | Focus ring color |
| `--radius` | Border radius base value |

## Using OKLCH Colors

Modern approach using OKLCH:

```css
@layer base {
  :root {
    /* Using OKLCH for better perceptual uniformity */
    --background: oklch(0.99 0 0);
    --foreground: oklch(0.09 0 0);

    --card: oklch(1 0 0);
    --card-foreground: oklch(0.09 0 0);

    --primary: oklch(0.6 0.15 250);
    --primary-foreground: oklch(0.98 0 0);

    --secondary: oklch(0.96 0.005 250);
    --secondary-foreground: oklch(0.2 0.05 250);

    --muted: oklch(0.96 0 0);
    --muted-foreground: oklch(0.45 0 0);

    --accent: oklch(0.96 0 0);
    --accent-foreground: oklch(0.2 0 0);

    --destructive: oklch(0.55 0.2 25);
    --destructive-foreground: oklch(0.98 0 0);

    --border: oklch(0.90 0 0);
    --input: oklch(0.90 0 0);
    --ring: oklch(0.6 0.15 250);

    --radius: 0.5rem;
  }

  .dark {
    --background: oklch(0.09 0 0);
    --foreground: oklch(0.98 0 0);

    --card: oklch(0.12 0 0);
    --card-foreground: oklch(0.98 0 0);

    --primary: oklch(0.98 0 0);
    --primary-foreground: oklch(0.2 0 0);

    --secondary: oklch(0.18 0.005 250);
    --secondary-foreground: oklch(0.98 0 0);

    --muted: oklch(0.18 0 0);
    --muted-foreground: oklch(0.65 0 0);

    --accent: oklch(0.18 0 0);
    --accent-foreground: oklch(0.98 0 0);

    --destructive: oklch(0.35 0.15 25);
    --destructive-foreground: oklch(0.98 0 0);

    --border: oklch(0.22 0 0);
    --input: oklch(0.22 0 0);
    --ring: oklch(0.85 0 0);
  }
}
```

## Custom Color Themes

### Brand Colors

```css
@layer base {
  :root {
    /* Custom brand primary */
    --primary: oklch(0.55 0.18 200);  /* Teal */
    --primary-foreground: oklch(0.98 0 0);

    /* Custom brand secondary */
    --secondary: oklch(0.95 0.02 200);
    --secondary-foreground: oklch(0.25 0.1 200);
  }
}
```

### Multiple Themes

```css
@layer base {
  /* Default theme */
  :root {
    --primary: oklch(0.6 0.15 250);  /* Blue */
  }

  /* Purple theme */
  .theme-purple {
    --primary: oklch(0.55 0.2 300);  /* Purple */
  }

  /* Green theme */
  .theme-green {
    --primary: oklch(0.6 0.18 145);  /* Green */
  }
}
```

```tsx
// Apply theme class to html element
<html className="theme-purple">
```

## Adding New Color Variables

### Extend the Theme

```css
@layer base {
  :root {
    /* Existing variables... */

    /* Custom additions */
    --success: oklch(0.65 0.18 145);
    --success-foreground: oklch(0.98 0 0);

    --warning: oklch(0.75 0.15 85);
    --warning-foreground: oklch(0.2 0.1 85);

    --info: oklch(0.6 0.12 225);
    --info-foreground: oklch(0.98 0 0);
  }

  .dark {
    --success: oklch(0.45 0.14 145);
    --success-foreground: oklch(0.98 0 0);

    --warning: oklch(0.55 0.12 85);
    --warning-foreground: oklch(0.98 0 0);

    --info: oklch(0.45 0.1 225);
    --info-foreground: oklch(0.98 0 0);
  }
}
```

### Use in Components

```tsx
// In your component
<div className="bg-success text-success-foreground">
  Success message
</div>

// Or in cn()
<Alert className={cn(
  "bg-[hsl(var(--success))]",
  "text-[hsl(var(--success-foreground))]"
)}>
  Success!
</Alert>
```

## Tailwind Config Integration

For Tailwind v4 with @theme:

```css
@import "tailwindcss";

@theme {
  /* Map CSS variables to Tailwind colors */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);

  /* Custom radius scale */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
}
```

## Chart Colors

For data visualization:

```css
@layer base {
  :root {
    --chart-1: oklch(0.6 0.18 200);
    --chart-2: oklch(0.65 0.15 145);
    --chart-3: oklch(0.7 0.15 85);
    --chart-4: oklch(0.55 0.2 300);
    --chart-5: oklch(0.6 0.18 25);
  }

  .dark {
    --chart-1: oklch(0.5 0.15 200);
    --chart-2: oklch(0.55 0.12 145);
    --chart-3: oklch(0.6 0.12 85);
    --chart-4: oklch(0.45 0.18 300);
    --chart-5: oklch(0.5 0.15 25);
  }
}
```

## Sidebar Colors

For sidebar components:

```css
@layer base {
  :root {
    --sidebar-background: oklch(0.98 0 0);
    --sidebar-foreground: oklch(0.2 0 0);
    --sidebar-primary: oklch(0.6 0.15 250);
    --sidebar-primary-foreground: oklch(0.98 0 0);
    --sidebar-accent: oklch(0.95 0 0);
    --sidebar-accent-foreground: oklch(0.2 0 0);
    --sidebar-border: oklch(0.9 0 0);
    --sidebar-ring: oklch(0.6 0.15 250);
  }

  .dark {
    --sidebar-background: oklch(0.12 0 0);
    --sidebar-foreground: oklch(0.95 0 0);
    --sidebar-primary: oklch(0.6 0.15 250);
    --sidebar-primary-foreground: oklch(0.98 0 0);
    --sidebar-accent: oklch(0.18 0 0);
    --sidebar-accent-foreground: oklch(0.95 0 0);
    --sidebar-border: oklch(0.22 0 0);
    --sidebar-ring: oklch(0.6 0.15 250);
  }
}
```

## Typography Customization

```css
@layer base {
  :root {
    --font-sans: "Inter", system-ui, sans-serif;
    --font-mono: "JetBrains Mono", monospace;
  }

  body {
    font-family: var(--font-sans);
    font-feature-settings: "rlig" 1, "calt" 1;
  }

  code {
    font-family: var(--font-mono);
  }
}
```

## Best Practices

1. **Use semantic variables** - Name by purpose, not color (e.g., `--primary` not `--blue`)
2. **Maintain contrast** - Ensure foreground/background pairs have sufficient contrast
3. **Test both modes** - Always verify light and dark mode appearance
4. **Use OKLCH** - For perceptually uniform color manipulation
5. **Document custom variables** - Add comments for non-standard additions

# PageLayout Module

**Path:** `frontend/src/components/ui/PageLayout.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/PageLayout.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `clsx` | `clsx` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ActionGroup`, `FormGrid`, `InlineField`, `MetricGrid`, `PageActions`, `PageHeader`, `PageLayout`, `TableFrame`, `Toolbar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PageLayoutProps](../entities/PageLayoutProps.md) | Type alias | 4 | <pre><code>&#123;&#10;    children&#58; ReactNode&#59;&#10;    variant&#63;&#58; &#39;default&#39; &#124; &#39;wide&#39; &#124; &#39;workbench&#39;&#59;&#10;    className&#63;&#58; string&#59;&#10;    testId&#63;&#58; string&#59;&#10;&#125;</code></pre> | — |
| [PageHeaderProps](../entities/PageHeaderProps.md) | Type alias | 24 | <pre><code>&#123;&#10;    title&#58; ReactNode&#59;&#10;    subtitle&#63;&#58; ReactNode&#59;&#10;    meta&#63;&#58; ReactNode&#59;&#10;    actions&#63;&#58; ReactNode&#59;&#10;    className&#63;&#58; string&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PageLayout` | `({ children, variant = 'default', className, testId }: PageLayoutProps)` | — | — |
| `PageHeader` | `({ title, subtitle, meta, actions, className }: PageHeaderProps)` | — | — |
| `PageActions` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `Toolbar` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `ActionGroup` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `FormGrid` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `InlineField` | <pre><code>&#40;&#123;&#10;    label&#44;&#10;    children&#44;&#10;    hint&#44;&#10;    className&#44;&#10;&#125;&#58; &#123;&#10;    label&#58; ReactNode&#59;&#10;    children&#58; ReactNode&#59;&#10;    hint&#63;&#58; ReactNode&#59;&#10;    className&#63;&#58; string&#59;&#10;&#125;&#41;</code></pre> | — | — |
| `MetricGrid` | `({ children, columns = 4, className }: { children: ReactNode; columns?: 3 \| 4 \| 5 \| 6; className?: string })` | — | — |
| `TableFrame` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |

# PageLayout Module

**Path:** `frontend/src/components/ui/PageLayout.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/PageLayout.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `clsx` | `clsx` |
| `react` | `ReactNode` |

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
| [PageLayoutProps](../entities/PageLayoutProps.md) | Type alias | 4 | — | — |
| [PageHeaderProps](../entities/PageHeaderProps.md) | Type alias | 24 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PageLayout` | `({ children, variant = 'default', className, testId }: PageLayoutProps)` | — | — |
| `PageHeader` | `({ title, subtitle, meta, actions, className }: PageHeaderProps)` | — | — |
| `PageActions` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `Toolbar` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `ActionGroup` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `FormGrid` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |
| `InlineField` | `({     label,     children,     hint,     className, }: {     label: ReactNode;     children: ReactNode;     hint?: ReactNode;     className?: string; })` | — | — |
| `MetricGrid` | `({ children, columns = 4, className }: { children: ReactNode; columns?: 3 \| 4 \| 5 \| 6; className?: string })` | — | — |
| `TableFrame` | `({ children, className }: { children: ReactNode; className?: string })` | — | — |

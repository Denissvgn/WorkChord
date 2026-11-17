import js from '@eslint/js'
import globals from 'globals'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'
import singlePageToolbar from './eslint-rules/single-page-toolbar.js'

export default defineConfig([
  globalIgnores(['dist', 'coverage']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      jsxA11y.flatConfigs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    rules: {
      // The app does not build with React Compiler, so reports of where it would skip a component do not apply.
      'react-hooks/preserve-manual-memoization': 'off',
      // Keep semantic, keyboard-interaction, and ARIA regressions blocking.
      'jsx-a11y/anchor-is-valid': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/control-has-associated-label': ['error', {
        ignoreElements: ['audio', 'canvas', 'embed', 'input', 'textarea', 'tr', 'td', 'video'],
        ignoreRoles: ['grid', 'listbox', 'menu', 'menubar', 'radiogroup', 'row', 'tablist', 'toolbar', 'tree', 'treegrid'],
        includeRoles: ['alert', 'dialog'],
      }],
      'jsx-a11y/interactive-supports-focus': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      'jsx-a11y/media-has-caption': 'error',
      'jsx-a11y/mouse-events-have-key-events': 'error',
      'jsx-a11y/no-autofocus': 'error',
      'jsx-a11y/no-noninteractive-element-interactions': 'error',
      'jsx-a11y/no-static-element-interactions': 'error',
    },
  },
  {
    // The page frame and the shared parts: pages and components build their screens from
    // Button, Select, ButtonLink, OverflowMenu and the page parts, never from the native elements.
    files: ['src/**/*.tsx'],
    ignores: ['src/components/common/**', 'src/components/ui/**', 'src/**/*.test.tsx', 'src/test/**'],
    plugins: { workchord: { rules: { 'single-page-toolbar': singlePageToolbar } } },
    rules: {
      'no-restricted-syntax': ['error',
        {
          selector: "JSXOpeningElement[name.type='JSXIdentifier'][name.name='button']",
          message: 'Use Button, ButtonLink or OverflowMenu from the shared parts instead of a native <button>.',
        },
        {
          selector: "JSXOpeningElement[name.type='JSXIdentifier'][name.name='select']",
          message: 'Use Select from the shared parts instead of a native <select>.',
        },
      ],
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: '(^|/)IterationSelector(\\.[a-z]+)?$',
          message: 'No page has its own iteration selector. The scope bar in the top bar sets the iteration for every scoped page.',
        }],
      }],
      'workchord/single-page-toolbar': 'error',
    },
  },
])

---
applyTo: "**/*.{ts,tsx}"
excludeAgent: "cloud-agent"
---
# TypeScript & React Deployment Safety

## Production Crashes & React Failures
- **Infinite Render Loops**: Flag `useEffect`, `useMemo`, or `useCallback` hooks with unstable object/array literals or missing dependencies that trigger infinite re-renders.
- **State Mutation**: Flag direct mutations of state or props (e.g., `state.items.push()`), which break React change detection and cause desynchronized UI state.
- **SSR & Hydration Breakages**: In Next.js App Router, flag browser APIs (`window`, `localStorage`, `document`) used in Server Components without `"use client"` or without `useEffect`/dynamic import guards.
- **Unsafe Type Casts on External Data**: Flag unchecked `as Type` assertions on unvalidated API responses or external payloads that could trigger runtime `TypeError: cannot read property of undefined`.
- **Resource Leaks**: Verify cleanup handlers exist for event listeners, intervals, websockets, and active subscriptions in `useEffect`.

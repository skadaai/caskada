---
"brainyflow": minor
---

### Enhancements and Refactoring of BrainyFlow

- Improved type safety by introducing generics and stricter type annotations for `Memory`, `Node`, and `Flow`.
- Refactored `TestNode` to `BaseTestNode` for better modularity in tests.
- Enhanced documentation with updated examples and added type-safe patterns.
- `Memory` and `Node` now alow for explicit type parameters (`GlobalStore`, `LocalStore`).

### Migration Notes
- Update `Node` and `Memory` instantiations to include type parameters.
- Update tests to use `BaseTestNode` instead of `TestNode`.

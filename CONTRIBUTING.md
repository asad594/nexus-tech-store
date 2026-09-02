# 🤝 Contributing to Nexus Tech Store

Thank you for your interest in contributing to **Nexus Tech Store**! We welcome contributions ranging from bug fixes and documentation to new features and UI improvements.

---

## 🌿 Branching Strategy

- `main`: Production-ready, stable codebase.
- `feature/<feature-name>`: New capabilities or functional extensions.
- `fix/<bug-description>`: Bug fixes and issue patches.
- `docs/<topic>`: Documentation updates and architectural guides.
- `chore/<tooling>`: Tooling, dependencies, and CI/CD workflow updates.

---

## 📝 Commit Conventions

We enforce [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short summary in imperative mood>

# Examples:
feat(backend): add custom field validators for store catalog
feat(frontend): add useScrollPosition custom hook
test(backend): add unit tests for throttling configuration
docs(api): update OpenAPI 3.0 specification
```

**Allowed Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`.

---

## 🧪 Testing Guidelines

Before opening a pull request, ensure all test suites pass with zero regressions:

### Backend Testing
```bash
cd backend
python manage.py test store
```

### Pre-commit Hooks
```bash
pre-commit run --all-files
```

---

## 🚀 Pull Request Checklist

When submitting a PR, verify the following:
- [ ] Code follows existing PEP 8 (Python) and ESLint/Prettier (JS) standards.
- [ ] New endpoints, models, or hooks include appropriate unit test coverage.
- [ ] No regression in frontend styling, responsive layouts, or API backward compatibility.
- [ ] `CHANGELOG.md` is updated if submitting notable feature additions or fixes.


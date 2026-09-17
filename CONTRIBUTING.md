# Contributing to ComplaintIQ

First off, thank you for considering contributing to ComplaintIQ! It's people like you that make it such a great tool.

## How to Report Bugs
If you find a bug, please create an issue on GitHub. Include:
- A descriptive title.
- Steps to reproduce the behavior.
- Expected behavior vs actual behavior.
- Screenshots if applicable.
- Your OS and browser version.

## How to Suggest Features
Feature requests are welcome! Open an issue and provide:
- A clear, descriptive title.
- A detailed description of the proposed feature.
- The specific use case or problem it solves.

## Development Setup
1. Fork the repository.
2. Clone your fork locally.
3. Follow the installation instructions in `README.md` to set up the backend and frontend.
4. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`.

## Pull Request Guidelines
- Keep pull requests focused on a single issue or feature.
- Ensure your code follows the established style guide (see `CLAUDE.md`).
- Update documentation (`README.md`, `docs/API.md`, etc.) if you change functionality.
- Verify that the app still starts and runs locally without errors.

## Code Style Guide
- **Python**: PEP 8 compliance. Use Black for formatting. Include type hints.
- **JavaScript**: ES6+, meaningful variable names, use Prettier for formatting.
- **HTML/CSS**: Semantic HTML, use Tailwind utility classes.

## Testing Requirements
Since this is an MVP, we rely on manual API testing via Swagger UI (`/docs`). Before submitting a PR:
- Verify all modified endpoints function correctly.
- Test frontend UI changes across desktop and simulated mobile views.
- Ensure no console errors appear in the browser.

## Commit Message Format
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat: add new AI drafting module`
- `fix: resolve CORS issue on login`
- `docs: update API endpoints in API.md`
- `refactor: optimize DB queries in services`

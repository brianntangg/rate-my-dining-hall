# Contributing to Rate My Dining Hall

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit and push
7. Create a Pull Request

## Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

Quick start:

```bash
cp .env.example .env
docker-compose up
```

## Code Style

### Backend (Python)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function parameters and return values
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

Example:

```python
def calculate_review_score(upvotes: int, downvotes: int) -> int:
    """Calculate the score for a review.

    Args:
        upvotes: Number of upvotes
        downvotes: Number of downvotes

    Returns:
        The calculated score (upvotes - downvotes)
    """
    return upvotes - downvotes
```

### Frontend (TypeScript/React)

- Use functional components with hooks
- Define TypeScript interfaces for all props and data
- Use meaningful component and variable names
- Keep components focused and reusable
- Extract complex logic into custom hooks

Example:

```typescript
interface ReviewCardProps {
  review: Review;
  onVote: (reviewId: number, value: 1 | -1) => void;
}

export const ReviewCard: React.FC<ReviewCardProps> = ({ review, onVote }) => {
  // Component implementation
};
```

## Testing

### Backend Tests

All new features should include tests. Use pytest:

```bash
cd backend
pytest
```

Test structure:

```python
def test_feature_success(client: TestClient):
    """Test successful feature operation"""
    response = client.post("/api/endpoint", json={"data": "value"})
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```

### Running Tests

Before submitting a PR:

```bash
# Backend tests
cd backend
pytest -v

# Check coverage
pytest --cov=app

# Frontend build (when tests are added)
cd frontend
npm run build
```

## Pull Request Process

1. **Create a clear PR title**
   - Use format: `[Feature/Fix/Docs] Brief description`
   - Examples:
     - `[Feature] Add email verification`
     - `[Fix] Resolve duplicate vote issue`
     - `[Docs] Update deployment guide`

2. **Write a good description**
   - Explain what changes you made
   - Reference any related issues
   - Include screenshots for UI changes
   - List any breaking changes

3. **Ensure tests pass**
   - All existing tests must pass
   - Add tests for new features
   - GitHub Actions will run tests automatically

4. **Keep PRs focused**
   - One feature/fix per PR
   - Split large changes into multiple PRs
   - Rebase on latest main/develop before submitting

5. **Respond to feedback**
   - Address reviewer comments
   - Push additional commits if needed
   - Mark conversations as resolved when addressed

## Commit Messages

Write clear, concise commit messages:

Good:

```text
Add user profile page

- Create profile component
- Add API endpoint for user data
- Include tests for profile route
```

Bad:

```text
fix stuff
wip
changes
```

## Database Migrations

When modifying models:

1. Create migration:

   ```bash
   cd backend
   alembic revision --autogenerate -m "Description of change"
   ```

2. Review the generated migration file

3. Test the migration:

   ```bash
   alembic upgrade head
   alembic downgrade -1
   alembic upgrade head
   ```

4. Include migration file in your PR

## Adding New Dependencies

### Backend

1. Add to `backend/requirements.txt`
2. Rebuild Docker: `docker-compose up --build backend`
3. Document why the dependency is needed in PR

### Frontend

1. Use `npm install <package>`
2. Commit `package.json` and `package-lock.json`
3. Document why the dependency is needed in PR

## API Design Guidelines

1. **Use RESTful conventions**
   - GET for retrieving data
   - POST for creating resources
   - PATCH for partial updates
   - DELETE for removing resources

2. **Return appropriate status codes**
   - 200: Success
   - 201: Created
   - 400: Bad request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not found
   - 500: Server error

3. **Use consistent response formats**

   ```python
   # Success
   {"id": 1, "name": "Resource"}

   # Error
   {"detail": "Error message"}
   ```

4. **Document all endpoints**
   - Add docstrings to route functions
   - Include example requests/responses
   - Document required auth

## UI/UX Guidelines

1. **Follow existing patterns**
   - Use Tailwind utility classes
   - Match existing component styles
   - Maintain consistent spacing

2. **Mobile-first responsive design**
   - Test on mobile, tablet, and desktop
   - Use responsive Tailwind classes

3. **Loading and error states**
   - Show loading indicators
   - Display meaningful error messages
   - Provide retry options when appropriate

4. **Accessibility**
   - Use semantic HTML
   - Include ARIA labels where needed
   - Ensure keyboard navigation works

## Feature Ideas

Want to contribute but not sure where to start? Here are some ideas:

### Short-term (MVP improvements)

- [ ] Add image upload support (Cloudinary)
- [ ] Implement review editing
- [ ] Add pagination for reviews
- [ ] Implement search functionality
- [ ] Add email verification
- [ ] Improve mobile layout

### Medium-term

- [ ] Admin panel for managing dining halls
- [ ] User profiles with review history
- [ ] Comment/reply system for reviews
- [ ] Report inappropriate reviews
- [ ] Rating breakdown (food quality, service, cleanliness)

### Long-term

- [ ] Multi-school support
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Integration with dining hall menus
- [ ] Analytics dashboard

## Questions?

- Open an issue for bug reports or feature requests
- Use GitHub Discussions for questions
- Check existing issues before creating new ones

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/)

Thank you for contributing to Rate My Dining Hall!

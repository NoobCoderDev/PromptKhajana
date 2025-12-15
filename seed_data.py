"""
Seed data script to populate the database with professional developer prompts
"""
from app import create_app, db
from app.models import Category, Tag, Prompt

def create_categories():
    """Create predefined categories"""
    categories_data = [
        {'name': 'Development', 'slug': 'development', 'icon': 'fas fa-code', 
         'description': 'General software development prompts'},
        {'name': 'Refactoring', 'slug': 'refactoring', 'icon': 'fas fa-recycle', 
         'description': 'Code refactoring and improvement prompts'},
        {'name': 'Testing', 'slug': 'testing', 'icon': 'fas fa-flask', 
         'description': 'Unit, integration, and E2E testing prompts'},
        {'name': 'Debugging', 'slug': 'debugging', 'icon': 'fas fa-bug', 
         'description': 'Debugging and troubleshooting prompts'},
        {'name': 'Code Review', 'slug': 'code-review', 'icon': 'fas fa-eye', 
         'description': 'Code review and quality assurance prompts'},
        {'name': 'Architecture', 'slug': 'architecture', 'icon': 'fas fa-building', 
         'description': 'System design and architecture prompts'},
        {'name': 'Documentation', 'slug': 'documentation', 'icon': 'fas fa-book', 
         'description': 'Technical documentation prompts'},
        {'name': 'Performance', 'slug': 'performance', 'icon': 'fas fa-bolt', 
         'description': 'Performance optimization prompts'},
        {'name': 'Security', 'slug': 'security', 'icon': 'fas fa-lock', 
         'description': 'Security review and hardening prompts'},
        {'name': 'DevOps', 'slug': 'devops', 'icon': 'fas fa-rocket', 
         'description': 'CI/CD and deployment prompts'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.query.filter_by(slug=cat_data['slug']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            categories.append(category)
        else:
            categories.append(category)
    
    db.session.commit()
    return categories

def create_tags():
    """Create predefined tags"""
    tags_data = [
        'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'Flask', 'Django',
        'API', 'Database', 'SQL', 'NoSQL', 'Frontend', 'Backend', 'Full-Stack',
        'Clean Code', 'Best Practices', 'Design Patterns', 'Microservices',
        'REST', 'GraphQL', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'Git', 'CI/CD', 'Monitoring', 'Logging', 'Error Handling'
    ]
    
    tags = []
    for tag_name in tags_data:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name, slug=tag_name.lower().replace('.', '').replace(' ', '-'))
            db.session.add(tag)
            tags.append(tag)
        else:
            tags.append(tag)
    
    db.session.commit()
    return tags

def create_prompts(categories, tags):
    """Create professional developer prompts"""
    
    # Helper function to get category by slug
    def get_cat(slug):
        return next(c for c in categories if c.slug == slug)
    
    # Helper function to get tags by names
    def get_tags(*names):
        return [t for t in tags if t.name in names]
    
    prompts_data = [
        {
            'title': 'Code Review Checklist Generator',
            'description': 'Generate a comprehensive code review checklist for any programming language',
            'content': '''# Code Review Checklist

Please analyze the following code and create a comprehensive code review checklist:

**Code Context:**
[Paste your code here]

**Programming Language:** [Specify language]

**Review Focus Areas:**
1. Code quality and readability
2. Performance considerations
3. Security vulnerabilities
4. Error handling
5. Testing coverage
6. Documentation completeness
7. Best practices adherence
8. Design patterns usage

Please provide:
- Specific issues found
- Severity level (Critical/High/Medium/Low)
- Suggested improvements
- Code examples for fixes''',
            'use_case': 'Use this prompt when conducting code reviews, preparing for pull request reviews, or establishing code quality standards for your team.',
            'examples': '''**Example Usage:**

```python
# Example code to review
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total
```

**AI Response would include:**
- Missing type hints
- No input validation
- No error handling for missing 'price' key
- Could use sum() with generator expression
- Missing docstring''',
            'difficulty': 'Intermediate',
            'rating': 4.8,
            'category_id': get_cat('code-review').id,
            'tags': get_tags('Best Practices', 'Clean Code')
        },
        {
            'title': 'API Design Best Practices',
            'description': 'Design RESTful APIs following industry best practices',
            'content': '''# RESTful API Design

I need to design a RESTful API for: [Describe your application/feature]

**Requirements:**
- Resource: [e.g., User Management, Product Catalog]
- Operations needed: [CRUD operations]
- Authentication: [JWT, OAuth, API Key]
- Expected load: [requests per second]

Please provide:
1. **Endpoint Structure** - URL patterns following REST conventions
2. **HTTP Methods** - Appropriate methods for each operation
3. **Request/Response Format** - JSON schema examples
4. **Status Codes** - Proper HTTP status codes
5. **Error Handling** - Standardized error response format
6. **Pagination** - Strategy for large datasets
7. **Versioning** - API versioning approach
8. **Rate Limiting** - Recommendations for rate limiting
9. **Security** - Authentication and authorization patterns
10. **Documentation** - OpenAPI/Swagger specification''',
            'use_case': 'Use when designing new APIs, refactoring existing endpoints, or establishing API standards for your organization.',
            'examples': '''**Example:**
Resource: User Management System

**Response includes:**
```
GET    /api/v1/users          - List users (paginated)
GET    /api/v1/users/{id}     - Get user details
POST   /api/v1/users          - Create user
PUT    /api/v1/users/{id}     - Update user
DELETE /api/v1/users/{id}     - Delete user
```''',
            'difficulty': 'Advanced',
            'rating': 4.9,
            'category_id': get_cat('architecture').id,
            'tags': get_tags('API', 'REST', 'Best Practices', 'Backend')
        },
        {
            'title': 'Unit Test Generator',
            'description': 'Generate comprehensive unit tests for your functions and classes',
            'content': '''# Unit Test Generation

Generate comprehensive unit tests for the following code:

**Code to Test:**
```
[Paste your function/class here]
```

**Testing Framework:** [pytest/unittest/jest/mocha]
**Programming Language:** [Python/JavaScript/TypeScript/etc.]

**Test Coverage Requirements:**
1. Happy path scenarios
2. Edge cases
3. Error conditions
4. Boundary values
5. Mock external dependencies
6. Test data fixtures

Please provide:
- Complete test file with imports
- Test class/suite structure
- Individual test cases with descriptive names
- Assertions for expected behavior
- Mock/stub setup if needed
- Test data examples
- Coverage for at least 90% of code paths''',
            'use_case': 'Use when writing tests for new features, improving test coverage, or learning testing best practices.',
            'examples': '''**Example:**
```python
def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

**Generated tests would cover:**
- Valid discount calculations
- Zero discount
- 100% discount
- Negative discount (error case)
- Over 100% discount (error case)
- Edge values (0.01, 99.99)''',
            'difficulty': 'Intermediate',
            'rating': 4.7,
            'category_id': get_cat('testing').id,
            'tags': get_tags('Python', 'Best Practices', 'Testing')
        },
        {
            'title': 'Database Schema Design',
            'description': 'Design optimal database schemas with proper relationships and indexes',
            'content': '''# Database Schema Design

Design a database schema for: [Describe your application]

**Requirements:**
- Database Type: [PostgreSQL/MySQL/MongoDB/etc.]
- Main Entities: [List key entities]
- Expected Scale: [number of records, concurrent users]
- Query Patterns: [common queries]

Please provide:
1. **Entity Relationship Diagram** (textual description)
2. **Table Definitions** with columns, data types, constraints
3. **Primary Keys** and **Foreign Keys**
4. **Indexes** for query optimization
5. **Relationships** (one-to-one, one-to-many, many-to-many)
6. **Normalization** level and justification
7. **Sample Queries** for common operations
8. **Migration Strategy** for schema changes
9. **Scalability Considerations**
10. **Data Integrity Rules**''',
            'use_case': 'Use when starting new projects, refactoring existing databases, or optimizing database performance.',
            'examples': '''**Example:**
Application: E-commerce Platform
Entities: Users, Products, Orders, Reviews

**Response includes:**
- Users table (id, email, password_hash, created_at)
- Products table (id, name, price, stock, category_id)
- Orders table (id, user_id, total, status, created_at)
- Order_Items junction table
- Indexes on foreign keys and frequently queried columns''',
            'difficulty': 'Advanced',
            'rating': 4.8,
            'category_id': get_cat('architecture').id,
            'tags': get_tags('Database', 'SQL', 'Design Patterns')
        },
        {
            'title': 'Performance Optimization Analysis',
            'description': 'Analyze code for performance bottlenecks and optimization opportunities',
            'content': '''# Performance Optimization

Analyze the following code for performance issues and suggest optimizations:

**Code:**
```
[Paste your code here]
```

**Context:**
- Programming Language: [language]
- Current Performance: [execution time, memory usage]
- Performance Target: [desired metrics]
- Scale: [data volume, concurrent users]

Please analyze:
1. **Time Complexity** - Big O analysis
2. **Space Complexity** - Memory usage
3. **Bottlenecks** - Identify slow operations
4. **Database Queries** - N+1 queries, missing indexes
5. **Algorithm Efficiency** - Better algorithms/data structures
6. **Caching Opportunities** - What can be cached
7. **Async Operations** - Parallelization opportunities
8. **Resource Usage** - CPU, memory, I/O optimization

Provide:
- Specific performance issues
- Optimized code examples
- Expected performance improvement
- Trade-offs and considerations''',
            'use_case': 'Use when experiencing slow application performance, optimizing critical code paths, or preparing for scale.',
            'examples': '''**Example:**
```python
# Slow code
def get_user_posts(user_id):
    user = User.query.get(user_id)
    posts = []
    for post_id in user.post_ids:
        post = Post.query.get(post_id)  # N+1 query!
        posts.append(post)
    return posts
```

**Optimized:**
```python
def get_user_posts(user_id):
    return Post.query.filter(Post.user_id == user_id).all()
```''',
            'difficulty': 'Advanced',
            'rating': 4.9,
            'category_id': get_cat('performance').id,
            'tags': get_tags('Performance', 'Database', 'Best Practices')
        },
        {
            'title': 'Security Vulnerability Scanner',
            'description': 'Identify security vulnerabilities and suggest fixes',
            'content': '''# Security Vulnerability Analysis

Review the following code for security vulnerabilities:

**Code:**
```
[Paste your code here]
```

**Application Type:** [Web API/Frontend/Backend/Mobile]
**Framework:** [Flask/Django/Express/React/etc.]

Check for:
1. **SQL Injection** - Unsafe database queries
2. **XSS** - Cross-site scripting vulnerabilities
3. **CSRF** - Cross-site request forgery
4. **Authentication Issues** - Weak password policies, session management
5. **Authorization** - Access control flaws
6. **Data Exposure** - Sensitive data in logs/responses
7. **Input Validation** - Unvalidated user input
8. **Cryptography** - Weak encryption, hardcoded secrets
9. **Dependencies** - Known vulnerable packages
10. **API Security** - Rate limiting, CORS issues

Provide:
- Vulnerability description and severity
- Exploit scenario
- Secure code example
- Prevention best practices''',
            'use_case': 'Use during security audits, before production deployments, or when implementing authentication/authorization.',
            'examples': '''**Example:**
```python
# Vulnerable code
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection!
    result = db.execute(query)
    return jsonify(result)
```

**Secure version:**
```python
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return jsonify(result)
```''',
            'difficulty': 'Advanced',
            'rating': 5.0,
            'category_id': get_cat('security').id,
            'tags': get_tags('Security', 'Best Practices', 'Backend')
        },
        {
            'title': 'Refactoring Strategy',
            'description': 'Get step-by-step refactoring guidance for legacy code',
            'content': '''# Code Refactoring Strategy

I need to refactor the following code:

**Current Code:**
```
[Paste your code here]
```

**Issues:**
- [List known problems: duplication, complexity, poor naming, etc.]

**Constraints:**
- Must maintain backward compatibility: [Yes/No]
- Test coverage: [percentage]
- Timeline: [available time]

Please provide:
1. **Code Smells Identified** - What's wrong
2. **Refactoring Steps** - Incremental, safe changes
3. **Design Patterns** - Applicable patterns
4. **Before/After Examples** - Show improvements
5. **Testing Strategy** - How to ensure no breakage
6. **Risk Assessment** - Potential issues
7. **Metrics** - Complexity reduction, maintainability improvement

Prioritize:
- Readability
- Maintainability
- Testability
- Performance (if applicable)''',
            'use_case': 'Use when dealing with legacy code, reducing technical debt, or improving code maintainability.',
            'examples': '''**Example:**
```python
# Before: God class with multiple responsibilities
class UserManager:
    def create_user(self, data): ...
    def send_email(self, user): ...
    def log_activity(self, action): ...
    def validate_password(self, pwd): ...
```

**After: Single Responsibility Principle**
```python
class UserRepository:
    def create(self, user): ...

class EmailService:
    def send_welcome_email(self, user): ...

class ActivityLogger:
    def log(self, action): ...
```''',
            'difficulty': 'Intermediate',
            'rating': 4.6,
            'category_id': get_cat('refactoring').id,
            'tags': get_tags('Clean Code', 'Design Patterns', 'Best Practices')
        },
        {
            'title': 'Docker Configuration Generator',
            'description': 'Generate production-ready Dockerfile and docker-compose configurations',
            'content': '''# Docker Configuration

Create Docker configuration for:

**Application Details:**
- Type: [Web API/Frontend/Backend/Full-stack]
- Language/Framework: [Python/Node.js/Java/etc.]
- Dependencies: [Database, Redis, etc.]
- Environment: [Development/Production]

Please provide:
1. **Dockerfile** - Multi-stage build, optimized layers
2. **docker-compose.yml** - All services defined
3. **.dockerignore** - Exclude unnecessary files
4. **Environment Variables** - Configuration management
5. **Health Checks** - Container health monitoring
6. **Volume Mounts** - Data persistence
7. **Networking** - Service communication
8. **Security** - Non-root user, minimal base image
9. **Build Optimization** - Layer caching, size reduction
10. **Documentation** - How to build and run

Best Practices:
- Small image size
- Fast build times
- Security hardening
- Production-ready''',
            'use_case': 'Use when containerizing applications, setting up development environments, or preparing for deployment.',
            'examples': '''**Example for Flask App:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```''',
            'difficulty': 'Intermediate',
            'rating': 4.7,
            'category_id': get_cat('devops').id,
            'tags': get_tags('Docker', 'DevOps', 'CI/CD')
        },
        {
            'title': 'CI/CD Pipeline Configuration',
            'description': 'Create comprehensive CI/CD pipeline configurations',
            'content': '''# CI/CD Pipeline Setup

Create a CI/CD pipeline for:

**Project Details:**
- Repository: [GitHub/GitLab/Bitbucket]
- Application Type: [Web/API/Mobile/etc.]
- Tech Stack: [languages, frameworks]
- Deployment Target: [AWS/Azure/GCP/Heroku/etc.]

Pipeline Stages:
1. **Build** - Compile/bundle application
2. **Test** - Run unit, integration tests
3. **Lint** - Code quality checks
4. **Security Scan** - Dependency vulnerabilities
5. **Build Docker Image** - Containerization
6. **Deploy to Staging** - Automated staging deployment
7. **Integration Tests** - E2E tests on staging
8. **Deploy to Production** - Production deployment
9. **Smoke Tests** - Post-deployment validation
10. **Rollback Strategy** - Automated rollback on failure

Include:
- Pipeline configuration file (GitHub Actions/GitLab CI/Jenkins)
- Environment variables and secrets management
- Deployment strategies (blue-green, canary, rolling)
- Notifications (Slack, email)
- Monitoring integration''',
            'use_case': 'Use when setting up automated deployments, improving release processes, or establishing DevOps practices.',
            'examples': '''**GitHub Actions Example:**
```yaml
name: CI/CD
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```''',
            'difficulty': 'Advanced',
            'rating': 4.8,
            'category_id': get_cat('devops').id,
            'tags': get_tags('CI/CD', 'DevOps', 'AWS')
        },
        {
            'title': 'Technical Documentation Writer',
            'description': 'Generate comprehensive technical documentation',
            'content': '''# Technical Documentation

Create documentation for:

**Subject:**
- Type: [API/Library/Framework/System]
- Name: [project name]
- Purpose: [what it does]

**Documentation Sections:**

1. **Overview** - What is it, why use it
2. **Getting Started** - Installation, setup
3. **Quick Start Guide** - Hello World example
4. **Core Concepts** - Key terminology, architecture
5. **API Reference** - Detailed API documentation
6. **Usage Examples** - Common use cases with code
7. **Configuration** - All configuration options
8. **Best Practices** - Recommended patterns
9. **Troubleshooting** - Common issues and solutions
10. **FAQ** - Frequently asked questions
11. **Changelog** - Version history
12. **Contributing** - How to contribute

**Code/System to Document:**
```
[Paste code or describe system]
```

Format: [Markdown/ReStructuredText/HTML]
Audience: [Beginners/Intermediate/Advanced developers]''',
            'use_case': 'Use when documenting new features, creating API documentation, or onboarding new team members.',
            'examples': '''**Example Output:**
# User Authentication API

## Overview
RESTful API for user authentication with JWT tokens.

## Quick Start
```python
from auth_api import AuthClient
client = AuthClient(api_key="your_key")
token = client.login("user@example.com", "password")
```

## API Reference
### POST /auth/login
Authenticate user and return JWT token...''',
            'difficulty': 'Beginner',
            'rating': 4.5,
            'category_id': get_cat('documentation').id,
            'tags': get_tags('Documentation', 'API', 'Best Practices')
        },
        {
            'title': 'Error Handling Strategy',
            'description': 'Implement comprehensive error handling and logging',
            'content': '''# Error Handling Implementation

Design error handling strategy for:

**Application Context:**
- Type: [Web API/CLI/Library/etc.]
- Language: [Python/JavaScript/Java/etc.]
- Framework: [Flask/Express/Spring/etc.]

**Requirements:**
1. **Exception Hierarchy** - Custom exception classes
2. **Error Codes** - Standardized error codes
3. **Error Messages** - User-friendly messages
4. **Logging Strategy** - What to log, log levels
5. **Error Response Format** - Consistent JSON/XML structure
6. **Stack Traces** - When to include/exclude
7. **Error Recovery** - Retry logic, fallbacks
8. **Monitoring** - Error tracking integration (Sentry, etc.)
9. **User Feedback** - How to communicate errors to users
10. **Security** - Avoid leaking sensitive information

**Current Code:**
```
[Paste code that needs error handling]
```

Provide:
- Custom exception classes
- Try-catch patterns
- Error middleware/decorators
- Logging configuration
- Example error responses''',
            'use_case': 'Use when building robust applications, improving error handling, or debugging production issues.',
            'examples': '''**Example:**
```python
# Before
def get_user(user_id):
    user = db.query(User).get(user_id)
    return user.to_dict()

# After
class UserNotFoundError(Exception):
    pass

def get_user(user_id):
    try:
        user = db.query(User).get(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
        return user.to_dict()
    except UserNotFoundError as e:
        logger.warning(str(e))
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```''',
            'difficulty': 'Intermediate',
            'rating': 4.6,
            'category_id': get_cat('development').id,
            'tags': get_tags('Error Handling', 'Best Practices', 'Logging')
        },
        {
            'title': 'Debugging Assistant',
            'description': 'Systematic debugging approach for complex issues',
            'content': '''# Debugging Guide

Help me debug this issue:

**Problem Description:**
[Describe the bug/issue]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Code:**
```
[Paste relevant code]
```

**Error Message/Stack Trace:**
```
[Paste error message]
```

**Environment:**
- Language/Framework: [details]
- Version: [version numbers]
- OS: [operating system]
- Dependencies: [relevant packages]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

Please provide:
1. **Root Cause Analysis** - What's causing the issue
2. **Debugging Steps** - How to investigate further
3. **Fix** - Code changes needed
4. **Prevention** - How to avoid similar issues
5. **Testing** - How to verify the fix
6. **Alternative Solutions** - Other approaches

Include:
- Logging suggestions
- Debugging tools to use
- Common pitfalls in this scenario''',
            'use_case': 'Use when stuck on a bug, investigating production issues, or learning debugging techniques.',
            'examples': '''**Example:**
Problem: "Function returns None instead of expected value"

**Analysis:**
1. Check if function has return statement
2. Verify conditional logic paths
3. Check for early returns
4. Validate input parameters
5. Add print/log statements
6. Use debugger breakpoints''',
            'difficulty': 'Intermediate',
            'rating': 4.7,
            'category_id': get_cat('debugging').id,
            'tags': get_tags('Debugging', 'Error Handling', 'Best Practices')
        },
        {
            'title': 'Microservices Architecture Design',
            'description': 'Design scalable microservices architecture',
            'content': '''# Microservices Architecture

Design a microservices architecture for:

**Application:** [Describe your application]
**Current State:** [Monolith/Partial microservices/Greenfield]
**Scale Requirements:** [Users, requests, data volume]

Please design:

1. **Service Decomposition**
   - Identify bounded contexts
   - Define service boundaries
   - Service responsibilities

2. **Communication Patterns**
   - Synchronous (REST/gRPC)
   - Asynchronous (Message queues)
   - Event-driven architecture

3. **Data Management**
   - Database per service
   - Data consistency strategies
   - Shared data handling

4. **Service Discovery**
   - Registry pattern
   - Load balancing

5. **API Gateway**
   - Routing
   - Authentication
   - Rate limiting

6. **Resilience Patterns**
   - Circuit breakers
   - Retry logic
   - Fallbacks
   - Timeouts

7. **Monitoring & Observability**
   - Distributed tracing
   - Centralized logging
   - Metrics collection

8. **Deployment Strategy**
   - Container orchestration
   - CI/CD pipeline
   - Blue-green deployment

Provide:
- Architecture diagram (textual)
- Service definitions
- Technology recommendations
- Migration strategy (if from monolith)''',
            'use_case': 'Use when breaking down monoliths, designing scalable systems, or planning microservices migration.',
            'examples': '''**Example:**
E-commerce Application

**Services:**
- User Service (authentication, profiles)
- Product Service (catalog, inventory)
- Order Service (order processing)
- Payment Service (payment processing)
- Notification Service (emails, SMS)

**Communication:**
- API Gateway → Services (REST)
- Services → Services (gRPC)
- Event Bus (RabbitMQ) for async events''',
            'difficulty': 'Advanced',
            'rating': 4.9,
            'category_id': get_cat('architecture').id,
            'tags': get_tags('Microservices', 'Architecture', 'Design Patterns')
        },
        {
            'title': 'Frontend Component Architecture',
            'description': 'Design reusable, maintainable frontend components',
            'content': '''# Frontend Component Design

Design a component architecture for:

**Framework:** [React/Vue/Angular/Svelte]
**Component Type:** [Form/Table/Modal/Dashboard/etc.]
**Complexity:** [Simple/Medium/Complex]

**Requirements:**
- Functionality: [What it should do]
- Props/Inputs: [Configurable options]
- State Management: [Local/Global]
- Styling: [CSS/Styled-components/Tailwind]

Please provide:

1. **Component Structure**
   - File organization
   - Component hierarchy
   - Prop definitions

2. **State Management**
   - Local state
   - Context/Redux integration
   - State update patterns

3. **Event Handling**
   - User interactions
   - Event callbacks
   - Custom events

4. **Styling Approach**
   - CSS modules/Styled components
   - Responsive design
   - Theme support

5. **Accessibility**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support

6. **Performance**
   - Memoization
   - Lazy loading
   - Code splitting

7. **Testing**
   - Unit tests
   - Integration tests
   - Accessibility tests

8. **Documentation**
   - Props documentation
   - Usage examples
   - Storybook stories

Include complete code example with TypeScript types if applicable.''',
            'use_case': 'Use when building component libraries, creating reusable UI components, or establishing frontend architecture.',
            'examples': '''**Example: Button Component**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant,
  size,
  disabled,
  onClick,
  children
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
      aria-label={typeof children === 'string' ? children : undefined}
    >
      {children}
    </button>
  );
};
```''',
            'difficulty': 'Intermediate',
            'rating': 4.6,
            'category_id': get_cat('development').id,
            'tags': get_tags('React', 'Frontend', 'TypeScript', 'Design Patterns')
        },
        {
            'title': 'Database Migration Strategy',
            'description': 'Plan and execute safe database migrations',
            'content': '''# Database Migration Planning

Plan a database migration for:

**Current State:**
- Database: [PostgreSQL/MySQL/MongoDB/etc.]
- Schema: [Describe current schema]
- Data Volume: [Number of records]
- Downtime Tolerance: [Zero/Minimal/Acceptable]

**Target State:**
- Changes needed: [New tables/columns/indexes/etc.]
- Reason: [Why this migration is needed]

Please provide:

1. **Migration Strategy**
   - Backward compatible approach
   - Rollback plan
   - Data migration steps

2. **Migration Scripts**
   - Up migration (SQL/ORM)
   - Down migration (rollback)
   - Data transformation scripts

3. **Testing Plan**
   - Test on copy of production data
   - Validation queries
   - Performance testing

4. **Deployment Steps**
   - Pre-migration checklist
   - Execution order
   - Post-migration verification

5. **Risk Mitigation**
   - Backup strategy
   - Monitoring during migration
   - Rollback triggers

6. **Performance Impact**
   - Lock analysis
   - Index rebuild time
   - Query performance changes

7. **Zero-Downtime Approach** (if required)
   - Dual-write strategy
   - Feature flags
   - Gradual rollout

Provide:
- Complete migration scripts
- Timeline estimate
- Risk assessment
- Rollback procedure''',
            'use_case': 'Use when modifying production databases, adding new features requiring schema changes, or optimizing database structure.',
            'examples': '''**Example: Adding a column**
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill data (in batches)
UPDATE users SET phone = '' WHERE phone IS NULL;

-- Step 3: Make column NOT NULL
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- Rollback
ALTER TABLE users DROP COLUMN phone;
```''',
            'difficulty': 'Advanced',
            'rating': 4.8,
            'category_id': get_cat('development').id,
            'tags': get_tags('Database', 'SQL', 'DevOps')
        },
        {
            'title': 'API Integration Guide',
            'description': 'Integrate third-party APIs with best practices',
            'content': '''# API Integration

Integrate with: [API name/service]

**API Details:**
- Documentation URL: [link]
- Authentication: [API Key/OAuth/JWT]
- Rate Limits: [requests per minute/hour]
- Endpoints needed: [list endpoints]

**Integration Requirements:**
- Programming Language: [Python/JavaScript/etc.]
- Use Case: [What you're trying to achieve]
- Error Handling: [How to handle failures]
- Data Volume: [Expected API calls]

Please provide:

1. **Client Implementation**
   - API client class/module
   - Authentication handling
   - Request/response models

2. **Error Handling**
   - Retry logic with exponential backoff
   - Rate limit handling
   - Timeout configuration
   - Error logging

3. **Data Validation**
   - Request validation
   - Response parsing
   - Schema validation

4. **Caching Strategy**
   - What to cache
   - Cache invalidation
   - TTL configuration

5. **Testing**
   - Mock API responses
   - Integration tests
   - Error scenario tests

6. **Monitoring**
   - API call metrics
   - Error rate tracking
   - Performance monitoring

7. **Security**
   - API key management
   - Secrets storage
   - Request signing

8. **Documentation**
   - Usage examples
   - Configuration options
   - Troubleshooting guide

Include complete, production-ready code.''',
            'use_case': 'Use when integrating payment gateways, social media APIs, cloud services, or any third-party API.',
            'examples': '''**Example: Stripe Integration**
```python
import stripe
from tenacity import retry, stop_after_attempt, wait_exponential

class StripeClient:
    def __init__(self, api_key):
        stripe.api_key = api_key
    
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=2, max=10))
    def create_payment_intent(self, amount, currency='usd'):
        try:
            return stripe.PaymentIntent.create(
                amount=amount,
                currency=currency
            )
        except stripe.error.RateLimitError:
            # Handle rate limit
            raise
        except stripe.error.StripeError as e:
            # Handle other errors
            logger.error(f"Stripe error: {e}")
            raise
```''',
            'difficulty': 'Intermediate',
            'rating': 4.7,
            'category_id': get_cat('development').id,
            'tags': get_tags('API', 'Backend', 'Error Handling')
        },
        {
            'title': 'Code Complexity Reducer',
            'description': 'Simplify complex code while maintaining functionality',
            'content': '''# Code Simplification

Simplify this complex code:

**Current Code:**
```
[Paste complex code here]
```

**Issues:**
- Cyclomatic complexity: [if known]
- Nested levels: [depth]
- Function length: [lines]
- Readability concerns: [describe]

**Goals:**
- Reduce complexity
- Improve readability
- Maintain functionality
- Add tests if missing

Please provide:

1. **Complexity Analysis**
   - Current complexity metrics
   - Specific problem areas
   - Code smells identified

2. **Refactoring Steps**
   - Extract methods/functions
   - Reduce nesting
   - Simplify conditionals
   - Remove duplication

3. **Simplified Code**
   - Refactored version
   - Explanation of changes
   - Complexity improvement metrics

4. **Design Patterns**
   - Applicable patterns
   - When to use each pattern

5. **Testing Strategy**
   - Unit tests for new functions
   - Integration tests
   - Regression tests

6. **Documentation**
   - Function docstrings
   - Inline comments (where needed)
   - Usage examples

Focus on:
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- Clear naming
- Early returns''',
            'use_case': 'Use when code becomes hard to understand, maintain, or test due to high complexity.',
            'examples': '''**Example:**
```python
# Before: Complex nested conditions
def process_order(order):
    if order:
        if order.items:
            if order.user:
                if order.user.is_active:
                    if order.total > 0:
                        return process_payment(order)
    return None

# After: Early returns, clear logic
def process_order(order):
    if not order or not order.items:
        return None
    if not order.user or not order.user.is_active:
        return None
    if order.total <= 0:
        return None
    return process_payment(order)
```''',
            'difficulty': 'Intermediate',
            'rating': 4.6,
            'category_id': get_cat('refactoring').id,
            'tags': get_tags('Clean Code', 'Refactoring', 'Best Practices')
        },
        {
            'title': 'Logging Strategy Implementation',
            'description': 'Implement comprehensive logging for debugging and monitoring',
            'content': '''# Logging Implementation

Set up logging for:

**Application Type:** [Web API/CLI/Background Job/etc.]
**Language/Framework:** [Python/Node.js/Java/etc.]
**Environment:** [Development/Staging/Production]

**Requirements:**

1. **Log Levels**
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages
   - ERROR: Error messages
   - CRITICAL: Critical issues

2. **Log Structure**
   - Timestamp
   - Log level
   - Module/file name
   - Function name
   - Message
   - Context (user_id, request_id, etc.)
   - Stack trace (for errors)

3. **Log Destinations**
   - Console (development)
   - File (with rotation)
   - Centralized logging (ELK, CloudWatch, etc.)
   - Error tracking (Sentry, Rollbar)

4. **What to Log**
   - Application startup/shutdown
   - Request/response (API calls)
   - Database queries (slow queries)
   - External API calls
   - Errors and exceptions
   - Business events
   - Performance metrics
   - Security events

5. **What NOT to Log**
   - Passwords
   - API keys
   - Credit card numbers
   - Personal identifiable information (PII)

6. **Log Format**
   - JSON (for parsing)
   - Human-readable (for development)
   - Structured logging

7. **Performance Considerations**
   - Async logging
   - Log sampling
   - Conditional logging

Provide:
- Complete logging configuration
- Logger setup code
- Usage examples
- Best practices''',
            'use_case': 'Use when setting up new applications, debugging production issues, or improving observability.',
            'examples': '''**Example: Python Logging**
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'module': record.module,
            'message': record.getMessage(),
            'request_id': getattr(record, 'request_id', None)
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Setup
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Usage
logger.info('User logged in', extra={'request_id': '123', 'user_id': 456})
```''',
            'difficulty': 'Intermediate',
            'rating': 4.5,
            'category_id': get_cat('development').id,
            'tags': get_tags('Logging', 'Monitoring', 'Best Practices')
        },
        {
            'title': 'GraphQL Schema Designer',
            'description': 'Design efficient GraphQL schemas and resolvers',
            'content': '''# GraphQL Schema Design

Design a GraphQL schema for:

**Application:** [Describe your application]
**Data Entities:** [List main entities]
**Client Requirements:** [What data clients need]

Please provide:

1. **Type Definitions**
   - Object types
   - Input types
   - Enums
   - Interfaces
   - Unions

2. **Queries**
   - List queries
   - Single item queries
   - Nested queries
   - Pagination
   - Filtering
   - Sorting

3. **Mutations**
   - Create operations
   - Update operations
   - Delete operations
   - Batch operations

4. **Subscriptions** (if needed)
   - Real-time updates
   - Event subscriptions

5. **Resolvers**
   - Field resolvers
   - DataLoader for N+1 prevention
   - Error handling
   - Authorization

6. **Performance Optimization**
   - Query complexity analysis
   - Depth limiting
   - Rate limiting
   - Caching strategy

7. **Security**
   - Authentication
   - Authorization (field-level)
   - Input validation
   - Query cost analysis

8. **Documentation**
   - Schema descriptions
   - Deprecation notices
   - Usage examples

Provide:
- Complete schema definition
- Resolver implementations
- Example queries
- Best practices''',
            'use_case': 'Use when building GraphQL APIs, migrating from REST, or designing flexible data fetching layers.',
            'examples': '''**Example Schema:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}

input CreateUserInput {
  name: String!
  email: String!
}
```''',
            'difficulty': 'Advanced',
            'rating': 4.7,
            'category_id': get_cat('development').id,
            'tags': get_tags('GraphQL', 'API', 'Backend')
        },
        {
            'title': 'Load Testing Strategy',
            'description': 'Design and execute comprehensive load testing',
            'content': '''# Load Testing Plan

Create a load testing strategy for:

**Application:** [Your application]
**Type:** [Web API/Website/Mobile Backend]
**Expected Load:** [Concurrent users, requests/second]

**Testing Goals:**
- Baseline performance
- Identify bottlenecks
- Determine capacity limits
- Validate scalability

Please provide:

1. **Test Scenarios**
   - Normal load
   - Peak load
   - Stress test (beyond capacity)
   - Spike test (sudden traffic increase)
   - Soak test (sustained load)

2. **Metrics to Monitor**
   - Response time (p50, p95, p99)
   - Throughput (requests/second)
   - Error rate
   - CPU usage
   - Memory usage
   - Database connections
   - Network I/O

3. **Test Tools**
   - Tool selection (JMeter/Locust/k6/Artillery)
   - Configuration
   - Test scripts

4. **Test Data**
   - Realistic test data
   - Data generation strategy
   - Database seeding

5. **Execution Plan**
   - Ramp-up strategy
   - Duration
   - User distribution
   - Geographic distribution

6. **Analysis**
   - Performance baselines
   - Bottleneck identification
   - Optimization recommendations
   - Capacity planning

7. **Reporting**
   - Test results format
   - Graphs and charts
   - Executive summary
   - Technical details

Provide:
- Complete test scripts
- Execution commands
- Analysis methodology
- Optimization recommendations''',
            'use_case': 'Use before major launches, capacity planning, performance optimization, or SLA validation.',
            'examples': '''**Example: k6 Load Test**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 200 },  // Ramp to 200
    { duration: '5m', target: 200 },  // Stay at 200
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
};

export default function () {
  let response = http.get('https://api.example.com/users');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```''',
            'difficulty': 'Advanced',
            'rating': 4.8,
            'category_id': get_cat('testing').id,
            'tags': get_tags('Performance', 'Testing', 'DevOps')
        },
        {
            'title': 'Monorepo Setup Guide',
            'description': 'Set up and manage monorepo with multiple packages',
            'content': '''# Monorepo Configuration

Set up a monorepo for:

**Project Type:** [Frontend/Backend/Full-stack]
**Packages:** [List packages/apps]
**Build Tool:** [npm workspaces/Yarn workspaces/Lerna/Nx/Turborepo]

Please provide:

1. **Repository Structure**
   - Directory layout
   - Package organization
   - Shared code location

2. **Workspace Configuration**
   - Package manager setup
   - Workspace definitions
   - Dependency management

3. **Build System**
   - Build orchestration
   - Dependency graph
   - Incremental builds
   - Caching strategy

4. **Scripts**
   - Build all packages
   - Test all packages
   - Lint all packages
   - Version management
   - Publishing workflow

5. **Shared Dependencies**
   - Common dependencies
   - Version synchronization
   - Shared configurations (ESLint, TypeScript, etc.)

6. **CI/CD Integration**
   - Affected packages detection
   - Parallel builds
   - Deployment strategy

7. **Development Workflow**
   - Local development
   - Hot reloading
   - Debugging across packages

8. **Best Practices**
   - Code sharing patterns
   - Versioning strategy
   - Change management

Provide:
- Complete configuration files
- Directory structure
- Example package setup
- Common commands''',
            'use_case': 'Use when managing multiple related packages, shared component libraries, or microservices in a single repository.',
            'examples': '''**Example: npm Workspaces**
```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces",
    "lint": "npm run lint --workspaces"
  }
}

// Directory structure
my-monorepo/
├── packages/
│   ├── ui-components/
│   ├── utils/
│   └── api-client/
├── apps/
│   ├── web/
│   └── mobile/
└── package.json
```''',
            'difficulty': 'Advanced',
            'rating': 4.7,
            'category_id': get_cat('devops').id,
            'tags': get_tags('DevOps', 'CI/CD', 'Best Practices')
        }
    ]
    
    for prompt_data in prompts_data:
        # Check if prompt already exists
        existing = Prompt.query.filter_by(title=prompt_data['title']).first()
        if not existing:
            tags_to_add = prompt_data.pop('tags')
            prompt = Prompt(**prompt_data)
            prompt.tags = tags_to_add
            db.session.add(prompt)
    
    db.session.commit()
    print(f"✅ Created {len(prompts_data)} professional prompts")

def seed_database():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
    # Create categories
    print("📁 Creating categories...")
    categories = create_categories()
    print(f"✅ Created {len(categories)} categories")
    
    # Create tags
    print("🏷️  Creating tags...")
    tags = create_tags()
    print(f"✅ Created {len(tags)} tags")
    
    # Create prompts
    print("💡 Creating prompts...")
    create_prompts(categories, tags)
    
    print("✨ Database seeding completed successfully!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()

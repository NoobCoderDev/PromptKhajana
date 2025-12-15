# Prompt Khajana - Professional Prompt Library

A production-ready Flask application for managing and sharing AI prompts with role-based access control.

## Features

### Authentication & Authorization
- **User Registration & Login** with secure password hashing
- **Role-Based Access Control (RBAC)**
  - SuperAdmin: Full CRUD access to prompts, categories, and tags
  - Normal Users: View and copy prompts only
- Session-based authentication using Flask-Login
- Protected routes with decorators

### Prompt Management
- Create, Read, Update, Delete (CRUD) operations for SuperAdmins
- Rich prompt fields:
  - Title, Description, Content
  - Category, Tags, Difficulty Level
  - Use Cases, Examples
  - View Count, Rating
- Markdown rendering with syntax highlighting
- Copy-to-clipboard functionality

### Search & Filtering
- Full-text search across prompts
- Filter by category, tags, difficulty
- Sort by newest, popular, or rating
- Related prompts suggestions

### Admin Dashboard
- Statistics overview (total prompts, categories, tags)
- Manage prompts, categories, and tags
- Recent prompts listing

### UI/UX
- Modern, responsive design with Tailwind CSS
- Dark/Light mode toggle with localStorage persistence
- Professional gradient effects and animations
- Font Awesome icons
- Prism.js syntax highlighting

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login + Werkzeug password hashing
- **Frontend**: Jinja2 templates + Tailwind CSS
- **Markdown**: markdown2 with code-friendly extras
- **Syntax Highlighting**: Prism.js

## Installation

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python init_db.py
```

5. Run the application:
```bash
python run.py
```

6. Access at `http://127.0.0.1:5000`

## Default Credentials

### SuperAdmin
- Email: `admin@promptkhajana.com`
- Password: `admin123`

### Normal User
- Email: `user@example.com`
- Password: `user123`

## Project Structure

```
PromptKhajana/
├── app/
│   ├── __init__.py          # App factory and configuration
│   ├── models.py            # Database models
│   ├── routes.py            # Main routes (public)
│   ├── auth.py              # Authentication routes
│   ├── admin.py             # Admin routes (protected)
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Homepage
│   │   ├── view_prompt.html # Prompt detail page
│   │   ├── add_prompt.html  # Add prompt form
│   │   ├── edit_prompt.html # Edit prompt form
│   │   ├── category.html    # Category view
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── manage_prompts.html
│   │   │   ├── manage_categories.html
│   │   │   └── manage_tags.html
│   │   └── errors/
│   │       ├── 403.html
│   │       └── 404.html
│   └── static/
├── instance/
│   └── prompts.db           # SQLite database
├── init_db.py               # Database initialization script
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## Database Models

### User
- id, username, email, password_hash
- is_admin (Boolean for SuperAdmin role)
- created_at

### Category
- id, name, slug, description, icon
- created_at

### Tag
- id, name, slug
- created_at

### Prompt
- id, title, description, content
- use_case, examples, difficulty
- rating, views
- category_id (Foreign Key)
- tags (Many-to-Many)
- created_at, updated_at

## Routes

### Public Routes
- `/` - Homepage with search and filters
- `/prompt/<id>` - View single prompt
- `/category/<slug>` - View prompts by category
- `/api/prompts` - JSON API for prompts
- `/api/categories` - JSON API for categories

### Authentication Routes
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/logout` - User logout

### Admin Routes (SuperAdmin Only)
- `/admin/dashboard` - Admin dashboard
- `/admin/prompts` - Manage all prompts
- `/admin/categories` - Manage categories
- `/admin/tags` - Manage tags
- `/add` - Add new prompt
- `/edit/<id>` - Edit prompt
- `/delete/<id>` - Delete prompt

## Security Features

- Password hashing with Werkzeug
- CSRF protection (Flask default)
- Session-based authentication
- Role-based access control
- Protected admin routes with decorators
- HTTP 403 for unauthorized access
- Secure form handling

## Authorization Rules

### SuperAdmin Can:
- Create, update, delete prompts
- Manage categories and tags
- Access admin dashboard
- View all prompts

### Normal User Can:
- Register and login
- View all prompts
- Copy prompts
- Search and filter prompts
- **Cannot** create, update, or delete prompts
- **Cannot** access admin routes

## Environment Variables

Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///prompts.db
```

## Production Deployment

For production, use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## API Endpoints

### GET /api/prompts
Returns all prompts in JSON format

### GET /api/categories
Returns all categories with prompt counts

## Contributing

This is a professional implementation following Flask best practices:
- Modular blueprint structure
- Clean separation of concerns
- Secure authentication and authorization
- Production-ready error handling
- RESTful route naming

## License

MIT License

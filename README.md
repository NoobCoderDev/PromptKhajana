# Prompt Khajana 💎

A professional Flask-based web application for managing and discovering AI prompts tailored for software developers. Store, organize, search, and share high-quality prompts for development, testing, debugging, architecture, and more.

## ✨ Features

### Core Functionality
- **📚 Comprehensive Prompt Library** - 20+ professional developer prompts across 10 categories
- **🔍 Advanced Search & Filtering** - Search by keywords, filter by category, tags, and difficulty
- **📝 Markdown Support** - Rich text formatting with syntax highlighting for code blocks
- **📋 One-Click Copy** - Copy prompts to clipboard with a single click
- **🏷️ Tag System** - Organize prompts with multiple tags
- **⭐ Rating & Views** - Track popularity and engagement
- **🎯 Difficulty Levels** - Beginner, Intermediate, and Advanced classifications

### User Experience
- **🌓 Dark/Light Mode** - Beautiful themes with smooth transitions
- **📱 Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- **⚡ Fast & Smooth** - Optimized performance with elegant animations
- **🎨 Modern UI** - Gradient accents, glassmorphism, and premium design
- **♿ Accessible** - Semantic HTML and ARIA labels

### Technical Features
- **🗄️ SQLite Database** - Lightweight, file-based relational database
- **🔗 RESTful API** - JSON endpoints for programmatic access
- **🏗️ Clean Architecture** - Modular Flask blueprints
- **🔒 Secure** - Input validation and CSRF protection
- **📊 SEO Optimized** - Proper meta tags and semantic HTML

## 🛠️ Tech Stack

- **Backend**: Python 3.10+ with Flask 3.1
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Markdown**: markdown2 with syntax highlighting (Prism.js)
- **Deployment**: Gunicorn-ready

## 📂 Project Structure

```
prompt-khajana/
├── app/
│   ├── __init__.py          # App factory and configuration
│   ├── models.py            # Database models (Prompt, Category, Tag)
│   ├── routes.py            # Blueprint routes with search/filtering
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base template with dark mode
│   │   ├── index.html       # Homepage with search/filters
│   │   ├── view_prompt.html # Prompt detail page
│   │   ├── add_prompt.html  # Add new prompt form
│   │   ├── edit_prompt.html # Edit prompt form
│   │   └── category.html    # Category view
│   └── static/              # Static files (if needed)
├── seed_data.py             # Database seeding script
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd PromptKhajana
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Windows
   copy .env.example .env

   # Linux/Mac
   cp .env.example .env
   ```
   
   Edit `.env` and update the `SECRET_KEY` for production.

5. **Initialize the database and seed data**
   ```bash
   python seed_data.py
   ```
   
   This will:
   - Create all database tables
   - Add 10 categories (Development, Testing, Debugging, etc.)
   - Add 30+ tags (Python, JavaScript, API, etc.)
   - Seed 20 professional developer prompts

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage Guide

### Browsing Prompts
- Visit the homepage to see all prompts
- Use the search bar to find prompts by keywords
- Filter by category, tags, or difficulty level
- Sort by newest, most popular, or highest rated

### Viewing a Prompt
- Click on any prompt card to view details
- See the full prompt content with markdown rendering
- View use cases and examples
- Copy the prompt to clipboard with one click
- Check related prompts in the same category

### Adding a Prompt
1. Click "Add Prompt" in the navigation
2. Fill in the title, description, and content
3. Select category and difficulty level
4. Choose relevant tags
5. Optionally add use cases and examples
6. Submit to save

### Editing/Deleting
- Click "Edit" on any prompt detail page
- Update fields and save changes
- Delete prompts with confirmation

## 🎨 Categories

The application includes 10 predefined categories:

1. **💻 Development** - General software development prompts
2. **♻️ Refactoring** - Code refactoring and improvement
3. **🧪 Testing** - Unit, integration, and E2E testing
4. **🐛 Debugging** - Debugging and troubleshooting
5. **👁️ Code Review** - Code review and quality assurance
6. **🏗️ Architecture** - System design and architecture
7. **📚 Documentation** - Technical documentation
8. **⚡ Performance** - Performance optimization
9. **🔒 Security** - Security review and hardening
10. **🚀 DevOps** - CI/CD and deployment

## 🏷️ Sample Tags

Python, JavaScript, TypeScript, React, Node.js, Flask, Django, API, Database, SQL, NoSQL, Frontend, Backend, Full-Stack, Clean Code, Best Practices, Design Patterns, Microservices, REST, GraphQL, Docker, Kubernetes, AWS, Azure, GCP, Git, CI/CD, Monitoring, Logging, Error Handling

## 🔌 API Endpoints

### Get All Prompts (JSON)
```
GET /api/prompts
```

### Get All Categories (JSON)
```
GET /api/categories
```

Response includes prompt count for each category.

## 🌐 Deployment

### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Environment Variables for Production

```env
SECRET_KEY=your-strong-secret-key-here
DATABASE_URL=sqlite:///prompts.db
FLASK_ENV=production
FLASK_DEBUG=0
```

### Deployment Platforms

This application is ready to deploy on:
- **Heroku** - Use the included `wsgi.py`
- **Render** - Configure with gunicorn command
- **Railway** - Auto-detected Flask app
- **PythonAnywhere** - WSGI configuration included
- **DigitalOcean App Platform** - Buildpack support

## 🔧 Development

### Database Migrations

If you modify models, you can use Flask-Migrate:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

### Adding More Prompts

Edit `seed_data.py` and add your prompts to the `prompts_data` list, then run:

```bash
python seed_data.py
```

### Customizing Styles

The application uses Tailwind CSS via CDN. For custom styles:
- Edit the `<style>` section in `templates/base.html`
- Modify CSS variables for colors and themes
- Add custom classes as needed

## 🎯 Roadmap

- [ ] User authentication and profiles
- [ ] Prompt favorites/bookmarks
- [ ] Community ratings and reviews
- [ ] Prompt versioning
- [ ] Export prompts (JSON, Markdown)
- [ ] Import prompts from files
- [ ] Advanced analytics dashboard
- [ ] Prompt templates
- [ ] AI-powered prompt suggestions
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Flask and SQLAlchemy
- UI powered by Tailwind CSS
- Syntax highlighting by Prism.js
- Icons from Heroicons
- Fonts from Google Fonts (Inter)

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Made with ❤️ for developers by developers**

💎 **Prompt Khajana** - Your treasure trove of professional AI prompts

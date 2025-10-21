# Prompt Khajana

A Flask-based web application for managing and discovering AI prompts. Store, organize, and share your best prompts with ease.

## Features

- Browse all prompts with category filtering
- View detailed prompt information
- Add new prompts with examples and ratings
- Edit existing prompts
- Delete prompts
- Responsive design with Tailwind CSS
- SQLite database with Flask-SQLAlchemy
- Database migrations with Flask-Migrate

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login (setup included)
- **Migrations**: Flask-Migrate
- **Frontend**: HTML, Tailwind CSS
- **Deployment**: Gunicorn

## Project Structure

prompt-khajana/
├── app/
│ ├── init.py # App factory and config
│ ├── routes.py # Blueprint routes
│ ├── models.py # Database models
│ ├── templates/ # HTML templates
│ └── static/ # Static files
├── migrations/ # Database migrations
├── run.py # Application entry point
├── requirements.txt # Python dependencies
└── .env # Environment variables


## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```
git clone <your-repo-url>
cd prompt-khajana
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create environment file:
```
cp .env.example .env
```

5. Initialize the database:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```
python run.py
```

7. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Database Migrations

After making changes to models:
```
flask db migrate -m "Description of changes"
flask db upgrade
```

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///prompts.db
FLASK_ENV=development
```

## Deployment

This app is configured for deployment with Gunicorn. The `Procfile` is included for platforms like Heroku or Render.

## Future Enhancements

- User authentication and profiles
- Prompt search and filtering
- Category management
- Prompt sharing and exports
- Rating system
- Comments and feedback
- API endpoints
- Favorites/bookmarks

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License

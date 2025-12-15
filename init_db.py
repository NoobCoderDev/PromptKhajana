from app import create_app, db
from app.models import User, Category, Tag

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    
    existing_admin = User.query.filter_by(email='admin@promptkhajana.com').first()
    if not existing_admin:
        print("Creating superadmin user...")
        admin = User(
            username='admin',
            email='admin@promptkhajana.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Superadmin created: admin@promptkhajana.com / admin123")
    else:
        print("Superadmin already exists")
    
    existing_user = User.query.filter_by(email='user@example.com').first()
    if not existing_user:
        print("Creating normal user...")
        user = User(
            username='normaluser',
            email='user@example.com',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        print("Normal user created: user@example.com / user123")
    else:
        print("Normal user already exists")
    
    if Category.query.count() == 0:
        print("Creating default categories...")
        categories = [
            Category(name='Development', slug='development', description='Software development prompts', icon='fa-code'),
            Category(name='Testing', slug='testing', description='Testing and QA prompts', icon='fa-bug'),
            Category(name='Debugging', slug='debugging', description='Debugging assistance prompts', icon='fa-wrench'),
            Category(name='Refactoring', slug='refactoring', description='Code refactoring prompts', icon='fa-sync'),
            Category(name='Documentation', slug='documentation', description='Documentation writing prompts', icon='fa-file-alt'),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print(f"Created {len(categories)} categories")
    
    if Tag.query.count() == 0:
        print("Creating default tags...")
        tags = [
            Tag(name='Python', slug='python'),
            Tag(name='JavaScript', slug='javascript'),
            Tag(name='SQL', slug='sql'),
            Tag(name='API', slug='api'),
            Tag(name='Backend', slug='backend'),
            Tag(name='Frontend', slug='frontend'),
        ]
        for tag in tags:
            db.session.add(tag)
        db.session.commit()
        print(f"Created {len(tags)} tags")
    
    print("\nDatabase initialization complete!")
    print("\nLogin credentials:")
    print("SuperAdmin: admin@promptkhajana.com / admin123")
    print("Normal User: user@example.com / user123")

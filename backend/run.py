"""
Application entry point for InterPrep-AI Next Generation.
"""
import os
from app import create_app
from app.extensions import db
from flask_migrate import Migrate

# Create Flask application
app = create_app(os.getenv('FLASK_CONFIG', 'development'))
migrate = Migrate(app, db)

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command('seed-db')
def seed_db():
    """Seed the database with initial data."""
    from app.models import (
        User, UserProfile, 
        LearningCategory, LearningTopic, LearningContent
    )
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )
    db.session.add(admin)
    db.session.flush()
    
    # Create admin profile
    profile = UserProfile(
        user_id=admin.id,
        full_name='Admin User',
        bio='System administrator'
    )
    db.session.add(profile)
    
    # Create learning categories based on "Cracking the Coding Interview"
    categories = [
        {
            'name': 'Arrays and Strings',
            'description': 'Fundamental data structures for storing collections of elements',
            'order': 1
        },
        {
            'name': 'Linked Lists',
            'description': 'Linear data structures where elements are stored in nodes',
            'order': 2
        },
        {
            'name': 'Stacks and Queues',
            'description': 'Abstract data types with specific access patterns',
            'order': 3
        },
        {
            'name': 'Trees and Graphs',
            'description': 'Non-linear data structures representing hierarchical relationships',
            'order': 4
        },
        {
            'name': 'Bit Manipulation',
            'description': 'Operations at the bit level of numeric representations',
            'order': 5
        },
        {
            'name': 'Math and Logic Puzzles',
            'description': 'Mathematical problems and logical reasoning',
            'order': 6
        },
        {
            'name': 'Object-Oriented Design',
            'description': 'Principles and patterns of object-oriented programming',
            'order': 7
        },
        {
            'name': 'Recursion and Dynamic Programming',
            'description': 'Techniques for solving problems by breaking them down',
            'order': 8
        },
        {
            'name': 'System Design and Scalability',
            'description': 'Designing large-scale distributed systems',
            'order': 9
        }
    ]
    
    # Add categories and topics
    for category_data in categories:
        category = LearningCategory(
            name=category_data['name'],
            description=category_data['description'],
            order=category_data['order']
        )
        db.session.add(category)
    
    db.session.commit()
    print('Database seeded with initial data.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

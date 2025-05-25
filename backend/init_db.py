# """
# Database initialization script for InterPrep-AI Next Generation.
# """
# from dotenv import load_dotenv
# from pathlib import Path
# import sys
# import os

# # Dynamically load the .env from the **root project directory**
# env_path = Path(__file__).resolve().parent.parent / ".env"
# load_dotenv(dotenv_path=env_path)

# # Add backend/ to sys.path so imports work
# sys.path.append(str(Path(__file__).resolve().parent))


# from app import create_app
# from app.extensions import db
# from app.models import User, UserProfile, Question, Submission, Favorite, PracticeHistory
# from app.models import LearningCategory, LearningTopic, LearningContent, LearningProgress

# # Create the Flask app
# app = create_app('development')

# # Create the database tables
# with app.app_context():
#     print("Creating database tables...")
#     db.create_all()
#     print("Database tables created successfully!")
    
#     # Check if we need to seed initial data
#     if User.query.count() == 0:
#         print("Seeding initial data...")
        
#         # Create admin user
#         admin = User(
#             username='admin',
#             email='admin@example.com',
#             password='adminpassword'
#         )
#         db.session.add(admin)
#         db.session.flush()
        
#         # Create learning categories based on "Cracking the Coding Interview"
#         categories = [
#             {
#                 'name': 'Arrays and Strings',
#                 'description': 'Fundamental data structures for storing collections of elements',
#                 'order': 1
#             },
#             {
#                 'name': 'Linked Lists',
#                 'description': 'Linear data structures where elements are stored in nodes',
#                 'order': 2
#             },
#             {
#                 'name': 'Stacks and Queues',
#                 'description': 'Abstract data types with specific access patterns',
#                 'order': 3
#             },
#             {
#                 'name': 'Trees and Graphs',
#                 'description': 'Non-linear data structures representing hierarchical relationships',
#                 'order': 4
#             },
#             {
#                 'name': 'Bit Manipulation',
#                 'description': 'Operations at the bit level of numeric representations',
#                 'order': 5
#             },
#             {
#                 'name': 'Math and Logic Puzzles',
#                 'description': 'Mathematical problems and logical reasoning',
#                 'order': 6
#             },
#             {
#                 'name': 'Object-Oriented Design',
#                 'description': 'Principles and patterns of object-oriented programming',
#                 'order': 7
#             },
#             {
#                 'name': 'Recursion and Dynamic Programming',
#                 'description': 'Techniques for solving problems by breaking them down',
#                 'order': 8
#             },
#             {
#                 'name': 'System Design and Scalability',
#                 'description': 'Designing large-scale distributed systems',
#                 'order': 9
#             }
#         ]
        
#         for category_data in categories:
#             category = LearningCategory(
#                 name=category_data['name'],
#                 description=category_data['description'],
#                 order=category_data['order']
#             )
#             db.session.add(category)
        
#         db.session.commit()
#         print("Initial data seeded successfully!")
    
#     print("Database initialization complete!")


"""
Database initialization script for InterPrep-AI Next Generation.
"""
from dotenv import load_dotenv
from pathlib import Path
import sys
import os

# Load environment variables from the .env file in the project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Add backend/ to sys.path so app imports work
sys.path.append(str(Path(__file__).resolve().parent))

from app import create_app
from app.extensions import db
from app.models import User, UserProfile, Question, Submission, Favorite, PracticeHistory
from app.models import LearningCategory, LearningTopic, LearningContent, LearningProgress

# Create the Flask app using development config
app = create_app('development')

with app.app_context():
    print("🛠️  Creating database tables...")
    db.create_all()
    print("✅ Database tables created successfully!")

    if User.query.count() == 0:
        print("🔐 Seeding admin user and categories...")

       # Create admin user
        admin = User('admin', 'admin@example.com', 'adminpassword')
        if hasattr(admin, 'set_password'):
            admin.set_password('adminpassword')
        else:
            admin.password = 'adminpassword'  # fallback if no method
        db.session.add(admin)
        db.session.flush()

        # Define core learning categories
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

        # Add categories if they don’t already exist
        for cat in categories:
            existing = LearningCategory.query.filter_by(name=cat['name']).first()
            if not existing:
                category = LearningCategory(
                    name=cat['name'],
                    description=cat['description'],
                    order=cat['order']
                )
                db.session.add(category)

        db.session.commit()
        print("🚀 Admin user and learning categories seeded!")

    else:
        print("ℹ️  Admin already exists. Skipping seeding.")

    print("🎉 Database initialization complete!")
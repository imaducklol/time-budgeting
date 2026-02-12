import requests
import random
from faker import Faker
import json
from typing import List, Dict
import time

fake = Faker()

# Configuration
NUM_USERS = 100
NUM_BUDGETS = 3
NUM_GROUPS = 3
NUM_CATEGORIES = 5
NUM_TRANSACTIONS = 15

# Sample data generators
def generate_budget_name():
    budget_types = ["Personal", "Work", "Project", "Team", "Department"]
    contexts = ["Weekly", "Monthly", "Sprint", "Q1", "Q2", "Q3", "Q4", "2024", "2025"]
    return f"{random.choice(budget_types)} {random.choice(contexts)} Budget"

def generate_group_name():
    groups = [        'Reading', 'Exercise', 'Creative Arts', 'Cooking', 'Outdoors',
        'Gaming', 'Work', 'Mindfulness', 'Gaming', 'Social']
    return random.choice(groups)

def generate_category_name():
    categories = ["Fiction", "Non-fiction", "Poetry", "Graphic novels", "Running", "Weightlifting", "Yoga", "Cycling", "Drawing", "Painting", "Writing", "Playing an instrument", "Baking", "Cooking new cuisines", "Meal prepping", "Language learning", "Coding", "Photography", "Hiking", "Gardening", "Birdwatching", "Volunteering", "Board games", "Video games", "Puzzles", "Meditation", "Journaling", "Deep breathing exercises", "Local sightseeing", "Road trips"]
    return random.choice(categories)

def generate_transaction_name():
    actions = [
        "Read", 
        "Practiced", 
        "Created", 
        "Cooked", 
        "Learned", 
        "Explored", 
        "Played", 
        "Meditated", 
        "Planned", 
        "Photographed"
    ]

    subjects = [
        "fiction book", 
        "non-fiction article", 
        "poem", 
        "painting", 
        "recipe", 
        "new language", 
        "exercise routine", 
        "board game", 
        "puzzle", 
        "local landmark"
    ]
    return f"{random.choice(actions)} {random.choice(subjects)}"

def generate_time_allocated():
    # Between 30 minutes and 8 hours
    hours = random.randint(0, 8)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def generate_time_period():
    # Between 5 minutes and 4 hours
    hours = random.randint(0, 4)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



def generate_sql_inserts(output_file="populate_budget_data.sql"):
    """Generates SQL INSERT statements for bulk loading"""
    
    print("Generating SQL inserts...")
    
    with open(output_file, 'w') as f:
        # Start transaction for performance
        f.write("BEGIN TRANSACTION;\n\n")
        
        user_id = 1
        budget_id = 1
        group_id = 1
        category_id = 1
        transaction_id = 1
        
        # Generate users
        f.write("-- Inserting users\n")
        for u in range(NUM_USERS):
            username = fake.name().replace("'", "''")
            email = fake.email()
            f.write(f"INSERT INTO \"user\" (user_id, username, email) VALUES ({user_id}, '{username}', '{email}');\n")
            
            # Generate budgets for this user
            for b in range(NUM_BUDGETS):
                budget_name = generate_budget_name().replace("'", "''")
                f.write(f"INSERT INTO \"budget\" (budget_id, user_id, budget_name) VALUES ({budget_id}, {user_id}, '{budget_name}');\n")
                
                # Generate groups for this budget
                for g in range(NUM_GROUPS):
                    group_name = generate_group_name().replace("'", "''")
                    f.write(f"INSERT INTO \"group\" (group_id, budget_id, group_name) VALUES ({group_id}, {budget_id}, '{group_name}');\n")
                    
                    # Generate categories for this group
                    for c in range(NUM_CATEGORIES):
                        category_name = generate_category_name().replace("'", "''")
                        time_allocated = generate_time_allocated()
                        f.write(f"INSERT INTO \"category\" (category_id, budget_id, group_id, category_name, time_allocated) VALUES ({category_id}, {budget_id}, {group_id}, '{category_name}', INTERVAL '{time_allocated}');\n")
                        
                        # Generate transactions for this category
                        for t in range(NUM_TRANSACTIONS):
                            transaction_name = generate_transaction_name().replace("'", "''")
                            period = generate_time_period()
                            f.write(f"INSERT INTO \"transaction\" (transaction_id, category_id, transaction_name, period) VALUES ({transaction_id}, {category_id}, '{transaction_name}', INTERVAL '{period}');\n")
                            transaction_id += 1
                        
                        category_id += 1
                    group_id += 1
                budget_id += 1
            
            user_id += 1
            if (u + 1) % 10 == 0:
                print(f"Generated SQL for {u + 1}/{NUM_USERS} users...")
        
        f.write("\nCOMMIT;\n")
    
    total_records = (user_id - 1) + (budget_id - 1) + (group_id - 1) + (category_id - 1) + (transaction_id - 1)
    print(f"\nSQL generation complete!")
    print(f"Total records: {total_records:,}")
    print(f"  Users: {NUM_USERS:,}")
    print(f"  Budgets: {(budget_id - 1):,}")
    print(f"  Groups: {(group_id - 1):,}")
    print(f"  Categories: {(category_id - 1):,}")
    print(f"  Transactions: {(transaction_id - 1):,}")
    print(f"\nOutput file: {output_file}")
    print(f"To execute: psql -U username -d database_name -f {output_file}")
    print(f"Or: mysql -u username -p database_name < {output_file}")

if __name__ == "__main__":    
    generate_sql_inserts()
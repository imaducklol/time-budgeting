import requests
from faker import Faker
import random
from typing import Dict, Any
import time

fake = Faker()

CONFIG = {
    'base_url': 'http://127.0.0.1:5000/api', 
    'num_users': 100,
    'num_budgets_per_user': 3,
    'num_groups_per_budget': 10,
    'num_categories_per_group': 10,
    'num_transactions_per_category': 15,
    'delay_between_requests': 0.00
}

def log_progress(message: str):
    """Print progress with timestamp"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def post_request(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make POST request and return response JSON"""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        time.sleep(CONFIG['delay_between_requests'])
        return response.json()
    except requests.exceptions.RequestException as e:
        log_progress(f"Error posting to {url}: {e}")
        raise

def generate_users(num_users: int) -> list:
    """Generate and post users, return list of user IDs"""
    log_progress(f"Creating {num_users} users...")
    user_ids = []
    
    for i in range(num_users):
        user_data = {
            'username': fake.name(),
            'email': fake.email()
        }
        
        url = f"{CONFIG['base_url']}/users"
        response = post_request(url, user_data)
        user_id = response.get('id') or response.get('user_id')
        user_ids.append(user_id)
        
        if (i + 1) % 10 == 0:
            log_progress(f"  Created {i + 1}/{num_users} users")
    
    log_progress(f"✓ Completed creating {num_users} users")
    return user_ids

def generate_budgets(user_id: int, num_budgets: int) -> list:
    """Generate and post budgets for a user, return list of budget IDs"""
    budget_ids = []
    budget_categories = [
        'Personal', 'Work', 'Project', 'Team', 'Department',
        'Annual', 'Monthly', 'Weekly', 'Q1', 'Q2', 'Q3', 'Q4'
    ]
    
    for i in range(num_budgets):
        budget_data = {
            'budget_name': f"{random.choice(budget_categories)} Budget {fake.word().capitalize()}"
        }
        
        url = f"{CONFIG['base_url']}/users/{user_id}/budgets"
        response = post_request(url, budget_data)
        budget_id = response.get('budget_id')
        budget_ids.append(budget_id)
    
    return budget_ids

def generate_groups(user_id: int, budget_id: int, num_groups: int) -> list:
    """Generate and post groups for a budget, return list of group IDs"""
    group_ids = []
    group_types = [
        'Reading', 'Exercise', 'Creative Arts', 'Cooking', 'Outdoors',
        'Gaming', 'Work', 'Mindfulness', 'Gaming', 'Social'
    ]
    
    for i in range(num_groups):
        group_data = {
            'group_name': f"{random.choice(group_types)}"
        }
        
        url = f"{CONFIG['base_url']}/users/{user_id}/budgets/{budget_id}/groups"
        response = post_request(url, group_data)
        group_id = response.get('group_id')
        group_ids.append(group_id)
    
    return group_ids

def generate_categories(user_id: int, budget_id: int, group_id: int, num_categories: int) -> list:
    """Generate and post categories for a group, return list of category IDs"""
    category_ids = []
    category_names = [
        "Fiction", "Non-fiction", "Poetry", "Graphic novels", "Running", "Weightlifting", "Yoga", "Cycling", "Drawing", "Painting", "Writing", "Playing an instrument", "Baking", "Cooking new cuisines", "Meal prepping", "Language learning", "Coding", "Photography", "Hiking", "Gardening", "Birdwatching", "Volunteering", "Board games", "Video games", "Puzzles", "Meditation", "Journaling", "Deep breathing exercises", "Local sightseeing", "Road trips"
    ]
    
    for i in range(num_categories):
        time_allocated = random.randint(1*60*60, 20 * 60 * 60)
        
        category_data = {
            'category_name': f"{random.choice(category_names)}",
            'time_allocated': time_allocated,
            'group_id': group_id
        }
        
        url = f"{CONFIG['base_url']}/users/{user_id}/budgets/{budget_id}/categories"
        response = post_request(url, category_data)
        category_id = response.get('id') or response.get('category_id')
        category_ids.append(category_id)
    
    return category_ids

def generate_transactions(user_id: int, budget_id: int, category_id: int, num_transactions: int):
    """Generate and post transactions for a category"""
    transaction_types = [
        'Task', 'Meeting', 'Session', 'Activity', 'Sprint',
        'Review', 'Call', 'Workshop', 'Training', 'Discussion'
    ]
    
    for i in range(num_transactions):
        # Period between 15 minutes and 8 hours (in seconds)
        period = random.randint(900, 28800)
        
        transaction_data = {
            'transaction_name': f"{random.choice(transaction_types)}: {fake.sentence(nb_words=4)}",
            'period': period
        }
        
        url = f"{CONFIG['base_url']}/users/{user_id}/budgets/{budget_id}/categories/{category_id}/transactions"
        post_request(url, transaction_data)

def main():
    """Main function to generate all test data"""
    start_time = time.time()
    
    # Calculate total API calls
    total_calls = (
        CONFIG['num_users'] +
        CONFIG['num_users'] * CONFIG['num_budgets_per_user'] +
        CONFIG['num_users'] * CONFIG['num_budgets_per_user'] * CONFIG['num_groups_per_budget'] +
        CONFIG['num_users'] * CONFIG['num_budgets_per_user'] * CONFIG['num_groups_per_budget'] * CONFIG['num_categories_per_group'] +
        CONFIG['num_users'] * CONFIG['num_budgets_per_user'] * CONFIG['num_groups_per_budget'] * CONFIG['num_categories_per_group'] * CONFIG['num_transactions_per_category']
    )
    
    log_progress(f"Starting data generation...")
    log_progress(f"Total API calls to make: {total_calls:,}")
    log_progress(f"Estimated time: {(total_calls * CONFIG['delay_between_requests']) / 60:.1f} minutes")
    
    # Generate users
    user_ids = generate_users(CONFIG['num_users'])
    
    # For each user, generate budgets
    for user_idx, user_id in enumerate(user_ids):
        log_progress(f"Processing user {user_idx + 1}/{len(user_ids)} (ID: {user_id})...")
        
        budget_ids = generate_budgets(user_id, CONFIG['num_budgets_per_user'])
        
        # For each budget, generate groups
        for budget_idx, budget_id in enumerate(budget_ids):
            if budget_idx % 10 == 0:
                log_progress(f"  Budget {budget_idx + 1}/{len(budget_ids)}...")
            
            group_ids = generate_groups(user_id, budget_id, CONFIG['num_groups_per_budget'])
            
            # For each group, generate categories
            for group_id in group_ids:
                category_ids = generate_categories(
                    user_id, budget_id, group_id, 
                    CONFIG['num_categories_per_group']
                )
                
                # For each category, generate transactions
                for category_id in category_ids:
                    generate_transactions(
                        user_id, budget_id, category_id,
                        CONFIG['num_transactions_per_category']
                    )
    
    elapsed_time = time.time() - start_time
    log_progress(f"\n✓ All done! Total time: {elapsed_time / 60:.1f} minutes")
    log_progress(f"Total records created: {total_calls:,}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("API Test Data Generator")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Base URL: {CONFIG['base_url']}")
    print(f"  Users: {CONFIG['num_users']}")
    print(f"  Budgets per user: {CONFIG['num_budgets_per_user']}")
    print(f"  Groups per budget: {CONFIG['num_groups_per_budget']}")
    print(f"  Categories per group: {CONFIG['num_categories_per_group']}")
    print(f"  Transactions per category: {CONFIG['num_transactions_per_category']}")
    print("\n" + "="*60 + "\n")
    
    confirm = input("This will make a LOT of API calls. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        main()
    else:
        print("Cancelled.")
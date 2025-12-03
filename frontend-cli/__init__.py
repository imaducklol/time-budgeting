"""
Author: Orion Hess
Created: 2025-12-3
Updated: 2025-12-3

Dead simple frontend
"""

def get_input():
    print("Choose an option:")
    print("0 - Exit")
    print("1 - List users")
    print("2 - Show user info")
    return input("Selection: ")

def user_list():
    pass

def user_info():
    pass

def user_create():
    pass

def main():
    running = True
    while running:
        user_input = get_input()
        match user_input.lower():
            case '0':
                running = False
            case '1':
                user_list()
            case '2':
                user_info()
            case '3':
                user_create()
            case '4':
                print("Not implemented")
        print("\n\n")

if __name__ == "__main__":
    main()

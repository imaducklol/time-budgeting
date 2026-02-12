"""
Author: Orion Hess
Created: 2025-12-3
Updated: 2025-12-3

Dead simple frontend
"""


import view
from model import Model


def main():
    model = Model("http://localhost:5000", debug_mode=False)
    while True:
        current_screen = model.get_screen()
        current_screen.display()
        current_screen.options()


if __name__ == "__main__":
    main()

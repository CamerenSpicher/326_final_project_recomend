"""
restaurant_recommender.py

A restaurant recommendation system based on user preferences.
"""

import csv

class Restaurant:
    """
    A class representing a restaurant.

    Attributes:
        name (str): Name of the restaurant.
        category (str): Type of cuisine.
        address (str): Location address.
        avg_price (float): Average meal price.
        dietary_options (list): List of supported dietary options.
        ambiance (str): Type of dining environment.
        description (str): Short description of the restaurant.
    """

    def __init__(self, name, category, address, avg_price, dietary_options, ambiance, description):
        self.name = name
        self.category = category
        self.address = address
        self.avg_price = float(avg_price.replace('$', '').strip())
        self.dietary_options = [opt.strip().lower() for opt in dietary_options.split(',')]
        self.ambiance = ambiance
        self.description = description

    def matches_preferences(self, preferences):
        """
        Checks if the restaurant matches the given user preferences.

        Args:
            preferences (dict): Dictionary of user preferences.

        Returns:
            bool: True if the restaurant matches preferences.
        """
        # Dietary match
        if preferences['diet'].lower() in ['no', '', 'any']:
            diet_match = True
        else:
            diet_match = preferences['diet'].lower() in self.dietary_options

        # Max price match
        if isinstance(preferences['max_price'], (int, float)):
            price_match = self.avg_price <= preferences['max_price']
        else:
            price_match = True

        # Category match
        if preferences['category'].lower() in ['no', '', 'any']:
            category_match = True
        else:
            category_match = preferences['category'].lower() == self.category.lower()

        # Ambiance match
        if preferences['ambiance'].lower() in ['no', '', 'any']:
            ambiance_match = True
        else:
            ambiance_match = preferences['ambiance'].lower() == self.ambiance.lower()

        return diet_match and price_match and category_match and ambiance_match

    def __repr__(self):
        return f"{self.name} ({self.category}) - ${self.avg_price:.2f} - {self.description}\n {self.address}"


def load_restaurants_from_csv(csv_path):
    """
    Loads restaurants from a CSV file.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        list: A list of Restaurant objects.
    """
    restaurants = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    restaurant = Restaurant(
                        row['Name'],
                        row['Category'],
                        row['Address'],
                        row['Avg Meal Price'],
                        row['Dietary Options'],
                        row['Ambiance'],
                        row['Description']
                    )
                    restaurants.append(restaurant)
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
    except FileNotFoundError:
        print("CSV file not found.")
    return restaurants


def get_user_preferences():
    """
    Gets user preferences from command line input.

    Returns:
        dict: User preferences.
    """
    print("Welcome to the College Park Restaurant Recommender!\n")

    category = input("Enter preferred cuisine category (e.g., Mexican, Pizza, Any): ").strip()
    diet = input("Enter your dietary restriction (e.g., Vegan, Gluten-Free, No): ").strip()
    max_price_input = input("Enter your maximum meal price (e.g., 15.00 or press Enter to skip): ").strip()
    ambiance = input("Preferred ambiance (Casual, Upscale, Family-Friendly, Any): ").strip()

    try:
        max_price = float(max_price_input)
    except ValueError:
        max_price = None

    return {
        'category': category,
        'diet': diet,
        'max_price': max_price,
        'ambiance': ambiance
    }


def recommend_restaurants(restaurants, preferences):
    """
    Filters and recommends restaurants based on preferences.

    Args:
        restaurants (list): List of Restaurant objects.
        preferences (dict): User preferences.

    Returns:
        list: Matching Restaurant objects.
    """
    return [r for r in restaurants if r.matches_preferences(preferences)]


if __name__ == "__main__":
    csv_path = "college_park_restaurants_detailed.csv"
    restaurants = load_restaurants_from_csv(csv_path)

    if not restaurants:
        print("No restaurants loaded. Check your CSV file.")
    else:
        preferences = get_user_preferences()
        matches = recommend_restaurants(restaurants, preferences)

        print(f"\nRecommended restaurants for your preferences:")
        if matches:
            for r in matches:
                print(f"- {r}")
        else:
            print("No matching restaurants found.")
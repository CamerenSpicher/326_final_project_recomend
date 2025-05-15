import unittest
from restaurant_recommender import Restaurant, recommend_restaurants

class TestRestaurant(unittest.TestCase):
    """
    Unit tests for the Restaurant class and recommend_restaurants function.
    These tests verify all logic branches in the matching algorithm under expected inputs.
    """

    def setUp(self):
        """Set up sample Restaurant objects for use in tests."""
        self.r1 = Restaurant("Old Maryland Grill", "American", "7777 Baltimore Ave", "$35", "Gluten-Free", "Casual Dining", "Upscale eatery offering regional American fare.")
        self.r2 = Restaurant("Bagels 'n Grinds", "Cafe", "7777 Baltimore Ave", "$10", "Vegan, Gluten-Free", "Casual Dining", "Breakfast cafe known for bagels & coffee.")
        self.r3 = Restaurant("Potomac Pizza", "Pizza", "7777 Baltimore Ave", "$15", "Gluten-Free", "Family-Friendly", "Family-friendly pizzeria serving classic pies.")
        self.r4 = Restaurant("Iron Rooster", "American", "7777 Baltimore Ave", "$20", "Vegetarian Options", "Casual Dining", "All-day breakfast & comfort food spot.")
        self.restaurants = [self.r1, self.r2, self.r3, self.r4]

    def test_price_matching(self):
        """Test that restaurants are filtered correctly by maximum price."""
        prefs = {'category': 'Any', 'diet': 'Any', 'max_price': 15, 'ambiance': 'Any'}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertIn(self.r2, matches)
        self.assertIn(self.r3, matches)
        self.assertNotIn(self.r1, matches)

    def test_dietary_restriction_match(self):
        """Test matching on dietary restrictions (e.g., vegan)."""
        prefs = {'category': 'Any', 'diet': 'Vegan', 'max_price': 50, 'ambiance': 'Any'}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertIn(self.r2, matches)
        self.assertNotIn(self.r3, matches)

    def test_category_matching(self):
        """Test filtering based on cuisine category."""
        prefs = {'category': 'Pizza', 'diet': 'Any', 'max_price': 50, 'ambiance': 'Any'}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertEqual(matches, [self.r3])

    def test_ambiance_matching(self):
        """Test filtering based on ambiance."""
        prefs = {'category': 'Any', 'diet': 'Any', 'max_price': 50, 'ambiance': 'Family-Friendly'}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertEqual(matches, [self.r3])

    def test_all_preferences_match(self):
        """Test that a restaurant must match all user preferences to be returned."""
        prefs = {
            'category': 'American',
            'diet': 'Vegetarian Options',
            'max_price': 25,
            'ambiance': 'Casual Dining'
        }
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertEqual(matches, [self.r4])

    def test_skipped_preferences(self):
        """Test behavior when user skips preferences (e.g., enters 'No' or '')."""
        prefs = {'category': '', 'diet': 'No', 'max_price': 100, 'ambiance': ''}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertEqual(set(matches), set(self.restaurants))

    def test_no_matches(self):
        """Test that empty list is returned when no restaurants match."""
        prefs = {'category': 'Greek', 'diet': 'Keto', 'max_price': 5, 'ambiance': 'Upscale'}
        matches = recommend_restaurants(self.restaurants, prefs)
        self.assertEqual(matches, [])

if __name__ == '__main__':
    unittest.main()

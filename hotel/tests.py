"""
Hotel App Tests
"""

from datetime import date, timedelta
from common.models import Country, City, Hotel, Room
from common.tests import BaseModelTest


class HotelModelTest(BaseModelTest):
    """
    Tests for the Hotel model.
    This test case includes the following tests:
    - `test_rooms`: Verifies that the correct number of rooms associated with the hotel is returned and are the ones created in the setup.
    - `test_hotel_str`: Checks the string representation of the hotel.
    - `test_hotel_country`: Ensures that the hotel is associated with the correct country.
    Setup:
    - Creates a country, city, hotel, and two rooms associated with the hotel.
    Attributes:
    - `country`: The country instance created for testing.
    - `city`: The city instance created for testing.
    - `hotel`: The hotel instance created for testing.
    - `room1`: The first room instance created for testing.
    - `room2`: The second room instance created for testing.
    """

    def setUp(self):
        """
        Set up the test environment by creating a country, city, hotel, and rooms.
        This method performs the following actions:
        - Creates a country named "Test Country".
        - Creates a city named "Test City" associated with the created country.
        - Creates a hotel named "Test Hotel" in the created city with a rating of 4.5.
        - Creates two rooms associated with the created hotel:
            - Room 1: Single room type, available from 2023-01-01 to 2023-01-05, costing 100.0.
            - Room 2: Double room type, available from 2023-01-01 to 2023-01-05, costing 200.0.
        """
        # Create a country
        self.country = Country.objects.create(name="Test Country")

        # Create a city
        self.city = City.objects.create(name="Test City", country=self.country)

        # Create a hotel
        self.hotel = Hotel.objects.create(name="Test Hotel", city=self.city, rating=4.5)

        # Create rooms associated with the hotel
        self.room1 = Room.objects.create(
            hotel=self.hotel,
            room_type="Single",
            from_date="2023-01-01",
            to_date="2023-01-05",
            cost=100.0,
        )
        self.room2 = Room.objects.create(
            hotel=self.hotel,
            room_type="Double",
            from_date="2023-01-01",
            to_date="2023-01-05",
            cost=200.0,
        )

    def test_rooms(self):
        """
        Test the retrieval of rooms associated with a hotel.
        This test verifies that:
        1. The correct number of rooms is returned.
        2. The rooms returned are the ones that were created.
        Assertions:
        - The count of rooms should be 2.
        - The specific rooms created (room1 and room2) should be in the retrieved rooms.
        """
        rooms = self.hotel.rooms
        self.assertEqual(rooms.count(), 2)
        self.assertIn(self.room1, rooms)
        self.assertIn(self.room2, rooms)

    def test_hotel_str(self):
        """
        Test the string representation of the Hotel model.

        This test ensures that the __str__ method of the Hotel model
        returns the correct string representation, which in this case
        should be "Test Hotel".
        """
        self.assertEqual(str(self.hotel), "Test Hotel")

    def test_hotel_country(self):
        """
        Test case to verify that the country attribute of the hotel object
        matches the expected country value.
        """
        self.assertEqual(self.hotel.country, self.country)


class RoomModelTest(BaseModelTest):
    """
    Unit tests for the Room model.
    Tests included:
    - Room creation and attribute validation.
    - String representation of the Room instance.
    - Calculation of room duration in days.
    - Calculation of room cost per day.
    Test Cases:
    - `test_room_creation`: Verifies that a Room instance is created with the correct attributes.
    - `test_room_str`: Checks the string representation of the Room instance.
    - `test_room_duration_in_days`: Ensures the duration in days is calculated correctly.
    - `test_room_cost_per_day`: Confirms the cost per day is calculated correctly.
    Setup:
    - Creates instances of Country, City, Hotel, and Room for testing.
    """

    def setUp(self):
        """
        Set up the test environment for TravelPlanner application.

        This method creates the following objects:
        - A `Country` object with the name "TestCountry".
        - A `City` object with the name "TestCity" associated with the created `Country`.
        - A `Hotel` object with the name "TestHotel", located in the created `City`, and with a rating of 4.0.
        - A `Room` object in the created `Hotel`, with the type "Single", available from today's date to 5 days later, and costing 500.0.
        """
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)
        self.hotel = Hotel.objects.create(name="TestHotel", city=self.city, rating=4.0)
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_type="Single",
            from_date=date.today(),
            to_date=date.today() + timedelta(days=5),
            cost=500.0,
        )

    def test_room_creation(self):
        """
        Test the creation of a room.

        This test verifies that a room is created with the correct attributes:
        - The room is associated with the correct hotel.
        - The room type is set to "Single".
        - The cost of the room is set to 500.0.
        """
        self.assertEqual(self.room.hotel, self.hotel)
        self.assertEqual(self.room.room_type, "Single")
        self.assertEqual(self.room.cost, 500.0)

    def test_room_str(self):
        """
        Test the string representation of the room.

        This test checks if the string representation of the room object
        matches the expected format, which includes the hotel name and
        the room type (e.g., "HotelName - Single").
        """
        self.assertEqual(str(self.room), f"{self.hotel.name} - Single")

    def test_room_duration_in_days(self):
        """
        Test that the duration in days for a room is correctly calculated.

        This test checks if the `duration_in_days` attribute of the `room` object
        returns the expected value of 5 days.
        """
        self.assertEqual(self.room.duration_in_days, 5)

    def test_room_cost_per_day(self):
        """
        Test the cost per day of the room.

        This test checks if the cost per day of the room is equal to 100.0.
        """
        self.assertEqual(self.room.cost_per_day, 100.0)

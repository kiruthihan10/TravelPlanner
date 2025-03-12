from django.test import TestCase
from .models import (
    Country,
    City,
    Sightseeing,
    Hotel,
    Room,
    Airport,
    Flight,
    Plan,
    FlightPlan,
    SightseeingPlan,
)
from datetime import date, datetime, timedelta


class CountryModelTest(TestCase):
    """
    Tests for the Country model and its associations with plans.
    Classes:
        CountryModelTest: Test case for the Country model.
    Methods:
        setUp(self):
            Set up test data for the test case.
        test_plans_associated_with_country(self):
            Test that plans are correctly associated with the country.
        test_string(self):
            Test the string representation of the country.
    """

    def setUp(self):
        """
        Set up test data for TravelPlanner application.

        This method creates:
        - Three countries: Country1, Country2, Country3
        - Two plans: Plan1 (version 1), Plan2 (version 1)
        - Three airports: Airport1 (in Country1), Airport2 (in Country2), Airport3 (in Country3)
        - Two flights:
            - Flight1: from Airport1 to Airport3, cost 100.0, departure on 2023-01-01 at 10:00, arrival on 2023-01-01 at 12:00
            - Flight2: from Airport3 to Airport2, cost 150.0, departure on 2023-01-02 at 10:00, arrival on 2023-01-02 at 12:00
        - Two flight plans:
            - FlightPlan1: associated with Flight1 and Plan1, order 1
            - FlightPlan2: associated with Flight2 and Plan2, order 1
        """
        self.country1 = Country.objects.create(name="Country1")
        self.country2 = Country.objects.create(name="Country2")
        self.country3 = Country.objects.create(name="Country3")
        self.plan1 = Plan.objects.create(name="Plan1", version=1)
        self.plan2 = Plan.objects.create(name="Plan2", version=1)
        airport1 = Airport.objects.create(name="Airport1", country=self.country1)
        airport2 = Airport.objects.create(name="Airport2", country=self.country2)
        airport3 = Airport.objects.create(name="Airport3", country=self.country3)
        FlightPlan.objects.create(
            flight=Flight.objects.create(
                name="Flight1",
                departure=airport1,
                arrival=airport3,
                cost=100.0,
                departure_date_time="2023-01-01T10:00:00Z",
                arrival_date_time="2023-01-01T12:00:00Z",
            ),
            plan=self.plan1,
            order=1,
        )
        FlightPlan.objects.create(
            flight=Flight.objects.create(
                name="Flight2",
                departure=airport3,
                arrival=airport2,
                cost=150.0,
                departure_date_time="2023-01-02T10:00:00Z",
                arrival_date_time="2023-01-02T12:00:00Z",
            ),
            plan=self.plan2,
            order=1,
        )

    def test_plans_associated_with_country(self):
        """
        Test that plans are correctly associated with their respective countries.
        This test verifies that:
        - plan1 is associated with country1 and not with country2.
        - plan2 is associated with country2 and not with country1.
        """
        plans_country1 = self.country1.plans
        plans_country2 = self.country2.plans

        self.assertIn(self.plan1, plans_country1)
        self.assertNotIn(self.plan2, plans_country1)
        self.assertIn(self.plan2, plans_country2)
        self.assertNotIn(self.plan1, plans_country2)

    def test_string(self):
        """
        Test that the string representation of the country1 object is "Country1".
        """
        self.assertEqual(str(self.country1), "Country1")


class CityModelTest(TestCase):
    """
    Unit tests for the City model.
    Classes:
        CityModelTest: Test case for creating and validating a City instance.
    Methods:
        setUp: Sets up the test environment by creating a Country and a City instance.
        test_city_creation: Tests the creation of a City instance and validates its attributes.
    """

    def setUp(self):
        """
        Set up test environment.

        This method creates a test country and a test city associated with that country.
        It initializes the following attributes:
        - self.country: A Country object with the name "TestCountry".
        - self.city: A City object with the name "TestCity" and associated with self.country.
        """
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)

    def test_city_creation(self):
        """
        Test the creation of a city object.

        This test verifies that the city object is created with the correct name and country attributes.

        Assertions:
            self.assertEqual(self.city.name, "TestCity"): Checks if the city's name is "TestCity".
            self.assertEqual(self.city.country, self.country): Checks if the city's country attribute matches the expected country.
        """
        self.assertEqual(self.city.name, "TestCity")
        self.assertEqual(self.city.country, self.country)


class SightseeingModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment.

        This method creates a test country, city, and sightseeing object to be used in the tests.

        Attributes:
            country (Country): A test country object.
            city (City): A test city object associated with the test country.
            sightseeing (Sightseeing): A test sightseeing object associated with the test city.
        """
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)
        self.sightseeing = Sightseeing.objects.create(
            name="TestSightseeing",
            city=self.city,
            cost=100.0,
            description="TestDescription",
            rating=4.5,
        )

    def test_sightseeing_creation(self):
        """
        Test the creation of a sightseeing object.

        This test verifies that the sightseeing object is created with the correct
        attributes: name, city, cost, description, and rating.

        Assertions:
            - The name of the sightseeing object should be "TestSightseeing".
            - The city of the sightseeing object should match the expected city.
            - The cost of the sightseeing object should be 100.0.
            - The description of the sightseeing object should be "TestDescription".
            - The rating of the sightseeing object should be 4.5.
        """
        self.assertEqual(self.sightseeing.name, "TestSightseeing")
        self.assertEqual(self.sightseeing.city, self.city)
        self.assertEqual(self.sightseeing.cost, 100.0)
        self.assertEqual(self.sightseeing.description, "TestDescription")
        self.assertEqual(self.sightseeing.rating, 4.5)

    def test_sightseeing_str(self):
        """
        Tests the string representation of the Sightseeing object.

        This method checks if the string representation of the Sightseeing
        object is equal to the expected value "TestSightseeing".
        """
        self.assertEqual(str(self.sightseeing), "TestSightseeing")

    def test_sightseeing_country(self):
        """
        Test that the sightseeing country matches the expected country.

        This test verifies that the `country` attribute of the `sightseeing` object
        is equal to the expected `country` attribute.
        """
        self.assertEqual(self.sightseeing.country, self.country)


class HotelModelTest(TestCase):
    """
    Tests for the Hotel model.
    This test case includes the following tests:
    - `test_rooms`: Verifies that the correct number of rooms associated with the hotel is returned and that the rooms are the ones created in the setup.
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


class RoomModelTest(TestCase):
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


class AirportModelTest(TestCase):
    """
    Test suite for the Airport model and related entities.
    Classes:
        AirportModelTest: Test case for testing the Airport model and its relationships.
    Methods:
        setUp():
            Sets up the test environment by creating countries, airports, flights, plans, and flight plans.
        test_plans_for_airport():
            Tests that the plans associated with each airport are correctly retrieved.
        test_airport_creation():
            Tests the creation of an airport and its association with a country.
        test_airport_str():
            Tests the string representation of an airport.
    """
    def setUp(self):
        """
        Set up the test environment by creating necessary objects for testing.
        This method creates:
        - Two countries (`country1` and `country2`).
        - Two airports (`airport1` and `airport2`), each associated with one of the countries.
        - Two flights (`flight1` and `flight2`), each with specific departure and arrival airports, costs, and date-times.
        - Two plans (`plan1` and `plan2`).
        - Two flight plans (`flight_plan1` and `flight_plan2`), each associating a flight with a plan and specifying an order.
        """
        # Create countries
        self.country1 = Country.objects.create(name="Country1")
        self.country2 = Country.objects.create(name="Country2")

        # Create airports
        self.airport1 = Airport.objects.create(name="Airport1", country=self.country1)
        self.airport2 = Airport.objects.create(name="Airport2", country=self.country2)

        # Create flights
        self.flight1 = Flight.objects.create(
            name="Flight1",
            departure=self.airport1,
            arrival=self.airport2,
            cost=100.0,
            departure_date_time="2023-01-01T10:00:00Z",
            arrival_date_time="2023-01-01T12:00:00Z",
        )
        self.flight2 = Flight.objects.create(
            name="Flight2",
            departure=self.airport2,
            arrival=self.airport1,
            cost=150.0,
            departure_date_time="2023-01-02T10:00:00Z",
            arrival_date_time="2023-01-02T12:00:00Z",
        )

        # Create plans
        self.plan1 = Plan.objects.create(name="Plan1", version=1)
        self.plan2 = Plan.objects.create(name="Plan2", version=1)

        # Create flight plans
        self.flight_plan1 = FlightPlan.objects.create(
            flight=self.flight1, plan=self.plan1, order=1
        )
        self.flight_plan2 = FlightPlan.objects.create(
            flight=self.flight2, plan=self.plan2, order=1
        )

    def test_plans_for_airport(self):
        """
        Test the plans associated with different airports.
        This test verifies that the plans for airport1 and airport2 contain
        the expected plans (plan1 and plan2).
        Assertions:
            - plan1 is in the list of plans for airport1.
            - plan2 is in the list of plans for airport1.
            - plan1 is in the list of plans for airport2.
            - plan2 is in the list of plans for airport2.
        """
        # Test plans for airport1
        plans_airport1 = self.airport1.plans
        self.assertIn(self.plan1, plans_airport1)
        self.assertIn(self.plan2, plans_airport1)

        # Test plans for airport2
        plans_airport2 = self.airport2.plans
        self.assertIn(self.plan1, plans_airport2)
        self.assertIn(self.plan2, plans_airport2)

    def test_airport_creation(self):
        """
        Test the creation of an airport instance.

        This test verifies that the airport instance is created with the correct
        name and country attributes.

        Assertions:
            - The name of the airport instance should be "Airport1".
            - The country attribute of the airport instance should match the expected country.
        """
        self.assertEqual(self.airport1.name, "Airport1")
        self.assertEqual(self.airport1.country, self.country1)

    def test_airport_str(self):
        """
        Test the string representation of the airport object.

        This test checks if the string representation of the airport object
        (self.airport1) is equal to the expected string "Airport1".
        """
        self.assertEqual(str(self.airport1), "Airport1")


class FlightModelTest(TestCase):
    """
    Unit tests for the Flight model.
    Classes:
        FlightModelTest: Test case for the Flight model.
    Methods:
        setUp(self):
            Sets up the test environment by creating countries, airports, flights, and plans.
        test_plans(self):
            Tests that the flight is associated with the correct plans.
        test_flight_str(self):
            Tests the string representation of the flight.
        test_flight_duration_in_hours(self):
            Tests the duration of the flight in hours.
    """
    def setUp(self):
        """
        Set up the test environment by creating necessary objects.
        This method creates:
        - Two countries (`country1` and `country2`).
        - Two airports (`airport1` and `airport2`), each associated with one of the countries.
        - A flight (`flight`) that departs from `airport1` and arrives at `airport2`.
        - Two plans (`plan1` and `plan2`).
        - Two flight plans (`flightPlan1` and `flightPlan2`), each associating the flight with one of the plans.
        """
        # Create countries
        self.country1 = Country.objects.create(name="Country1")
        self.country2 = Country.objects.create(name="Country2")

        # Create airports
        self.airport1 = Airport.objects.create(name="Airport1", country=self.country1)
        self.airport2 = Airport.objects.create(name="Airport2", country=self.country2)

        # Create flights
        self.flight = Flight.objects.create(
            name="Flight1",
            departure=self.airport1,
            arrival=self.airport2,
            cost=100.0,
            departure_date_time=datetime(2023, 1, 1, 10, 0),
            arrival_date_time=datetime(2023, 1, 1, 12, 0),
        )

        # Create plans
        self.plan1 = Plan.objects.create(name="Plan1", version=1)
        self.plan2 = Plan.objects.create(name="Plan2", version=1)

        self.flightPlan1 = FlightPlan.objects.create(
            flight=self.flight, plan=self.plan1, order=1
        )
        self.flightPlan2 = FlightPlan.objects.create(
            flight=self.flight, plan=self.plan2, order=1
        )

    def test_plans(self):
        """
        Test that the flight plans include plan1 and plan2.

        This test checks if the flight plans list contains the expected plans
        (plan1 and plan2) by using the assertIn method.
        """
        plans = self.flight.plans
        self.assertIn(self.plan1, plans)
        self.assertIn(self.plan2, plans)

    def test_flight_str(self):
        """
        Test the string representation of the flight object.

        This test checks if the string representation of the flight object
        matches the expected value "Flight1".
        """
        self.assertEqual(str(self.flight), "Flight1")

    def test_flight_duration_in_hours(self):
        """
        Test that the flight duration in hours is correctly calculated.

        This test checks if the `duration_in_hours` attribute of the `flight` object
        returns the expected value of 2 hours.
        """
        self.assertEqual(self.flight.duration_in_hours, 2)


class PlanModelTests(TestCase):
    """
    Test suite for the Plan model.
    This test suite includes the following tests:
    - `test_countries`: Verifies that the countries associated with the plan are correctly retrieved.
    - `test_planes`: Verifies that the flights associated with the plan are correctly retrieved.
    - `test_sightseeings`: Verifies that the sightseeing spots associated with the plan are correctly retrieved.
    - `test_cost`: Verifies that the total cost of the plan is correctly calculated.
    - `test_duration_in_days`: Verifies that the duration of the plan in days is correctly calculated based on the flights.
    - `test_duration_in_days_no_flights`: Verifies that a ValueError is raised when calculating the duration of a plan with no flights.
    The `setUp` method initializes the test data, including countries, cities, sightseeing spots, hotels, rooms, airports, flights, and plans.
    """

    def setUp(self):
        """
        Set up the test environment by creating instances of Country, City, Sightseeing, Hotel, Room, Airport, Flight, Plan, FlightPlan, and SightseeingPlan models.
        Creates:
            - Two countries
            - Two cities, each associated with a country
            - Two sightseeing spots, each associated with a city
            - Two hotels, each associated with a city
            - Two rooms, each associated with a hotel
            - Two airports, each associated with a country
            - Two flights, each associated with departure and arrival airports
            - One plan, with rooms added to it
            - Two flight plans, each associated with a flight and the plan
            - Two sightseeing plans, each associated with a sightseeing spot and the plan
        """
        # Create countries
        self.country1 = Country.objects.create(name="Country1")
        self.country2 = Country.objects.create(name="Country2")

        # Create cities
        self.city1 = City.objects.create(name="City1", country=self.country1)
        self.city2 = City.objects.create(name="City2", country=self.country2)

        # Create sightseeing spots
        self.sightseeing1 = Sightseeing.objects.create(
            name="Sightseeing1",
            city=self.city1,
            cost=100.0,
            description="Description1",
            rating=4.5,
        )
        self.sightseeing2 = Sightseeing.objects.create(
            name="Sightseeing2",
            city=self.city2,
            cost=150.0,
            description="Description2",
            rating=4.0,
        )

        # Create hotels
        self.hotel1 = Hotel.objects.create(name="Hotel1", city=self.city1, rating=4.0)
        self.hotel2 = Hotel.objects.create(name="Hotel2", city=self.city2, rating=3.5)

        # Create rooms
        self.room1 = Room.objects.create(
            hotel=self.hotel1,
            room_type="Single",
            from_date=date(2023, 1, 1),
            to_date=date(2023, 1, 5),
            cost=500.0,
        )
        self.room2 = Room.objects.create(
            hotel=self.hotel2,
            room_type="Double",
            from_date=date(2023, 1, 6),
            to_date=date(2023, 1, 10),
            cost=800.0,
        )

        # Create airports
        self.airport1 = Airport.objects.create(name="Airport1", country=self.country1)
        self.airport2 = Airport.objects.create(name="Airport2", country=self.country2)

        # Create flights
        self.flight1 = Flight.objects.create(
            name="Flight1",
            departure=self.airport1,
            arrival=self.airport2,
            cost=300.0,
            departure_date_time=datetime(2023, 1, 1, 10, 0),
            arrival_date_time=datetime(2023, 1, 1, 14, 0),
        )
        self.flight2 = Flight.objects.create(
            name="Flight2",
            departure=self.airport2,
            arrival=self.airport1,
            cost=350.0,
            departure_date_time=datetime(2023, 1, 10, 16, 0),
            arrival_date_time=datetime(2023, 1, 10, 20, 0),
        )

        # Create plan
        self.plan = Plan.objects.create(name="Plan1", version=1)
        self.plan.rooms.add(self.room1, self.room2)
        self.plan = Plan.objects.get(pk=self.plan.pk)

        # Create flight plans
        self.flight_plan1 = FlightPlan.objects.create(
            flight=self.flight1, plan=self.plan, order=1
        )
        self.flight_plan2 = FlightPlan.objects.create(
            flight=self.flight2, plan=self.plan, order=2
        )

        # Create sightseeing plans
        self.sightseeing_plan1 = SightseeingPlan.objects.create(
            sightseeing=self.sightseeing1, plan=self.plan, order=1
        )
        self.sightseeing_plan2 = SightseeingPlan.objects.create(
            sightseeing=self.sightseeing2, plan=self.plan, order=2
        )

    def test_countries(self):
        """
        Test that the countries in the travel plan include the expected countries.

        This test checks if the countries list in the travel plan contains
        the specified countries (country1 and country2).

        Assertions:
            self.assertIn(self.country1, countries): Verifies that country1 is in the countries list.
            self.assertIn(self.country2, countries): Verifies that country2 is in the countries list.
        """
        countries = self.plan.countries
        self.assertIn(self.country1, countries)
        self.assertIn(self.country2, countries)

    def test_planes(self):
        """
        Test that the planes list in the plan contains the expected flights.

        This test checks if `self.flight1` and `self.flight2` are present in the
        `planes` list of the `plan` object.
        """
        planes = self.plan.planes
        self.assertIn(self.flight1, planes)
        self.assertIn(self.flight2, planes)

    def test_sightseeings(self):
        """
        Test that the planned sightseeings include the expected sightseeing objects.

        This test checks if the sightseeings list in the plan contains the
        predefined sightseeing1 and sightseeing2 objects.
        """
        sightseeings = self.plan.sightseeings
        self.assertIn(self.sightseeing1, sightseeings)
        self.assertIn(self.sightseeing2, sightseeings)

    def test_cost(self):
        """
        Test the total cost calculation of the travel plan.

        This test verifies that the total cost of the travel plan is correctly
        calculated by summing up the costs of individual components such as
        rooms, sightseeing activities, and flights.

        It compares the total cost from the travel plan with the expected cost,
        which is the sum of the costs of room1, room2, sightseeing1, sightseeing2,
        flight1, and flight2.
        """
        total_cost = self.plan.cost
        expected_cost = (
            self.room1.cost
            + self.room2.cost
            + self.sightseeing1.cost
            + self.sightseeing2.cost
            + self.flight1.cost
            + self.flight2.cost
        )
        self.assertEqual(total_cost, expected_cost)

    def test_duration_in_days(self):
        """
        Test the duration_in_days method of the plan.

        This test calculates the expected duration in days by subtracting the 
        departure date and time of the first flight from the arrival date and 
        time of the second flight. It then asserts that the duration returned 
        by the plan's duration_in_days method matches the expected duration.
        """
        duration = self.plan.duration_in_days
        expected_duration = (
            self.flight2.arrival_date_time - self.flight1.departure_date_time
        ).days
        self.assertEqual(duration, expected_duration)

    def test_duration_in_days_no_flights(self):
        """
        Test the duration_in_days method for a plan with no flights.

        This test creates a plan with no flights and asserts that calling
        the duration_in_days method raises a ValueError.
        """
        # Create a plan with no flights
        empty_plan = Plan.objects.create(name="EmptyPlan", version=1)
        with self.assertRaises(ValueError):
            empty_plan.duration_in_days


class FlightPlanModelTest(TestCase):
    """
    Test suite for the FlightPlan model.
    This test case includes the following tests:
    - `test_flight_plan_creation`: Verifies that a FlightPlan instance is created correctly.
    - `test_flight_plan_unique_together`: Ensures that the unique constraint on the FlightPlan model is enforced.
    - `test_flight_plan_ordering`: Checks that FlightPlan instances are ordered correctly by the 'order' field.
    - `test_flight_plan_countries_property`: Tests the 'countries' property of the FlightPlan model to ensure it includes the correct countries.
    """
    def setUp(self):
        """
        Set up the test environment for the TravelPlanner application.

        This method creates the following objects:
        - Two Country objects: country1 and country2.
        - Two Airport objects: airport1 (associated with country1) and airport2 (associated with country2).
        - Two Flight objects: flight1 (from airport1 to airport2) and flight2 (from airport2 to airport1).
        - One Plan object: plan.
        - One FlightPlan object: flight_plan (associating flight1 with plan and setting the order to 1).
        """
        self.country1 = Country.objects.create(name="Country1")
        self.country2 = Country.objects.create(name="Country2")
        self.airport1 = Airport.objects.create(name="Airport1", country=self.country1)
        self.airport2 = Airport.objects.create(name="Airport2", country=self.country2)
        self.flight1 = Flight.objects.create(
            name="Flight1",
            departure=self.airport1,
            arrival=self.airport2,
            cost=100.0,
            departure_date_time="2023-01-01T10:00:00Z",
            arrival_date_time="2023-01-01T14:00:00Z",
        )
        self.flight2 = Flight.objects.create(
            name="Flight2",
            departure=self.airport2,
            arrival=self.airport1,
            cost=150.0,
            departure_date_time="2023-01-10T16:00:00Z",
            arrival_date_time="2023-01-10T20:00:00Z",
        )
        self.plan = Plan.objects.create(name="Plan1", version=1)
        self.flight_plan = FlightPlan.objects.create(
            flight=self.flight1, plan=self.plan, order=1
        )

    def test_flight_plan_creation(self):
        """
        Test the creation of a flight plan.

        This test verifies that the flight plan is created correctly by checking:
        1. The flight associated with the flight plan.
        2. The plan associated with the flight plan.
        3. The order of the flight plan.
        """
        self.assertEqual(self.flight_plan.flight, self.flight1)
        self.assertEqual(self.flight_plan.plan, self.plan)
        self.assertEqual(self.flight_plan.order, 1)

    def test_flight_plan_unique_together(self):
        """
        Test that creating a FlightPlan with the same flight, plan, and order raises an exception.
        This ensures the unique_together constraint on the FlightPlan model is enforced.
        """
        with self.assertRaises(Exception):
            FlightPlan.objects.create(flight=self.flight1, plan=self.plan, order=2)

    def test_flight_plan_ordering(self):
        """
        Test the ordering of flight plans within a plan.

        This test creates a second flight plan with a specified order and verifies
        that the flight plans are correctly ordered by the 'order' field when
        retrieved from the database.

        Assertions:
            - The first flight plan in the ordered list is the original flight plan.
            - The second flight plan in the ordered list is the newly created flight plan.
        """
        flight_plan2 = FlightPlan.objects.create(
            flight=self.flight2, plan=self.plan, order=2
        )
        flight_plans = FlightPlan.objects.filter(plan=self.plan).order_by("order")
        self.assertEqual(flight_plans[0], self.flight_plan)
        self.assertEqual(flight_plans[1], flight_plan2)

    def test_flight_plan_countries_property(self):
        """
        Test that the 'countries' property of the flight plan includes the expected countries.

        This test verifies that the 'countries' property of the flight plan object
        contains the countries 'country1' and 'country2'.
        """
        countries = self.flight_plan.countries
        self.assertIn(self.country1, countries)
        self.assertIn(self.country2, countries)


class SightseeingPlanModelTest(TestCase):
    """
    Unit tests for the SightseeingPlan model.
    This test case ensures that the SightseeingPlan model is correctly created and 
    associated with the appropriate Sightseeing and Plan instances.
    Methods:
        setUp(): Sets up the test environment by creating instances of Country, City, 
                 Sightseeing, Plan, and SightseeingPlan models.
        test_sightseeing_plan_creation(): Tests the creation of a SightseeingPlan 
                                          instance and verifies its attributes.
    """
    def setUp(self):
        """
        Set up test data for the TravelPlanner application.

        This method creates the following objects:
        - A Country object named "TestCountry".
        - A City object named "TestCity" associated with the created Country.
        - A Sightseeing object named "TestSightseeing" associated with the created City, with a cost of 100.0, a description of "TestDescription", and a rating of 4.5.
        - A Plan object named "TestPlan" with version 1.
        - A SightseeingPlan object associating the created Sightseeing and Plan objects, with an order of 1.
        """
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)
        self.sightseeing = Sightseeing.objects.create(
            name="TestSightseeing",
            city=self.city,
            cost=100.0,
            description="TestDescription",
            rating=4.5,
        )
        self.plan = Plan.objects.create(name="TestPlan", version=1)
        self.sightseeing_plan = SightseeingPlan.objects.create(
            sightseeing=self.sightseeing, plan=self.plan, order=1
        )

    def test_sightseeing_plan_creation(self):
        """
        Test the creation of a sightseeing plan.

        This test verifies that the sightseeing plan is created correctly by checking:
        - The sightseeing attribute of the sightseeing plan matches the expected sightseeing.
        - The plan attribute of the sightseeing plan matches the expected plan.
        - The order attribute of the sightseeing plan is set to 1.
        """
        self.assertEqual(self.sightseeing_plan.sightseeing, self.sightseeing)
        self.assertEqual(self.sightseeing_plan.plan, self.plan)
        self.assertEqual(self.sightseeing_plan.order, 1)

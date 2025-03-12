"""
Plan App Testing
"""

from common.models import (
    Plan,
    Country,
    City,
    Sightseeing,
    Airport,
    Flight,
    FlightPlan,
    SightseeingPlan,
)
from common.tests import BaseModelTest


class PlanModelTests(BaseModelTest):
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
        Set up the test environment by creating instances of required models.
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

        self.countries = self.create_n_countries(2)
        cities = self.create_n_cities(2, self.countries)
        self.sightseeings = self.create_n_sightseeings(2, cities)
        self.rooms = self.create_n_rooms(2, self.create_n_hotels(2, cities))
        flights = self.create_n_flights(2, self.create_n_airports(2, self.countries))
        self.plan = self.create_n_plans(1)[0]
        self.create_n_flight_plans(2, flights, [self.plan])
        self.create_n_sightseeing_plans(2, self.sightseeings, [self.plan])

        self.plan.rooms.add(self.rooms[0], self.rooms[1])
        self.plan = Plan.objects.get(pk=self.plan.pk)
        self.flight1 = flights[0]
        self.flight2 = flights[1]

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
        self.assertIn(self.countries[0], countries)
        self.assertIn(self.countries[1], countries)

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
        self.assertIn(self.sightseeings[0], sightseeings)
        self.assertIn(self.sightseeings[1], sightseeings)

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
            self.rooms[0].cost
            + self.rooms[1].cost
            + self.sightseeings[0].cost
            + self.sightseeings[1].cost
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
        with self.assertRaises(ValueError) as error:
            _ = empty_plan.duration_in_days
        self.assertEqual(
            str(error.exception),
            "No planes in the plan",
        )


class FlightPlanModelTest(BaseModelTest):
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
        self.flight1 = Flight.objects.create(
            name="Flight1",
            departure=Airport.objects.create(name="Airport1", country=self.country1),
            arrival=Airport.objects.create(name="Airport2", country=self.country2),
            cost=100.0,
            departure_date_time="2023-01-01T10:00:00Z",
            arrival_date_time="2023-01-01T14:00:00Z",
        )
        self.flight2 = Flight.objects.create(
            name="Flight2",
            departure=Airport.objects.create(name="Airport3", country=self.country2),
            arrival=Airport.objects.create(name="Airport4", country=self.country1),
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


class SightseeingPlanModelTest(BaseModelTest):
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
        - A Sightseeing object named "TestSightseeing" with the created City, a cost of 100.0, description of "TestDescription", a rating of 4.5.
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

"""
Plane App Test
"""

from datetime import datetime
from common.models import Country, Airport, Flight, Plan, FlightPlan
from common.tests import BaseModelTest


class AirportModelTest(BaseModelTest):
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

        # Create plans
        self.plan1 = Plan.objects.create(name="Plan1", version=1)
        self.plan2 = Plan.objects.create(name="Plan2", version=1)

        # Create flight plans
        FlightPlan.objects.create(flight=self.flight1, plan=self.plan1, order=1)
        FlightPlan.objects.create(
            flight=Flight.objects.create(
                name="Flight2",
                departure=self.airport2,
                arrival=self.airport1,
                cost=150.0,
                departure_date_time="2023-01-02T10:00:00Z",
                arrival_date_time="2023-01-02T12:00:00Z",
            ),
            plan=self.plan2,
            order=1,
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


class FlightModelTest(BaseModelTest):
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

        # Create flights
        self.flight = Flight.objects.create(
            name="Flight1",
            departure=Airport.objects.create(
                name="Airport1", country=Country.objects.create(name="Country1")
            ),
            arrival=Airport.objects.create(
                name="Airport2", country=Country.objects.create(name="Country2")
            ),
            cost=100.0,
            departure_date_time=datetime(2023, 1, 1, 10, 0),
            arrival_date_time=datetime(2023, 1, 1, 12, 0),
        )

        # Create plans
        self.plan1 = Plan.objects.create(name="Plan1", version=1)
        self.plan2 = Plan.objects.create(name="Plan2", version=1)

        FlightPlan.objects.create(flight=self.flight, plan=self.plan1, order=1)
        FlightPlan.objects.create(flight=self.flight, plan=self.plan2, order=1)

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

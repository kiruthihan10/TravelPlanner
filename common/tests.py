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
    def setUp(self):
        # Create test data
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
        # Test that plans are correctly associated with the country
        plans_country1 = self.country1.plans
        plans_country2 = self.country2.plans

        self.assertIn(self.plan1, plans_country1)
        self.assertNotIn(self.plan2, plans_country1)
        self.assertIn(self.plan2, plans_country2)
        self.assertNotIn(self.plan1, plans_country2)


class CityModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)

    def test_city_creation(self):
        self.assertEqual(self.city.name, "TestCity")
        self.assertEqual(self.city.country, self.country)


class SightseeingModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.sightseeing.name, "TestSightseeing")
        self.assertEqual(self.sightseeing.city, self.city)
        self.assertEqual(self.sightseeing.cost, 100.0)
        self.assertEqual(self.sightseeing.description, "TestDescription")
        self.assertEqual(self.sightseeing.rating, 4.5)

    def test_sightseeing_str(self):
        self.assertEqual(str(self.sightseeing), "TestSightseeing")

    def test_sightseeing_country(self):
        self.assertEqual(self.sightseeing.country, self.country)


class HotelModelTest(TestCase):
    def setUp(self):
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
        # Retrieve rooms associated with the hotel
        rooms = self.hotel.rooms

        # Check that the correct number of rooms is returned
        self.assertEqual(rooms.count(), 2)

        # Check that the rooms are the ones we created
        self.assertIn(self.room1, rooms)
        self.assertIn(self.room2, rooms)

    def test_hotel_str(self):
        self.assertEqual(str(self.hotel), "Test Hotel")

    def test_hotel_country(self):
        self.assertEqual(self.hotel.country, self.country)


class RoomModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.room.hotel, self.hotel)
        self.assertEqual(self.room.room_type, "Single")
        self.assertEqual(self.room.cost, 500.0)

    def test_room_str(self):
        self.assertEqual(str(self.room), f"{self.hotel.name} - Single")

    def test_room_duration_in_days(self):
        self.assertEqual(self.room.duration_in_days, 5)

    def test_room_cost_per_day(self):
        self.assertEqual(self.room.cost_per_day, 100.0)


class AirportModelTest(TestCase):
    def setUp(self):
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
        # Test plans for airport1
        plans_airport1 = self.airport1.plans
        self.assertIn(self.plan1, plans_airport1)
        self.assertIn(self.plan2, plans_airport1)

        # Test plans for airport2
        plans_airport2 = self.airport2.plans
        self.assertIn(self.plan1, plans_airport2)
        self.assertIn(self.plan2, plans_airport2)

    def test_airport_creation(self):
        self.assertEqual(self.airport1.name, "Airport1")
        self.assertEqual(self.airport1.country, self.country1)

    def test_airport_str(self):
        self.assertEqual(str(self.airport1), "Airport1")


class FlightModelTest(TestCase):
    def setUp(self):
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
        plans = self.flight.plans
        self.assertIn(self.plan1, plans)
        self.assertIn(self.plan2, plans)

    def test_flight_str(self):
        self.assertEqual(str(self.flight), "Flight1")

    def test_flight_duration_in_hours(self):
        self.assertEqual(self.flight.duration_in_hours, 2)


class PlanModelTests(TestCase):

    def setUp(self):
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
        countries = self.plan.countries
        self.assertIn(self.country1, countries)
        self.assertIn(self.country2, countries)

    def test_planes(self):
        planes = self.plan.planes
        self.assertIn(self.flight1, planes)
        self.assertIn(self.flight2, planes)

    def test_sightseeings(self):
        sightseeings = self.plan.sightseeings
        self.assertIn(self.sightseeing1, sightseeings)
        self.assertIn(self.sightseeing2, sightseeings)

    def test_cost(self):
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
        duration = self.plan.duration_in_days
        expected_duration = (
            self.flight2.arrival_date_time - self.flight1.departure_date_time
        ).days
        self.assertEqual(duration, expected_duration)


class FlightPlanModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.flight_plan.flight, self.flight1)
        self.assertEqual(self.flight_plan.plan, self.plan)
        self.assertEqual(self.flight_plan.order, 1)

    def test_flight_plan_unique_together(self):
        with self.assertRaises(Exception):
            FlightPlan.objects.create(flight=self.flight1, plan=self.plan, order=2)

    def test_flight_plan_ordering(self):
        flight_plan2 = FlightPlan.objects.create(
            flight=self.flight2, plan=self.plan, order=2
        )
        flight_plans = FlightPlan.objects.filter(plan=self.plan).order_by("order")
        self.assertEqual(flight_plans[0], self.flight_plan)
        self.assertEqual(flight_plans[1], flight_plan2)

    def test_flight_plan_countries_property(self):
        countries = self.flight_plan.countries
        self.assertIn(self.country1, countries)
        self.assertIn(self.country2, countries)


class SightseeingPlanModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.sightseeing_plan.sightseeing, self.sightseeing)
        self.assertEqual(self.sightseeing_plan.plan, self.plan)
        self.assertEqual(self.sightseeing_plan.order, 1)

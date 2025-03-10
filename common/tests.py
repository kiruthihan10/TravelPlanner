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
        self.country = Country.objects.create(name="TestCountry")

    def test_country_creation(self):
        self.assertEqual(self.country.name, "TestCountry")

    def test_country_str(self):
        self.assertEqual(str(self.country), "TestCountry")


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
        self.country = Country.objects.create(name="TestCountry")
        self.city = City.objects.create(name="TestCity", country=self.country)
        self.hotel = Hotel.objects.create(name="TestHotel", city=self.city, rating=4.0)

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.name, "TestHotel")
        self.assertEqual(self.hotel.city, self.city)
        self.assertEqual(self.hotel.rating, 4.0)

    def test_hotel_str(self):
        self.assertEqual(str(self.hotel), "TestHotel")

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
        self.country = Country.objects.create(name="TestCountry")
        self.airport = Airport.objects.create(name="TestAirport", country=self.country)

    def test_airport_creation(self):
        self.assertEqual(self.airport.name, "TestAirport")
        self.assertEqual(self.airport.country, self.country)

    def test_airport_str(self):
        self.assertEqual(str(self.airport), "TestAirport")


class FlightModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="TestCountry")
        self.departure_airport = Airport.objects.create(
            name="DepartureAirport", country=self.country
        )
        self.arrival_airport = Airport.objects.create(
            name="ArrivalAirport", country=self.country
        )
        self.flight = Flight.objects.create(
            name="TestFlight",
            departure=self.departure_airport,
            arrival=self.arrival_airport,
            cost=200.0,
            departure_date_time=datetime.now(),
            arrival_date_time=datetime.now() + timedelta(hours=2),
        )

    def test_flight_creation(self):
        self.assertEqual(self.flight.name, "TestFlight")
        self.assertEqual(self.flight.departure, self.departure_airport)
        self.assertEqual(self.flight.arrival, self.arrival_airport)
        self.assertEqual(self.flight.cost, 200.0)

    def test_flight_str(self):
        self.assertEqual(str(self.flight), "TestFlight")

    def test_flight_duration_in_hours(self):
        self.assertEqual(self.flight.duration_in_hours, 2)


class PlanModelTest(TestCase):
    def setUp(self):
        self.plan = Plan.objects.create(name="TestPlan", version=1)

    def test_plan_creation(self):
        self.assertEqual(self.plan.name, "TestPlan")
        self.assertEqual(self.plan.version, 1)


class FlightPlanModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="TestCountry")
        self.departure_airport = Airport.objects.create(
            name="DepartureAirport", country=self.country
        )
        self.arrival_airport = Airport.objects.create(
            name="ArrivalAirport", country=self.country
        )
        self.flight = Flight.objects.create(
            name="TestFlight",
            departure=self.departure_airport,
            arrival=self.arrival_airport,
            cost=200.0,
            departure_date_time=datetime.now(),
            arrival_date_time=datetime.now() + timedelta(hours=2),
        )
        self.plan = Plan.objects.create(name="TestPlan", version=1)
        self.flight_plan = FlightPlan.objects.create(
            flight=self.flight, plan=self.plan, order=1
        )

    def test_flight_plan_creation(self):
        self.assertEqual(self.flight_plan.flight, self.flight)
        self.assertEqual(self.flight_plan.plan, self.plan)
        self.assertEqual(self.flight_plan.order, 1)


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

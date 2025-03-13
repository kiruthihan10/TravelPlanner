"""
This module contains test cases for the TravelPlanner application models.
Classes:
    BaseModelTest(TestCase): Base Test Case for TravelPlanner application models.
Methods:
    generate_random_string(length=10):
    create_n_countries(n) -> List[Country]:
    create_n_cities(n: int, countries: List[Country]) -> List[City]:
    create_n_sightseeings(n: int, cities: List[City]) -> List[Sightseeing]:
    create_n_hotels(n: int, cities: List[City]) -> List[Hotel]:
    create_n_rooms(n: int, hotels: List[Hotel]) -> List[Room]:
    create_n_airports(n: int, countries: List[Country]) -> List[Airport]:
    create_n_flights(n: int, airports: List[Airport]) -> List[Flight]:
    create_n_plans(n: int) -> List[Plan]:
    create_n_flight_plans(n: int, flights: List[Flight], plans: List[Plan]) -> List[FlightPlan]:
    create_n_sightseeing_plans(n: int, sightseeings: List[Sightseeing], plans: List[Plan]) -> List[SightseeingPlan]:
"""

from datetime import date, datetime, timedelta

import random
import string
from typing import List
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


class BaseModelTest(TestCase):
    """
    Base Test Case for TravelPlanner application models.
    """

    def generate_random_string(self, length=10):
        """
        Generate a random string of specified length.
        Args:
            length (int): The length of the random string to generate. Default is 10.
        Returns:
            str: A random string consisting of ASCII letters.
        """

        return "".join(random.choices(string.ascii_letters, k=length))

    def create_n_countries(self, n) -> List[Country]:
        """
        Creates and returns a list of `n` Country objects with random names.

        Args:
            n (int): The number of Country objects to create.

        Returns:
            List[Country]: A list of created Country objects.
        """
        countries = []
        for _ in range(n):
            country = Country.objects.create(
                name=f"Country_{self.generate_random_string()}"
            )
            countries.append(country)
        return countries

    def create_n_cities(self, n: int, countries: List[Country]) -> List[City]:
        """
        Create a specified number of City instances and associate them with given countries.

        Args:
            n (int): The number of City instances to create.
            countries (List[Country]): A list of Country instances to associate with the cities.

        Returns:
            List[City]: A list of created City instances.
        """
        cities = []
        for i in range(n):
            city = City.objects.create(
                name=f"City_{self.generate_random_string()}",
                country=countries[i % len(countries)],
            )
            cities.append(city)
        return cities

    def create_n_sightseeings(self, n: int, cities: List[City]) -> List[Sightseeing]:
        """
        Creates a specified number of Sightseeing objects and associates them with the given cities.

        Args:
            n (int): The number of Sightseeing objects to create.
            cities (List[City]): A list of City objects to associate with the Sightseeing objects.

        Returns:
            List[Sightseeing]: A list of created Sightseeing objects.
        """
        sightseeings = []
        for i in range(n):
            sightseeing = Sightseeing.objects.create(
                name=f"Sightseeing_{self.generate_random_string()}",
                city=cities[i % len(cities)],
                cost=random.uniform(50.0, 200.0),
                description=self.generate_random_string(50),
                rating=random.uniform(3.0, 5.0),
            )
            sightseeings.append(sightseeing)
        return sightseeings

    def create_n_hotels(self, n: int, cities: List[City]) -> List[Hotel]:
        """
        Creates a specified number of Hotel instances and associates them with the given cities.

        Args:
            n (int): The number of Hotel instances to create.
            cities (List[City]): A list of City instances to associate with the hotels.

        Returns:
            List[Hotel]: A list of created Hotel instances.
        """
        hotels = []
        for i in range(n):
            hotel = Hotel.objects.create(
                name=f"Hotel_{self.generate_random_string()}",
                city=cities[i % len(cities)],
                rating=random.uniform(3.0, 5.0),
            )
            hotels.append(hotel)
        return hotels

    def create_n_rooms(self, n: int, hotels: List[Hotel]) -> List[Room]:
        """
        Create a specified number of rooms and assign them to the given hotels.

        Args:
            n (int): The number of rooms to create.
            hotels (List[Hotel]): A list of Hotel objects to which the rooms will be assigned.

        Returns:
            List[Room]: A list of created Room objects.
        """
        rooms = []
        for i in range(n):
            room = Room.objects.create(
                hotel=hotels[i % len(hotels)],
                room_type=random.choice(["Single", "Double", "Suite"]),
                from_date=date.today(),
                to_date=date.today() + timedelta(days=random.randint(1, 10)),
                cost=random.uniform(50.0, 200.0),
            )
            rooms.append(room)
        return rooms

    def create_n_airports(self, n: int, countries: List[Country]) -> List[Airport]:
        """
        Creates a specified number of Airport instances and associates them with the given countries.

        Args:
            n (int): The number of Airport instances to create.
            countries (List[Country]): A list of Country instances to associate with the airports.

        Returns:
            List[Airport]: A list of created Airport instances.
        """
        airports = []
        for i in range(n):
            airport = Airport.objects.create(
                name=f"Airport_{self.generate_random_string()}",
                country=countries[i % n],
            )
            airports.append(airport)
        return airports

    def create_n_flights(self, n: int, airports: List[Airport]) -> List[Flight]:
        """
        Creates a specified number of Flight instances with random attributes.

        Args:
            n (int): The number of Flight instances to create.
            airports (List[Airport]): A list of Airport instances to use for departure and arrival.

        Returns:
            List[Flight]: A list of created Flight instances.
        """
        flights = []
        for i in range(n):
            flight = Flight.objects.create(
                name=f"Flight_{self.generate_random_string()}",
                departure=airports[i % len(airports)],
                arrival=airports[(i + 1) % len(airports)],
                cost=random.uniform(100.0, 500.0),
                departure_date_time=datetime.now(),
                arrival_date_time=datetime.now()
                + timedelta(hours=random.randint(1, 10)),
            )
            flights.append(flight)
        return flights

    def create_n_plans(self, n: int) -> List[Plan]:
        """
        Create and return a list of 'n' Plan objects.

        Args:
            n (int): The number of Plan objects to create.

        Returns:
            List[Plan]: A list containing the created Plan objects.
        """
        plans = []
        for _ in range(n):
            plan = Plan.objects.create(name=f"Plan_{self.generate_random_string()}")
            plans.append(plan)
        return plans

    def create_n_flight_plans(
        self,
        n: int,
        flights: List[Flight],
        plans: List[Plan],
    ) -> List[FlightPlan]:
        """
        Creates a specified number of flight plans by associating flights and plans.

        Args:
            n (int): The number of flight plans to create.
            flights (List[Flight]): A list of Flight objects to be used in the flight plans.
            plans (List[Plan]): A list of Plan objects to be used in the flight plans.

        Returns:
            List[FlightPlan]: A list of created FlightPlan objects.
        """
        flight_plans = []
        for i in range(n):
            flight_plan = FlightPlan.objects.create(
                flight=flights[i % len(flights)],
                plan=plans[i % len(plans)],
                order=i + 1,
            )
            flight_plans.append(flight_plan)
        return flight_plans

    def create_n_sightseeing_plans(
        self,
        n: int,
        sightseeings: List[Sightseeing],
        plans: List[Plan],
    ) -> List[SightseeingPlan]:
        """
        Create a specified number of sightseeing plans.

        Args:
            n (int): The number of sightseeing plans to create.
            sightseeings (List[Sightseeing]): A list of sightseeing objects to be used in the plans.
            plans (List[Plan]): A list of plan objects to be used in the sightseeing plans.

        Returns:
            List[SightseeingPlan]: A list of created SightseeingPlan objects.
        """
        sightseeing_plans = []
        for i in range(n):
            sightseeing_plan = SightseeingPlan.objects.create(
                sightseeing=sightseeings[i % len(sightseeings)],
                plan=plans[i % len(plans)],
                order=i + 1,
            )
            sightseeing_plans.append(sightseeing_plan)
        return sightseeing_plans

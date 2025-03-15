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
import unittest

from django.test import TestCase
from django.http import HttpRequest
from django.core.paginator import Paginator

from .components.tables import ModelTable, pagination_handle

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


class TestPaginationHandleTest(unittest.TestCase):
    """
    Unit tests for the pagination_handle function.
    TestPaginationHandleTest is a test case class that contains the following tests:
    - test_default_values: Tests that the default pagination size is 10 and the default page number is 1.
    - test_custom_size_and_page: Tests that custom size and page number values are correctly parsed from the request.
    - test_invalid_size: Tests that an invalid size value defaults to 10.
    - test_invalid_page: Tests that an invalid page number value defaults to 1.
    - test_partial_parameters: Tests that partial parameters (only size or only page) are handled correctly.
    """

    def test_default_values(self):
        """
        Test the default values for pagination.

        This test verifies that when an HttpRequest object is passed to the
        pagination_handle function without any query parameters, the default
        values for size and page_number are correctly set to 10 and 1,
        respectively.
        """
        request = HttpRequest()
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 10)
        self.assertEqual(page_number, 1)

    def test_custom_size_and_page(self):
        """
        Test the pagination_handle function with custom size and page number.

        This test simulates an HTTP GET request with 'size' set to '20' and 'page' set to '2'.
        It verifies that the pagination_handle function correctly parses these values and
        returns the expected size and page number.

        Assertions:
            - The size returned by pagination_handle should be 20.
            - The page number returned by pagination_handle should be 2.
        """
        request = HttpRequest()
        request.GET["size"] = "20"
        request.GET["page"] = "2"
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 20)
        self.assertEqual(page_number, 2)

    def test_invalid_size(self):
        """
        Test case for pagination_handle function to handle invalid size parameter.

        This test simulates an HTTP GET request with an invalid 'size' parameter
        and verifies that the pagination_handle function returns the default size
        of 10 and the default page number of 1.

        Assertions:
            - The size should be set to the default value of 10.
            - The page number should be set to the default value of 1.
        """
        request = HttpRequest()
        request.GET["size"] = "invalid"
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 10)
        self.assertEqual(page_number, 1)

    def test_invalid_page(self):
        """
        Test case for handling an invalid page number in the pagination.

        This test simulates a request with an invalid page number and verifies
        that the pagination_handle function returns the default size and page number.

        Steps:
        1. Create an HttpRequest object.
        2. Set the 'page' parameter in the GET request to 'invalid'.
        3. Call the pagination_handle function with the request.
        4. Assert that the returned size is 10.
        5. Assert that the returned page number is 1.
        """
        request = HttpRequest()
        request.GET["page"] = "invalid"
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 10)
        self.assertEqual(page_number, 1)

    def test_partial_parameters(self):
        """
        Tests the pagination_handle function with partial parameters.
        This test verifies that the pagination_handle function correctly handles
        requests with only the 'size' parameter and only the 'page' parameter.
        Test cases:
        1. When the 'size' parameter is provided, the function should return the
            specified size and the default page number (1).
        2. When the 'page' parameter is provided, the function should return the
            default size (10) and the specified page number.
        Assertions:
        - The size should be equal to the provided 'size' parameter.
        - The page number should be equal to the default page number (1) when only
          the 'size' parameter is provided.
        - The size should be equal to the default size (10) when only the 'page'
          parameter is provided.
        - The page number should be equal to the provided 'page' parameter.
        """
        request = HttpRequest()
        request.GET["size"] = "15"
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 15)
        self.assertEqual(page_number, 1)

        request = HttpRequest()
        request.GET["page"] = "3"
        size, page_number = pagination_handle(request)
        self.assertEqual(size, 10)
        self.assertEqual(page_number, 3)


class ModelTableTest(BaseModelTest):
    """
    Unit tests for the ModelTable class.
    Tests included:
    - setUp: Initializes the test environment with sample data and a paginator.
    - test_default_row_func: Verifies the default row function returns the correct data.
    - test_custom_row_func: Checks that a custom row function can be used and returns the correct data.
    - test_rows: Ensures the correct number of rows are returned and the data is accurate.
    - test_columns: Validates that the table columns are set correctly.
    - test_has_previous: Tests the has_previous property for pagination.
    - test_has_next: Tests the has_next property for pagination.
    - test_previous_page_number: Verifies the previous_page_number property.
    - test_next_page_number: Verifies the next_page_number property.
    - test_page_number: Checks the current page number.
    - test_page_size: Ensures the page size is correct.
    - test_render: Tests the render method to ensure the table is rendered correctly.
    - test_row_column_mismatch: Ensures a ValueError is raised when there is a mismatch between row data and columns.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method initializes the following:
        - Creates 20 country instances using `create_n_countries`.
        - Initializes a Paginator with the created instances, setting 10 instances per page.
        - Retrieves the first page of the paginator.
        - Defines the columns to be used in the table.
        - Initializes a ModelTable with the first page and the specified columns.
        """
        self.instances = self.create_n_countries(20)
        self.paginator = Paginator(self.instances, 10)
        self.page = self.paginator.page(1)
        self.columns = ["name"]
        self.table = ModelTable(self.page, self.columns)

    def test_default_row_func(self):
        """
        Test the default_row_func method of the table.

        This test checks that the default_row_func method correctly generates
        a row for the given instance. It verifies that the generated row
        matches the expected output, which is a list containing the name
        of the instance.
        """
        instance = self.instances[0]
        row = self.table.default_row_func(instance)
        self.assertEqual(row, [self.instances[0].name])

    def test_custom_row_func(self):
        """
        Test the custom_row_func method of the ModelTable class.
        This test verifies that the custom_row_func correctly transforms the
        instance's name to uppercase and returns it in a list.
        Steps:
        1. Define a custom_row_func that takes an instance and returns a list
           containing the instance's name in uppercase.
        2. Create a ModelTable object with the custom_row_func.
        3. Call the row_func method of the ModelTable object with the first instance.
        4. Assert that the returned row is a list containing the instance's name
           in uppercase.
        """
        def custom_row_func(instance):
            """
            Converts the name attribute of the given instance to uppercase and returns it in a list.

            Args:
                instance (object): An object that has a 'name' attribute.

            Returns:
                list: A list containing the uppercase version of the instance's name.
            """
            return [instance.name.upper()]

        table = ModelTable(self.page, self.columns, custom_row_func)
        row = table.row_func(self.instances[0])
        self.assertEqual(row, [self.instances[0].name.upper()])

    def test_rows(self):
        """
        Tests the rows of the table.

        This test checks that the number of rows in the table is 10 and that the first row
        contains the name of the first instance.

        Assertions:
            - The number of rows in the table is 10.
            - The first row contains the name of the first instance.
        """
        rows = list(self.table.rows)
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0], [self.instances[0].name])

    def test_columns(self):
        """
        Test that the columns of the table are as expected.

        This test checks if the 'columns' attribute of the 'table' object
        contains exactly one column named "Name".
        """
        self.assertEqual(self.table.columns, ["Name"])

    def test_has_previous(self):
        """
        Test the `has_previous` property of the table.

        This test verifies that the `has_previous` property of the table is 
        correctly set based on the paginator's current page. Initially, it 
        asserts that `has_previous` is False when on the first page. Then, 
        it moves to the second page and asserts that `has_previous` is True.
        """
        self.assertFalse(self.table.has_previous)
        page = self.paginator.page(2)
        table = ModelTable(page, self.columns)
        self.assertTrue(table.has_previous)

    def test_has_next(self):
        """
        Test the `has_next` property of the table.

        This test verifies that the `has_next` property of the table is correctly
        set based on the paginator's current page. It checks that the property is
        True when there are more pages available and False when there are no more
        pages.

        Assertions:
            - The `has_next` property should be True when the table is initialized
              with the first page of the paginator.
            - The `has_next` property should be False when the table is initialized
              with the second page of the paginator.
        """
        self.assertTrue(self.table.has_next)
        page = self.paginator.page(2)
        table = ModelTable(page, self.columns)
        self.assertFalse(table.has_next)

    def test_previous_page_number(self):
        """
        Test that the previous_page_number property of the ModelTable class
        correctly returns the previous page number.

        This test creates a paginator page object for page 2 and a ModelTable
        instance using this page and the provided columns. It then asserts that
        the previous_page_number property of the ModelTable instance is 1.
        """
        page = self.paginator.page(2)
        table = ModelTable(page, self.columns)
        self.assertEqual(table.previous_page_number, 1)

    def test_next_page_number(self):
        """
        Test that the next_page_number property of the table returns the expected value.

        This test checks if the next_page_number property of the table instance
        returns 2, indicating that the pagination logic is functioning correctly.
        """
        self.assertEqual(self.table.next_page_number, 2)

    def test_page_number(self):
        """
        Test that the page number of the table is correctly set to 1.
        """
        self.assertEqual(self.table.page_number, 1)

    def test_page_size(self):
        """
        Test that the page size of the table is set to 10.

        This test verifies that the `page_size` attribute of the `table` object
        is correctly initialized to 10.
        """
        self.assertEqual(self.table.page_size, 10)

    def test_render(self):
        """
        Tests the render method of the table.

        This test checks if the rendered output of the table contains the string "Name".
        """
        rendered = self.table.render()
        self.assertIn("Name", rendered)

    def test_row_column_mismatch(self):
        """
        Test case to verify that a ValueError is raised when there is a mismatch
        between the number of columns defined and the number of columns returned
        by the custom row function.
        The custom_row_func returns a list with two elements, while the table is
        expected to have a different number of columns. This should trigger a
        ValueError when attempting to iterate over the table rows.
        """
        def custom_row_func(instance):
            """
            Generates a list containing the name attribute of the given instance twice.

            Args:
                instance: An object that has a 'name' attribute.

            Returns:
                A list containing the 'name' attribute of the instance repeated twice.
            """
            return [instance.name, instance.name]

        table = ModelTable(self.page, self.columns, custom_row_func)
        with self.assertRaises(ValueError):
            list(table.rows)

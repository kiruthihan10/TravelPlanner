"""
Country App Testing
"""

from django.core.paginator import Paginator

from common.models import Airport, City, Country, Flight, FlightPlan, Plan
from common.tests import BaseModelTest

from .tables import CountryTable
from .forms import CountryForm


class CountryModelTest(BaseModelTest):
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
            flight=self.create_n_flights(1, [airport3, airport2])[0],
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

    def test_cities(self):
        city1 = City.objects.create(name="TestCity1", country=self.country1)
        city2 = City.objects.create(name="TestCity2", country=self.country1)
        city3 = City.objects.create(name="TestCity3", country=self.country2)
        cities = self.country1.cities
        self.assertEqual(cities.count(), 2)
        self.assertIn(city1, cities)
        self.assertIn(city2, cities)
        self.assertNotIn(city3, cities)


class CountryFormTest(BaseModelTest):
    def test_form_fields(self):
        form = CountryForm()
        self.assertIn("name", form.fields)
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"], "Country Name"
        )

    def test_form_save(self):
        form_data = {"name": "Test Country"}
        form = CountryForm(data=form_data)
        self.assertTrue(form.is_valid())
        country = form.save()
        self.assertEqual(country.name, "Test Country")

    def test_render_form(self):
        form = CountryForm()
        rendered_form = form.render_form()
        self.assertIn('name="name"', rendered_form)
        self.assertIn('placeholder="Country Name"', rendered_form)


class CountryTableTest(BaseModelTest):
    """
    Test case for the CountryTable class.
    This test case includes the following tests:
    - Setting up the test environment with a list of countries.
    - Testing the default row function for a country instance.
    - Testing the string representation of the country table.
    """

    def setUp(self):
        """
        Set up the test environment.

        This method creates a list of country instances to be used in the tests.

        Attributes:
            countries (List[Country]): A list of country instances.
        """
        self.countries = self.create_n_countries(3)

    def test_default_row_func(self):
        """
        Test the default row function for a country instance.

        This test verifies that the default row function returns the correct number of columns
        for a given country instance.

        Assertions:
            - The default row function should return a list with two elements: the country's name and the count of its cities.
        """
        country = self.countries[0]
        paginator = Paginator(self.countries, 1)
        table = CountryTable(paginator.page(1))
        row = table.default_row_func(country)
        self.assertEqual(row, [country.name, country.cities.count()])

    def test_render(self):
        """
        Test the string representation of the country table.

        This test verifies that the string representation of the country table contains the correct column names
        and row values for each country instance.

        Assertions:
            - The rendered table should contain the column names "Name" and "Number of Cities".
            - The rendered table should contain the name and city count for each country instance.
        """
        paginator = Paginator(self.countries, len(self.countries))
        table = CountryTable(paginator.page(1))
        rendered_table = table.render()
        self.assertIn("Name", rendered_table)
        self.assertIn("Number of cities", rendered_table)
        for country in self.countries:
            self.assertIn(country.name, rendered_table)
            self.assertIn(str(country.cities.count()), rendered_table)

    def test_incorrect_type(self):
        """
        Test that the CountryTable raises a ValueError when an incorrect type is passed.

        This test verifies that the CountryTable raises a ValueError when an incorrect type is passed
        to the constructor.

        Assertions:
            - The CountryTable constructor should raise a ValueError when an incorrect type is passed.
        """
        paginator = Paginator([1, 2, 3], 1)
        with self.assertRaises(ValueError):
            CountryTable(paginator.page(1))


class CountryListViewTest(BaseModelTest):

    def setUp(self):
        self.countries = self.create_n_countries(3)

    def test_country_list(self):
        response = self.client.get("/country/")
        self.assertEqual(response.status_code, 200)
        for country in self.countries:
            self.assertContains(response, country.name)

    def test_country_list_search(self):
        response = self.client.get(f"/country/?search_text={self.countries[0].name}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.countries[0].name)


class CountryCreateViewTest(BaseModelTest):

    def test_create_country(self):
        response = self.client.get("/country/add")
        self.assertEqual(response.status_code, 200)
        form_data = {"name": "Test Country"}
        response = self.client.post("/country/add", form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Country.objects.count(), 1)
        country = Country.objects.first()
        if country:
            self.assertEqual(country.name, "Test Country")

    def test_incorrect_method(self):
        response = self.client.put("/country/add")
        self.assertEqual(response.status_code, 405)


class CityModelTest(BaseModelTest):
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
        self.city = self.create_n_cities(1, [self.country])[0]

    def test_city_creation(self):
        """
        Test the creation of a city object.

        This test verifies that the city object is created with the correct name and country attributes.

        Assertions:
            self.assertEqual(self.city.name, "TestCity"): Checks if the city's name is "TestCity".
            self.assertEqual(self.city.country, self.country): Checks if the city's country attribute matches the expected country.
        """
        self.assertEqual(self.city.name, str(self.city))
        self.assertEqual(self.city.country, self.country)


class SightseeingModelTest(BaseModelTest):
    """
    Test case for the Sightseeing model.
    This test case includes the following tests:
    - Setting up the test environment with a test country, city, and sightseeing object.
    - Testing the creation of a sightseeing object with the correct attributes.
    - Testing the string representation of the sightseeing object.
    - Testing that the sightseeing object's country matches the expected country.
    """

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
        self.sightseeing = self.create_n_sightseeings(1, [self.city])[0]

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
        self.assertEqual(self.sightseeing.name, str(self.sightseeing))

    def test_sightseeing_country(self):
        """
        Test that the sightseeing country matches the expected country.

        This test verifies that the `country` attribute of the `sightseeing` object
        is equal to the expected `country` attribute.
        """
        self.assertEqual(self.sightseeing.country, self.country)

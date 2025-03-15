"""
This module defines the models for the TravelPlanner application.
Models:
    Country: Represents a country with a name as the primary key.
    City: Represents a city with a name and a foreign key to Country.
    Sightseeing: Represents a sightseeing spot with a name, city, cost, description, and rating.
    Hotel: Represents a hotel with a name, city, and rating.
    Room: Represents a room in a hotel with a room type, date range, and cost.
    Airport: Represents an airport with a name and a foreign key to Country.
    Flight: Represents a flight with a name, departure and arrival airports, cost, and date-time information.
    Plan: Represents a travel plan with a name, version, and many-to-many relationships with rooms.
    FlightPlan: Represents a relationship between a flight and a plan with an order.
    SightseeingPlan: Represents a relationship between a sightseeing spot and a plan with an order.
"""

from typing import Set
from django.db import models


class Country(models.Model):
    """
    Represents a country in the TravelPlanner application.
    Attributes:
        name (str): The name of the country. This is the primary key.
    Methods:
        __str__(): Returns the name of the country.
        plans (property): Returns a queryset of plans associated with the country.
    """

    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    @property
    def plans(self):
        """
        Retrieves all Plan objects associated with the current country.

        Returns:
            QuerySet: A QuerySet containing all Plan objects that include the current country.
        """
        return Plan.objects.filter(
            models.Q(flightplan__flight__departure__country=self)
            | models.Q(flightplan__flight__arrival__country=self)
        ).distinct()

    @property
    def cities(self):
        """
        Retrieves all City objects associated with the current country.

        Returns:
            QuerySet: A QuerySet containing all City objects that are part of the current country.
        """
        return City.objects.filter(country=self)


class City(models.Model):
    """
    City model representing a city with a name and a reference to its country.

    Attributes:
        name (str): The name of the city. This is the primary key.
        country (ForeignKey): A foreign key reference to the Country model.
                              If the referenced country is deleted, the city will also be deleted.
    """

    name = models.CharField(max_length=100, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Sightseeing(models.Model):
    """
    Sightseeing model represents a tourist attraction or place of interest.
    Attributes:
        name (str): The name of the sightseeing location.
        city (City): The city where the sightseeing location is situated.
        cost (float): The cost associated with visiting the sightseeing location.
        description (str): A detailed description of the sightseeing location.
        rating (float): The rating of the sightseeing location.
    Properties:
        country (Country): The country where the sightseeing location is situated, derived from the associated city.
    Methods:
        __str__(): Returns the name of the sightseeing location.
    """

    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    cost = models.FloatField()
    description = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def country(self):
        """
        Returns the country associated with the city.

        Returns:
            str: The name of the country.
        """
        return self.city.country


class Hotel(models.Model):
    """
    Represents a hotel with a name, city, and rating.
    Attributes:
        name (str): The name of the hotel.
        city (City): The city where the hotel is located.
        rating (float): The rating of the hotel.
    Methods:
        __str__(): Returns the name of the hotel.
        country (property): Returns the country of the city where the hotel is located.
        rooms (property): Returns a queryset of rooms associated with the hotel.
    """

    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def country(self):
        """
        Returns the country associated with the city.

        Returns:
            str: The name of the country.
        """
        return self.city.country

    @property
    def rooms(self):
        """
        Retrieve all rooms associated with the current hotel instance.

        Returns:
            QuerySet: A Django QuerySet containing Room objects that are
                      associated with the current hotel instance.
        """
        return Room.objects.filter(hotel=self)


class Room(models.Model):
    """
    Room model representing a hotel room booking.
    Attributes:
        hotel (ForeignKey): Reference to the associated Hotel.
        room_type (CharField): Type of the room (e.g., single, double).
        from_date (DateField): Start date of the booking.
        to_date (DateField): End date of the booking.
        cost (FloatField): Total cost of the booking.
    Methods:
        __str__(): Returns a string representation of the room booking.
        duration_in_days (property): Calculates the duration of the booking in days.
        cost_per_day (property): Calculates the cost per day of the booking.
    """

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    cost = models.FloatField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

    @property
    def duration_in_days(self):
        """
        Calculate the duration between two dates in days.

        Returns:
            int: The number of days between `from_date` and `to_date`.
        """
        return (self.to_date - self.from_date).days

    @property
    def cost_per_day(self):
        """
        Calculate the cost per day of the travel plan.

        Returns:
            float: The cost per day calculated by dividing the total cost by the duration in days.
        """
        return self.cost / self.duration_in_days


class Airport(models.Model):
    """
    Represents an Airport model.
    Attributes:
        name (str): The name of the airport. Acts as the primary key.
        country (Country): The country where the airport is located. Foreign key to the Country model.
    Methods:
        __str__(): Returns the name of the airport.
        plans (property): Returns a queryset of Plan objects associated with the airport's country.
    """

    name = models.CharField(max_length=100, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def plans(self):
        """
        Retrieve plans associated with the current instance.

        Returns:
            QuerySet: A Django QuerySet containing the filtered `Plan` objects.
        """
        return Plan.objects.filter(
            models.Q(flightplan__flight__departure=self)
            | models.Q(flightplan__flight__arrival=self)
        ).distinct()


class Flight(models.Model):
    """
    Flight model representing a flight in the TravelPlanner application.
    Attributes:
        name (str): The name of the flight. Acts as the primary key.
        departure (ForeignKey): Foreign key to the Airport model representing the departure airport.
        arrival (ForeignKey): Foreign key to the Airport model representing the arrival airport.
        cost (float): The cost of the flight.
        departure_date_time (DateTimeField): The date and time of departure.
        arrival_date_time (DateTimeField): The date and time of arrival.
    Methods:
        __str__(): Returns the name of the flight.
        plans (QuerySet): Property that returns a queryset of Plan objects associated with the departure airport's country.
        duration_in_hours (float): Property that returns the duration of the flight in hours.
    """

    name = models.CharField(max_length=100, primary_key=True)
    departure = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure"
    )
    arrival = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrival"
    )
    cost = models.FloatField()
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def plans(self):
        """
        Retrieves all Plan objects associated with the current flight.
        Returns:
            QuerySet: A Django QuerySet containing all Plan objects that are linked
                      to the current flight through the flightplan relationship.
        """

        return Plan.objects.filter(flightplan__flight=self)

    @property
    def duration_in_hours(self):
        """
        Calculate the duration of the trip in hours.

        Returns:
            float: The duration of the trip in hours, calculated as the difference
            between arrival_date_time and departure_date_time in seconds divided by 3600.
        """
        return (self.arrival_date_time - self.departure_date_time).seconds / 3600


class Plan(models.Model):
    """
    Represents a travel plan with associated rooms, flights, and sightseeing activities.
    Attributes:
        name (str): The name of the plan, serving as the primary key.
        version (int): The version of the plan, default is 1.
        rooms (ManyToManyField): The rooms associated with the plan.
    Properties:
        countries (Set[Country]): A set of countries involved in the plan based on flight departures and arrivals.
        planes (QuerySet): A queryset of planes (flights) associated with the plan.
        sightseeings (QuerySet): A queryset of sightseeing activities associated with the plan.
        cost (int): The total cost of the plan, including rooms, sightseeing activities, and flights.
        duration_in_days (int): The duration of the plan in days, calculated from the first departure to the last arrival.
    Meta:
        unique_together (tuple): Ensures that the combination of name and version is unique.
    Raises:
        ValueError: If there are no planes in the plan when calculating the duration.
    """

    name = models.CharField(max_length=100, primary_key=True)
    version = models.IntegerField(default=1)
    rooms = models.ManyToManyField(Room)

    class Meta:
        """
        Meta class to define model-level options.

        Attributes:
            unique_together (tuple): Ensures that the combination of 'name' and 'version' fields is unique across the table.
        """

        unique_together = ("name", "version")

    @property
    def countries(self) -> Set[Country]:
        """
        Retrieves a set of countries involved in the flight plans associated with this plan.

        Returns:
            Set[Country]: A set of countries from the departure and arrival locations of the flight plans.
        """
        flight_plans = FlightPlan.objects.filter(plan=self)
        countries = set()
        for flight_plan in flight_plans:
            countries.add(flight_plan.flight.departure.country)
            countries.add(flight_plan.flight.arrival.country)
        return countries

    @property
    def planes(self):
        """
        Retrieve all planes associated with the current travel plan.

        This method filters the FlightPlan objects related to the current plan
        and then retrieves the corresponding Flight objects.

        Returns:
            QuerySet: A QuerySet containing all Flight objects associated with the current plan.
        """
        return Flight.objects.filter(flightplan__plan=self)

    @property
    def sightseeings(self):
        """
        Retrieve all sightseeings associated with the current plan.

        This method first fetches all SightseeingPlan objects related to the current plan.
        Then, it retrieves all Sightseeing objects that are part of these SightseeingPlan objects.

        Returns:
            QuerySet: A QuerySet containing all Sightseeing objects associated with the current plan.
        """
        sightseeing_plans = SightseeingPlan.objects.filter(plan=self)
        sightseeings = []
        for sightseeing_plan in sightseeing_plans:
            sightseeings.append(sightseeing_plan.sightseeing)
        return sightseeings

    @property
    def cost(self):
        """
        Calculate the total cost of the travel plan.

        This method sums up the costs of all rooms, sightseeings, and flights
        associated with the travel plan.

        Returns:
            int: The total cost of the travel plan.
        """
        cost = 0
        for room in self.rooms.all():
            cost += room.cost
        for sightseeing in self.sightseeings:
            cost += sightseeing.cost
        for flight in self.planes:
            cost += flight.cost
        return cost

    @property
    def duration_in_days(self):
        """
        Calculate the duration of the travel plan in days.

        This method determines the duration of the travel plan by calculating the
        difference in days between the departure time of the first plane and the
        arrival time of the last plane in the plan.

        Returns:
            int: The duration of the travel plan in days.

        Raises:
            ValueError: If there are no planes in the plan.
        """
        last_plane = self.planes.order_by("arrival_date_time").last()
        first_plane = self.planes.order_by("departure_date_time").first()
        if (last_plane is None) or (first_plane is None):
            raise ValueError("No planes in the plan")
        return (last_plane.arrival_date_time - first_plane.departure_date_time).days


class FlightPlan(models.Model):
    """
    FlightPlan model represents the relationship between a Flight and a Plan.
    Attributes:
        flight (ForeignKey): A reference to the Flight model.
        plan (ForeignKey): A reference to the Plan model.
        order (IntegerField): An integer representing the order of the flight plan.
    Meta:
        unique_together (tuple): Ensures that each combination of flight and plan is unique.
        ordering (list): Orders the flight plans by the 'order' field.
    Properties:
        countries (list): A list containing the departure and arrival countries of the flight.
    """

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        """
        Meta class for model options.

        Attributes:
            unique_together (tuple): Ensures that the combination of 'flight' and 'plan' is unique.
            ordering (list): Specifies the default ordering for the model, based on the 'order' field.
        """

        unique_together = ("flight", "plan")
        ordering = ["order"]

    @property
    def countries(self):
        """
        Returns a list of countries involved in the flight.

        This method retrieves the departure and arrival countries
        associated with the flight and returns them as a list.

        Returns:
            list: A list containing the departure country and arrival country.
        """
        return [self.flight.departure.country, self.flight.arrival.country]


class SightseeingPlan(models.Model):
    """
    SightseeingPlan model represents the relationship between a sightseeing activity and a travel plan.
    Attributes:
        sightseeing (ForeignKey): A reference to the Sightseeing model. When the referenced Sightseeing is deleted, relationship will also be deleted.
        plan (ForeignKey): A reference to the Plan model. When the referenced Plan is deleted, this relationship will also be deleted.
        order (IntegerField): An integer representing the order of the sightseeing activity within the plan.
    Meta:
        unique_together (tuple): Ensures that the combination of sightseeing and plan is unique.
        ordering (list): Orders the SightseeingPlan instances by the 'order' field.
    """

    sightseeing = models.ForeignKey(Sightseeing, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        """
        Meta class to define model-level options.

        Attributes:
            unique_together (tuple): Ensures that the combination of 'sightseeing' and 'plan' is unique.
            ordering (list): Specifies the default ordering of records by the 'order' field.
        """

        unique_together = ("sightseeing", "plan")
        ordering = ["order"]

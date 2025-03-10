from typing import Set
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    @property
    def plans(self):
        return Plan.objects.filter(countries=self)


class City(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Sightseeing(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    cost = models.FloatField()
    description = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def country(self):
        return self.city.country


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def country(self):
        return self.city.country

    @property
    def rooms(self):
        return Room.objects.filter(hotel=self)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    cost = models.FloatField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

    @property
    def duration_in_days(self):
        return (self.to_date - self.from_date).days

    @property
    def cost_per_day(self):
        return self.cost / self.duration_in_days


class Airport(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def plans(self):
        return Plan.objects.filter(countries=self.country)


class Flight(models.Model):
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
        return Plan.objects.filter(countries=self.departure.country)

    @property
    def duration_in_hours(self):
        return (self.arrival_date_time - self.departure_date_time).seconds / 3600


class Plan(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    version = models.IntegerField(default=1)
    rooms = models.ManyToManyField(Room)

    class Meta:
        unique_together = ("name", "version")

    @property
    def countries(self) -> Set[Country]:
        flightPlans = FlightPlan.objects.filter(plan=self)
        countries = set()
        for flightPlan in flightPlans:
            countries.add(flightPlan.flight.departure.country)
            countries.add(flightPlan.flight.arrival.country)
        return countries

    @property
    def planes(self):
        flightPlans = FlightPlan.objects.filter(plan=self)
        planes = Flight.objects.filter(flight__in=flightPlans)
        return planes

    @property
    def sightseeings(self):
        sightseeingPlans = SightseeingPlan.objects.filter(plan=self)
        sightseeings = Sightseeing.objects.filter(sightseeing__in=sightseeingPlans)
        return sightseeings

    @property
    def cost(self):
        cost = 0
        for room in self.rooms.all():
            cost += room.cost
        for sightseeing in self.sightseeings.all():
            cost += sightseeing.cost
        for flight in self.planes:
            cost += flight.cost
        return cost

    @property
    def duration_in_days(self):
        last_plane = self.planes.order_by("arrival_date_time").last()
        first_plane = self.planes.order_by("departure_date_time").first()
        if (last_plane is None) or (first_plane is None):
            raise ValueError("No planes in the plan")
        return (last_plane.arrival_date_time - first_plane.departure_date_time).days


class FlightPlan(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ("flight", "plan")
        ordering = ["order"]

    @property
    def countries(self):
        return [self.flight.departure.country, self.flight.arrival.country]


class SightseeingPlan(models.Model):
    sightseeing = models.ForeignKey(Sightseeing, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        unique_together = ("sightseeing", "plan")
        ordering = ["order"]


# Create your models here.

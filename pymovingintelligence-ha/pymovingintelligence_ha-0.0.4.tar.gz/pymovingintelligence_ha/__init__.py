"""Home Assistant Python 3 API wrapper for Moving Intelligence."""
import datetime
import logging

from .utils import Utilities

_LOGGER = logging.getLogger("pymovingintelligence_ha")


class MovingIntelligence:
    """Class for communicating with the Moving Intelligence API."""

    def __init__(
        self,
        username: str = None,
        apikey: str = None,
    ):
        """Init module."""

        self.utilities = Utilities(username, apikey)

    def get_devices(self) -> dict:
        """Get objects."""
        result = []

        objects = self.utilities.request(
            "GET",
            endpoint="/v1/objects",
        )

        for object in objects:
            device = Device(self.utilities, object["licence"])
            device.update_from_json(object)
            if device.odo:
                result.append(device)

        return result


class Device:
    """Entity used to store device information."""

    def __init__(self, utilities, license_plate):
        """Initialize a device, also a vehicle."""
        self._utilities = utilities

        self.identifier = None
        self.make = None
        self.model = None
        self.license_plate = license_plate
        self.chassisnumber = None
        self.startdate = None
        self.year = None
        self.remarks = None
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.odo = 0
        self.speed = 0
        self.street = None
        self.city = None
        self.country = None
        self.last_distance = None
        self.last_seen = None

    @property
    def plate_as_id(self):
        """Format the license plate so it can be used as identifier."""
        return self.license_plate.replace("-", "")

    @property
    def object_name(self):
        """Compose a friendly name."""
        return f"{self.license_plate} {self.make} {self.model}"

    @property
    def state_attributes(self):
        """Return all attributes of the vehicle."""

        return {
            "id": self.identifier,
            "make": self.make,
            "model": self.model,
            "license_plate": self.license_plate,
            "chassis_number": self.chassisnumber,
            "startdate": self.startdate,
            "year": self.year,
            "remarks": self.remarks,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "odo": self.odo,
            "speed": self.speed,
            "street": self.street,
            "city": self.city,
            "country": self.country,
            "last_distance": self.last_distance,
            "last_seen": self.last_seen,
        }

    def update_from_json(self, json_device):
        """Set all attributes based on API response."""
        self.identifier = json_device["id"]
        self.license_plate = json_device["licence"]
        self.make = json_device["brand"]
        self.model = json_device["model"]
        self.chassisnumber = json_device["chassisNumber"]
        if "startDate" in json_device:
            start = datetime.datetime.fromtimestamp(json_device["startDate"])
            self.startdate = start.strftime("%Y-%m-%d %H:%M:%S")
        if "yearOfManufacture" in json_device:
            self.year = json_device["yearOfManufacture"]
        if "remarks" in json_device:
            self.remarks = json_device["remarks"]
        self.odo = self.get_odometer(self.identifier)

        trip = self.get_object_detailed_trips(
            self.identifier, "CURRENT_MONTH", "UNKNOWN"
        )

        if trip:
            location = trip[-1]["locationAndSpeed"]
            if len(location) > 0 and location[-1].get("lat") is not None:
                self.latitude = float(location[-1]["lat"] / 1000000)
                self.longitude = float(location[-1]["lon"] / 1000000)
                self.speed = location[-1]["speed"]

            self.street = trip[-1]["endRoad"]
            self.city = trip[-1]["endCity"]
            self.country = trip[-1]["endCountry"]
            self.last_distance = trip[-1]["distance"] / 1000
            if trip[-1]["endDate"]:
                when = datetime.datetime.fromtimestamp(trip[-1]["endDate"])
                self.last_seen = when.strftime("%Y-%m-%d %H:%M:%S")


    def get_odometer(self, object_id: str, date=None) -> dict:
        """Get odometer readings."""

        odometer = None
        data = self._utilities.request(
            "GET",
            endpoint=f"/v1/object/{object_id}/odometer",
            params=self._utilities.clean_request_params({"date": date}),
        )

        if data:
            odometer = int(data["odoInMeters"] / 1000)

        return odometer

    def get_object_detailed_trips(
        self, object_id: str, period: str, classifications) -> dict:
        """Get detailed trips for object."""

        return self._utilities.request(
            "GET",
            endpoint=f"/v1/object/{object_id}/detailedtrips",
            params=self._utilities.clean_request_params(
                {
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

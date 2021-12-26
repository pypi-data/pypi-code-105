"""Python 3 API wrapper for Moving Intelligence."""
import logging
from .utils import Utilities

_LOGGER = logging.getLogger("pymovingintelligence")

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

        data = self.utilities.request(
            "GET",
            endpoint="/v1/objects",
        )
        return self.parse_devices(data)

    def parse_devices(self, json):
        """Parse result from API."""
        result = []

        for json_device in json:
            license_plate = json_device["licence"]

            device = Device(self.utilities, license_plate)
            device.update_from_json(json_device)
            if device.odo:
                result.append(device)

        return result


class Device:
    """Entity used to store device information."""

    def __init__(self, utilities, license_plate):
        """Initialize a device, also a vehicle."""
        self._utilities = utilities
        self.license_plate = license_plate

        self.identifier = None
        self.make = None
        self.model = None
        self.odo = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.speed = 0
        self.last_seen = None
        self.equipment_id = None
        self.last_distance = None
        self.current_address = None
        self.street = None
        self.city = None
        self.country = None

    @property
    def plate_as_id(self):
        """Format the license plate so it can be used as identifier."""
        return self.license_plate.replace("-", "")

    @property
    def state_attributes(self):
        """Return all attributes of the vehicle."""

        return {
            "id": self.identifier,
            "make": self.make,
            "model": self.model,
            "license_plate": self.license_plate,
            "odo": self.odo,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "speed": self.speed,
            "last_seen": self.last_seen,
            "friendly_name": f"{self.license_plate} {self.make} {self.model}",
            "equipment_id": self.equipment_id,
            "last_distance": self.last_distance,
            "current_address": self.current_address,
        }

    def update_from_json(self, json_device):
        """Set all attributes based on API response."""
        self.identifier = json_device["id"]
        self.license_plate = json_device["licence"]
        self.make = json_device["brand"]
        self.model = json_device["model"]
        self.equipment_id = json_device["chassisNumber"]

        self.odo = self.get_odometer(self.identifier)

        trip = self.get_object_detailed_trips(
            self.identifier, "CURRENT_MONTH", "UNKNOWN"
        )
        if trip:
            for entry in range(len(trip)):
                location = trip[entry]["locationAndSpeed"]
                if len(location) > 0 and location[-1].get("lat") is not None:
                    self.latitude = float(location[-1]["lat"] / 1000000)
                    self.longitude = float(location[-1]["lon"] / 1000000)
                    self.speed = location[-1]["speed"]

                self.street = trip[entry]["endRoad"]
                self.city = trip[entry]["endCity"]
                self.country = trip[entry]["endCountry"]
                self.last_distance = trip[entry]["distance"] / 1000
                self.last_seen = trip[entry]["endDate"]

        self.current_address = {
            "address": self.street,
            "city": self.city,
            "country": self.country,
        }

    def get_odometer(self, object_id: str, date=None) -> dict:
        """Get odometer readings."""

        odometer = None
        data = self._utilities.request(
            "GET",
            endpoint=f"/v1/object/{object_id}/odometer",
            params=self._utilities.clean_request_params({"date": date}),
        )

        if data:
            odometer = int(data["odoInMeters"]/1000)

        return odometer

    def get_object_detailed_trips(
        self, object_id: str, period: str, classifications, startdate=None, enddate=None
    ) -> dict:
        """Get detailed trips for object."""

        return self._utilities.request(
            "GET",
            endpoint=f"/v1/object/{object_id}/detailedtrips",
            params=self._utilities.clean_request_params(
                {
                    "startDate": startdate,
                    "endDate": enddate,
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

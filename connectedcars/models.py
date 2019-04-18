import attr
import datetime
import dateutil.parser

@attr.s
class Vehicle:
    """Represents a vehicle overview."""
    id = attr.ib(type=int)
    licensePlate = attr.ib(init=False)
    make = attr.ib(init=False)
    model = attr.ib(init=False)
    name = attr.ib(init=False)
    fuelEconomy = attr.ib(init=False, type=int)
    position = attr.ib(init=False)
    fuelLevel = attr.ib(init=False)
    odometer = attr.ib(init=False)
    
    @classmethod
    def create_from_dict(cls, dict):
        """Creates an instance from data in dictionary"""

        vehicle = Vehicle(int(dict['id']))
        vehicle.licensePlate = str(dict['licensePlate'])
        vehicle.make = str(dict['make'])
        vehicle.model = str(dict['model'])
        vehicle.name = str(dict['name'])
        vehicle.fuelEconomy = float(dict['fuelEconomy'])

        if dict['position'] is not None:
            vehicle.position = VehiclePosition.create_from_dict(dict['position'])

        if dict['fuelLevel'] is not None:
            vehicle.fuelLevel = VehicleFuelLevel.create_from_dict(dict['fuelLevel'])

        if dict['odometer'] is not None:
            vehicle.odometer = VehicleOdometer.create_from_dict(dict['odometer'])

        return vehicle

@attr.s
class VehiclePosition:
    """Represents a single position of a vehicle at a specific mesurement time."""
    time = attr.ib(type=str)
    latitude = attr.ib(type=float)
    longitude = attr.ib(type=float)

    @classmethod
    def create_from_dict(cls, dict):
        """Creates an instance from data in dictionary"""
        return VehiclePosition(
            dateutil.parser.parse(dict['time']),
            float(dict['latitude']),
            float(dict['longitude'])
        )

@attr.s
class VehicleFuelLevel:
    """Represents the fuel level of a vehicle at a specific measurement time."""
    time = attr.ib(type=datetime.datetime)
    liter = attr.ib(type=float)

    @classmethod
    def create_from_dict(cls, dict):
        """Creates an instance from data in dictionary"""
        return VehicleFuelLevel(
            dateutil.parser.parse(dict['time']),
            float(dict['liter'])
        )

@attr.s
class VehicleOdometer:
    """Represents the odometer state of a vehicle at a specific measurement time."""
    time = attr.ib(type=datetime.datetime)
    odometer = attr.ib(type=float)

    @classmethod
    def create_from_dict(cls, dict):
        """Creates an instance from data in dictionary"""
        return VehicleOdometer(
            dateutil.parser.parse(dict['time']),
            float(dict['odometer'])
        )

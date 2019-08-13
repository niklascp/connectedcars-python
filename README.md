# Python wrapper for the ConnectedCars REST API 

Connected Cars is an AVL/data collection service installed in most new **danish** vehicles from Audi, Volkswagen, Skoda and SEAT. The service has an API that is using *GraphQL*. This is a thin python wrapper for that API which handles authentication and refresh of access tokens. It allows the direct execution of *GraphQL* queries, but also includes some predefined queries that returns pyton objects for convenience.

## Installation

```pip install connectedcars```

## Data available

Depends on the car, but examples includes:

- gps position
- fuel level
- odometer

## Usage
```python
from connectedcars import ConnectedCarsClient

client = ConnectedCarsClient(username = 'XXX', password = 'XXX', namespace = 'XXX')
vehicles = client.vehicles_overview()

for vehicle in vehicles:
  print(vehicle.make, vehicle.model, vehicle.fuelLevel.liter)
```

Could output something like:
```
Volkswagen Golf 38.0
```

## Namespaces
You will need to provide a namespace corresponding to your login. Known namespaces are:

- `semler:minvolkswagen`

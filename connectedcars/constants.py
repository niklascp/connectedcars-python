AUTH_URL = "https://auth-api.connectedcars.io/auth/login/email/password"
API_URL = "https://api.connectedcars.io/graphql"
API_DEFAULT_TIMEOUT = 30

HEADER_NAMESPACE = "x-organization-namespace"

QUERY_COMPLETE = """
query User {
    viewer {
        id
        firstname
        lastname
        email
        vehicles {
        vehicle {
            id
            vin
            class
            brand
            make
            model
            name
            licensePlate
            fuelType
            fuelLevel {
                liter
            }
            fuelPercentage {
                percent
            }
            odometer {
                odometer
            }
            position {
                latitude
                longitude
            }
            refuelEvents {
                litersDifference
                time
            }
            latestBatteryVoltage {
                voltage
            }
            health {
                ok
                recommendation
            }
            trips (last:3) {
                items {
                    duration
                    fuelUsed
                    mileage
                    startLongitude
                    startLatitude
                    endLongitude
                    endLatitude
                }
            }
        }
        }
    }
}"""
QUERY_USER = """
query User {
    viewer {
        id
        firstname
        lastname
        email
    }
}"""
QUERY_VEHICLE_VIN = """
query User {
    viewer {
        vehicles {
            vehicle {
                id
                vin
            }
        }
    }
}"""
QUERY_VEHICLE_OVERVIEW = """
query User {
    viewer {
        vehicles {
            vehicle {
                id
                licensePlate
                unitSerial
                make
                model 
                name
                fuelEconomy
                health {
                    ok
                    recommendation
                }
                ignition {
                    time
                    on
                }
                odometer { 
                    time 
                    odometer
                }
                fuelLevel { 
                    time
                    liter
                }
                position { 
                    time
                    latitude
                    longitude 
                }
            }
        }
    }
}
"""
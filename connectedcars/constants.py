AUTH_URL = "https://auth-api.connectedcars.io/auth/login/email/password"
API_URL = "https://api.connectedcars.io/graphql"
API_TIMEOUT = 15

HEADER_NAMESPACE = "x-organization-namespace"

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
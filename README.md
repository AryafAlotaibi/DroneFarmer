# DroneFarmer
DroneFarmer is a simulated agricultural drone system for No-Till Farming. It simulates autonomous seed dispersal and GPS tracking in a zigzag pattern, demonstrating the concept of smart, automated farming without human intervention or plowing.


## Features

- **Autonomous Flight Path**: The drone follows a zigzag flight pattern to cover the entire area efficiently.
- **Simulated Seed Dispersal**: The drone simulates the process of dropping seeds without human intervention or plowing.
- **Aerial Image Capture Simulation**: The drone captures simulated images of the field to aid in crop monitoring (currently not functional in the simulator).
- **Location Tracking**: Continuously tracks the drone’s position using GPS, providing precise data on the coverage area.
- **Distance Calculation**: Calculates the distance between the drone’s current location and the home point using the Haversine formula.
- **Battery Estimation**: Estimates battery consumption based on the distance traveled.
- **Battery Monitoring**: Monitors battery level and automatically decides to either return to launch or land safely if the battery is low.
- **Autonomous Control**: The drone operates autonomously without manual intervention, making it ideal for large-scale, automated farming.



## Setup
To run the drone simulation, PX4 Autopilot and jMAVSim must be installed in a Linux-based environment.  
Please follow standard PX4 installation procedures available at [PX4 Documentation](https://docs.px4.io/main/en/).   


 

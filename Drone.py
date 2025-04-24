import asyncio
from mavsdk import System
import random
import math


# Haversine formula to calculate distance in meters between two GPS points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c  # Output in meters

# Simple battery consumption estimator (We assumed 1% battery per 100 meters)
def estimate_battery_for_distance(distance_m):
    battery_per_meter = 1 / 100  # 1% battery per 100 meter
    return distance_m * battery_per_meter


async def drone_screening():
    # Connect to the drone
    drone = System()
    print("Connecting to drone!")
    await drone.connect(system_address="udp://:14540")
    print("Drone connected!")

    # Arming
    print("Arming...")
    await drone.action.arm()
    print("Armed")

    # Takeoff
    print("Taking off;)...")
    await drone.action.takeoff()
    await asyncio.sleep(6)

    # Get home position
    home_position = await anext(drone.telemetry.home())
    home_lat = home_position.latitude_deg
    home_lon = home_position.longitude_deg
    alt = 10.0


    print("Starting area scan...")
    # Define grid size (3 rows, 6 columns)
    rows = 3
    cols = 6
    step_lat = 0.00005  # ~5m per step
    step_lon = 0.00005

    # Get home position
    home = await anext(drone.telemetry.position())
    home_lat = home.latitude_deg
    home_lon = home.longitude_deg
    alt = home.absolute_altitude_m + 5

    # Zigzag screening pattern
    for i in range(rows):
        for j in range(cols):
            if i % 2 == 0:
                lon_offset = j * step_lon  # left to right
            else:
                lon_offset = (cols - 1 - j) * step_lon  # right to left

            lat_offset = i * step_lat
            target_lat = home_lat + lat_offset
            target_lon = home_lon + lon_offset

            print(f"Flying to point ({target_lat}, {target_lon})")
            await drone.action.goto_location(target_lat, target_lon, alt, 0)
            await asyncio.sleep(3)


            # Capture image
            if random.random() < 0.3:
                print("Capturing image... (simulated)")
                #await drone.camera.take_photo()

                # Get current location (location of the drone when capturing the image)
                current_position = await anext(drone.telemetry.position())
                current_lat = current_position.latitude_deg
                current_lon = current_position.longitude_deg

                # Save the location (you can print it or save to a list/file)
                print(f"Image captured at location: Latitude = {current_lat}, Longitude = {current_lon}")



            # Battery check
            battery = await anext(drone.telemetry.battery())
            remaining = battery.remaining_percent

            # Get current position
            current_position = await anext(drone.telemetry.position())
            current_lat = current_position.latitude_deg
            current_lon = current_position.longitude_deg

            # Calculate distance to home
            distance_to_home = haversine(current_lat, current_lon, home_lat, home_lon)
            required_battery = estimate_battery_for_distance(distance_to_home) #"1% بطارية لكل 100 متر"

            print(f"Battery: {remaining:.1f}%, Distance to home: {distance_to_home:.1f}m, Required battery: {required_battery:.2f}%")

            if remaining * 100 < 40:
                if remaining * 100 > required_battery:
                    print("Battery low, but return is possible. Returning to launch...")
                    await drone.action.return_to_launch()
                else:
                    print("Battery too low to return. Landing now...")
                    await drone.action.land()
                return

    # Return to home after full scan (Includes land)
    print("Scan complete. Returning to home.")
    await drone.action.return_to_launch()

asyncio.run(drone_screening())

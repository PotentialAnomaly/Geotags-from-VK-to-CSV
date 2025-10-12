"""Main script for collecting VK geotags.

This script configures search parameters and calls functions
from vk_geotags module to collect geotagged photos from VK API.
"""

from vk_geotags import get_geotag_csv


def main():
    """Configure your parameters and run the geotag collector."""
    # Setting the search parameters.
    # For all types of parameters call help(get_geotag_csv)
    
    # Search query (searches in descriptions, titles, tags)
    # Empty string = all photos
    q = '' 
  
    # Example: Saint Petersburg, Russia
    lat = 60  # Latitude in decimal degrees (from -90 to 90)
    long = 30  # Longitude in decimal degrees (from -180 to 180)
    radius = 50000  # Search radius: must be 10, 100, 800, 6000, or 50000 meters

    # Example time period: March 8, 2021, 12:00 - 16:00
    # The time in tuple format (year, month, day, hour, minute, second)
    start_time = (2021, 3, 8, 12, 0, 0) # Photos uploaded not earlier than this time
    end_time = (2021, 3, 8, 16, 0, 0)  # Photos uploaded no later than this time
    
    sort = 0  # Sort order: 0 - by date, 1 - by likes
    
    csv_filename = 'geotags8marta.csv'  # Output filename with .csv

    # Run the collector
    print(f"Starting geotag collection...")
    print(f"Location: ({lat}, {long}), Radius: {radius}m")
    print(f"Time period: {start_time} to {end_time}")

    get_geotag_csv(q, lat, long, radius, start_time, end_time, sort,
                   csv_filename)

    print(f"Done! Results saved to {csv_filename}")


if __name__ == '__main__':
    main()

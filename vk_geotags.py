"""Module for retrieving photo geotags from VK API.

This module provides functions to search for geotagged photos on VK
and save the results to a CSV file.
"""

# Local application imports
from config import API_VERSION, SERVICE_TOKEN

def get_photos(q, lat, long, radius, start_time_unix, end_time_unix, count, offset, sort):
    """Get photos data from VK API
    Args:
        q (str): Search query string (searches in descriptions, titles, tags).
            Empty string returns all photos.
        lat (float): Latitude in decimal degrees (from -90 to 90).
        long (float): Longitude in decimal degrees (from -180 to 180).
        radius (int): Search radius in meters. Must be one of the following 
            values: 10, 100, 800, 6000, or 50000.
        start_time_unix (int): Start time in Unix timestamp format. Photos 
            uploaded not earlier than this time will be returned.
        end_time_unix (int): End time in Unix timestamp format. Photos 
            uploaded no later than this time will be returned.
        count (int): Number of photos to get (maximum 1000).
        offset (int): Allows you to upload the next count of photos (limit 3000 per request).
        sort (int): Sort order (0 - by upload date, 1 - by number of likes).
    
    Returns:
        requests.Response: Response from VK API containing photo data.
        """
    parameters = {
         'q': q,
        'lat': lat,
        'long': long,
        'radius': radius,
        'start_time': start_time_unix,
        'end_time': end_time_unix,
        'count': count,
        'offset': offset,
        'sort': sort,
        'v': API_VERSION,
        'access_token': SERVICE_TOKEN}
    response = requests.get('https://api.vk.com/method/photos.search',
    params=parameters)
    return response

def get_geotag_csv(q, lat, long, radius, start_time, end_time, sort, csv_filename):
    """Get CSV with VK photos data (Date, Owner_ID, Photo_ID, Lat,Long).
    
        Args:
        q (str): Search query string (searches in descriptions, titles, tags).
            Empty string returns all photos.
        lat (float): Latitude in decimal degrees (from -90 to 90).
        long (float): Longitude in decimal degrees (from -180 to 180).
        radius (int): Search radius in meters. Must be one of the following 
            values: 10, 100, 800, 6000, or 50000.
        start_time (tuple): Start of time period in tuple format
            (year, month, day, hour, minute, second). Time zone: UTC±0:00.
            Photos uploaded not earlier than this time will be returned.
            Example: (2020, 3, 12, 0, 0, 0).
        end_time (tuple): End of time period in tuple format
            (year, month, day, hour, minute, second). Time zone: UTC±0:00.
            Photos uploaded no later than this time will be returned.
            Example: (2021, 7, 12, 23, 59, 59).
        sort (int): Sort order (0 - by upload date, 1 - by number of likes).
        csv_filename (str): Output filename with .csv extension for saving 
            results.
    
    Returns:
        None: Function saves results directly to CSV file.
        """
    # Convert time to Unix timestamp
    start_time_unix = int(datetime(*start_time).timestamp())
    end_time_unix = int(datetime(*end_time).timestamp())

    # Lists to store data
    dates = []
    lats = []
    longs = []
    photo_ids = []
    owner_ids = []

    # Maximum 3000 photos (3 requests of 1000 each)
    for offset in [0, 1000, 2000]:
        response = get_photos(q, lat, long, radius,
            start_time_unix, end_time_unix, 1000, offset, sort)
        data = response.json()
        
        items = data.get('response', {}).get('items', [])

        # Stop if no more photos are available
        if not items:
            break

        # Extract data from each photo
        for item in items:
            date = item.get('date')
            lat_coord = item.get('lat')
            long_coord = item.get('long')
            photo_id = item.get('id')
            owner_id = item.get('owner_id')

            # Only add photos with complete geodata
            if date is not None and lat_coord is not None and long_coord is not None:
                dates.append(date)
                lats.append(lat_coord)
                longs.append(long_coord)
                photo_ids.append(photo_id)
                owner_ids.append(owner_id)
                
        
        # Check if the end of the data has been reached (so as not to include duplicate values)
        total_count = data.get('response', {}).get('count', 0)
        if offset + len(items) >= total_count:
            break
        
        time.sleep(0.5)  # Pause between requests to avoid being banned

    # Save data to CSV file
    np.savetxt(csv_filename,
               np.column_stack((dates, owner_ids, photo_ids, lats, longs)),
               fmt='%f',
               delimiter=',',
               header='Date,Owner_ID,Photo_ID,Lat,Long',
               comments='')

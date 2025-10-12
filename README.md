# VK Geotag Collector

> [Русская версия](README.ru.md) | **English version** 🌍

Python script for collecting geotagged photos from VK API and exporting them to CSV format.

## 📋 Features

- 🌍 Search photos by geographic location (latitude, longitude, radius)
- ⏰ Filter by date and time (down to seconds)
- 📊 Export to CSV format (Date, Owner_ID, Photo_ID, Lat, Long)
- 🔄 Pagination support (up to 3000 photos per request)
- ⚡ Rate limiting to prevent API bans

## 🏙️ Purpose

Social media geotag research is an important part of both academic and applied geography. By visualizing CSV data as points on a map in ArcGIS or QGIS, you can understand where and when people spend their time — where to place a business location (geomarketing), where agglomeration boundaries end (population geography), and more.

Of course, where people post photos doesn't fully reflect where they take photos, and doesn't always reflect where they spend time during routine activities (home, work). But photo geotags, unlike mobile operator data, are a simple and accessible tool for approximate understanding of population activities.

## 🚀 Getting Started

### Requirements

- Python 3.7+
- VK API service token

### Installation

1. Clone the repository:
git clone https://github.com/PotentialAnomaly/Geotags-from-VK-to-CSV.git  
cd Geotags-from-VK-to-CSV

2. Install dependencies:
pip install -r requirements.txt

3. Create configuration file:
cp config.example.py config.py

4. Edit `config.py` and add your VK API credentials:
   - Get service token by registering an application (takes 5 minutes with a VK account): https://vk.com/apps?act=manage
   - (IF THE PROJECT REVIEWER DOESN'T HAVE TIME TO GET A TOKEN, THEY CAN MESSAGE ME ON TELEGRAM @unumerratum)

## 📖 Usage

### Method 1: Using the main script

1. Edit parameters in `main.py`:
q = '' # Search query (empty = all photos)  
lat = 60 # Latitude  
long = 30 # Longitude  
radius = 50000 # Radius in meters (10, 100, 800, 6000, or 50000)  
start_time = (2021, 3, 8, 12, 0, 0) # Start time  
end_time = (2021, 3, 8, 16, 0, 0) # End time  
sort = 0 # Sort: 0 = by date, 1 = by likes  
csv_filename = 'output.csv'  

2. Run the script:
python main.py

### Method 2: Import as a module

from vk_geotags import get_geotag_csv

get_geotag_csv(
q='',
lat=60,
long=30,
radius=50000,
start_time=(2021, 3, 8, 12, 0, 0),
end_time=(2021, 3, 8, 16, 0, 0),
sort=0,
csv_filename='output.csv')

## 📊 Output Format

CSV file with the following columns:

| Column | Description |
|--------|-------------|
| Date | Unix timestamp of photo upload |
| Owner_ID | VK user ID who uploaded the photo |
| Photo_ID | VK photo ID |
| Lat | Latitude of the photo |
| Long | Longitude of the photo |

## 🔧 Parameters

- **q** (str): Search query string (searches in titles, descriptions, photo tags). Empty string returns all photos.
- **lat** (float): Latitude in decimal degrees (from -90 to 90).
- **long** (float): Longitude in decimal degrees (from -180 to 180).
- **radius** (int): Search radius in meters. Valid values: 10, 100, 800, 6000, or 50000.
- **start_time** (tuple): Start of time period (year, month, day, hour, minute, second).
- **end_time** (tuple): End of time period (same format).
- **sort** (int): Sort order (0 - by date, 1 - by likes).
- **csv_filename** (str): Output filename with .csv extension.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Arthur Shlein**  
Faculty of Geography and Geoinformation Technology, HSE University

- GitHub: [@PotentialAnomaly](https://github.com/PotentialAnomaly)

## 🙏 Acknowledgments

- VK API documentation: https://dev.vk.com/

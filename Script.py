import requests
import os

URL = "https://mesonet.agron.iastate.edu/api/1/currents.json?network=NE_DCP"
OUTPUT_FILE = "NE_mesonet.txt"

def create_placefile():
    try:
        headers = {'User-Agent': 'PlacefileBot/1.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        data = response.json().get('data', [])

        with open(OUTPUT_FILE, "w") as f:
            f.write("Refresh: 5\n")
            f.write("Threshold: 999\n")
            f.write("Title: NE Mesonet (Wind Barbs)\n")
            # ADD THIS LINE: Font Number 1, 12px height, Bold (1), "Arial"
            f.write("Font: 1, 12, 1, \"Arial\"\n")
            f.write("IconFile: 1, 32, 32, 16, 16, \"https://raw.githubusercontent.com/pbrady/Placefiles/master/wind_barbs.png\"\n\n")

            for station in data:
                lat, lon = station.get('lat'), station.get('lon')
                stid, temp = station.get('station'), station.get('tmpf')
                wind_kts, wind_dir = station.get('sknt'), station.get('drct')

                if any(v is None for v in [lat, lon, temp, wind_kts, wind_dir]):
                    continue

                icon_index = int(round(wind_kts / 5.0))
                if icon_index > 25: icon_index = 25
                
                wind_mph = round(wind_kts * 1.15, 1)

                f.write(f"Object: {lat},{lon}\n")
                f.write(f"  Threshold: 999\n")
                f.write(f"  Color: 255 255 255\n")
                f.write(f"  Text: -10, -10, 1, \"{int(temp)}\"\n")
                f.write(f"  Icon: 0, 0, {int(wind_dir)}, {icon_index}, 1, \"{stid}: {temp}F, {wind_mph}mph\"\n")
                f.write("End:\n\n")
        print("Update successful.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_placefile()

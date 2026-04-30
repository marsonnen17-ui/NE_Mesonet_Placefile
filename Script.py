import requests
import os

# Configuration
URL = "https://mesonet.agron.iastate.edu/api/1/currents.json?network=NE_DCP"
OUTPUT_FILE = "NE_Mesonet.txt"

def create_placefile():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json().get('data', [])

        with open(OUTPUT_FILE, "w") as f:
            # --- PLACEFILE HEADER ---
            f.write("Refresh: 5\n")
            f.write("Threshold: 999\n")
            f.write("Title: NE Mesonet (Wind Barbs)\n")
            
            # Fix: Define BOTH Font 1 and Font 0 to prevent the GR2 error
            f.write("Font: 1, 12, 1, \"Arial\"\n")
            f.write("Font: 0, 12, 1, \"Arial\"\n")
            
            # IconFile: fileNumber, width, height, hotX, hotY, "URL"
            f.write("IconFile: 1, 32, 32, 16, 16, \"https://raw.githubusercontent.com/pbrady/Placefiles/master/wind_barbs.png\"\n\n")

            for station in data:
                lat, lon = station.get('lat'), station.get('lon')
                stid = station.get('station')
                temp = station.get('tmpf')
                wind_kts = station.get('sknt')
                wind_dir = station.get('drct')

                if any(v is None for v in [lat, lon, temp, wind_kts, wind_dir]):
                    continue

                # --- Wind Barb Calculation --- Potentially remove
                icon_index = int(round(wind_kts / 5.0))
                if icon_index > 25: icon_index = 25
                if icon_index < 0: icon_index = 0
                
                wind_mph = round(wind_kts * 1.15, 1)

                # --- Write Station Object ---
                f.write(f"Object: {lat}, {lon}\n")
                f.write(f"  Threshold: 999\n")
                f.write(f"  Color: 255 255 255\n")
                
                # Text: x-offset, y-offset, fontNumber, "string"
                f.write(f"  Text: -12, -12, 1, \"{int(temp)}\"\n")
                
                # FIXED ICON LINE: 
                # Icon: x, y, angle, fileNumber, iconNumber, "hover"
                # (Previous code had icon_index and fileNumber swapped)
                f.write(f"  Icon: 0, 0, {int(wind_dir)}, 1, {icon_index}, \"{stid}: {temp}F, {wind_mph}mph\"\n")
                f.write("End:\n\n")
                
        print(f"Successfully updated {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_placefile()

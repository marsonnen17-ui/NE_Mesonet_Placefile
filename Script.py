import requests
import os

# Configuration
URL = "https://mesonet.agron.iastate.edu/api/1/currents.json?network=NE_DCP"
OUTPUT_FILE = "NE_Mesonet_V1.txt"

def create_placefile():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json().get('data', [])

        with open(OUTPUT_FILE, "w") as f:
            # --- STRICT PLACEFILE HEADER ORDER ---
            f.write("Title: NE Mesonet (Wind Barbs)\n")
            f.write("Refresh: 5\n")
            f.write("Threshold: 999\n")
            
            # 1. Define IconFile FIRST (file ID, width, height, hotX, hotY, URL)
            # Using index 1 and a standard wind barb URL
            f.write("IconFile: 1, 32, 32, 16, 16, \"https://github.com/marsonnen17-ui/Mesonet_Test/blob/main/WindBarb.jpg\"\n")
            
            # 2. Define Font SECOND
            f.write("Font: 1, 12, 1, \"Arial\"\n")
            f.write("Font: 0, 12, 1, \"Arial\"\n\n")

            for station in data:
                lat, lon = station.get('lat'), station.get('lon')
                stid = station.get('station')
                temp = station.get('tmpf')
                wind_kts = station.get('sknt', 0)
                wind_dir = station.get('drct', 0)

                # Skip if basic location data is missing
                if any(v is None for v in [lat, lon, temp]):
                    continue

                # --- Wind Barb Calculation ---
                # Ensure values are integers and within range
                wind_kts = float(wind_kts) if wind_kts else 0
                icon_index = int(round(wind_kts / 5.0))
                #if icon_index > 25: icon_index = 25
                if icon_index < 0: icon_index = 0
                
                wind_mph = round(wind_kts * 1.15, 1)

                # --- Station Object ---
                # Use no spaces in the coordinates to ensure old parsers don't fail
                f.write(f"Object: {lat},{lon}\n")
                f.write("  Threshold: 999\n")
                f.write("  Color: 255 255 255\n")
                
                # Text: offset-x, offset-y, fontNumber, "string"
                f.write(f"  Text: -12, -12, 1, \"{int(temp)}\"\n")
                
                # Icon: offset-x, offset-y, angle, fileNumber, iconNumber, "hover"
                # This line refers to IconFile 1 defined above
                f.write(f"  Icon: 0, 0, {int(wind_dir)}, 1, {icon_index}, \"{stid}: {temp}F, {wind_mph}mph\"\n")
                f.write("End:\n\n")
                
        print(f"Update successful. Placefile saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_placefile()

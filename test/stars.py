# process_bsc_data_json.py
import json
import os

# --- Configuration ---
# Name of the file where you saved the JSON array data (just the [...])
BSC_DATA_FILENAME = 'starData.json' # Using .json extension now

# Define the magnitude limit for stars (inclusive, e.g., <= 4.0 means magnitudes 4.0 and brighter)
MAGNITUDE_LIMIT = 4.0 

# Use 4.0 to include stars up to magnitude 4

# Define the output JSON filename
OUTPUT_FILENAME = 'bright_stars_bsc_filtered.json'
# ----------------------

# --- Helper functions for coordinate conversion ---
# (These remain the same as the input fields are RAh, RAm, etc.)
def hms_to_degrees(ra_h, ra_m, ra_s):
    """Converts Right Ascension from Hours, Minutes, Seconds to Degrees."""
    try:
        h = float(ra_h)
        m = float(ra_m)
        s = float(ra_s)
        # Convert to total hours, then to degrees (1 hour = 15 degrees)
        total_hours = h + m/60.0 + s/3600.0
        return total_hours * 15.0
    except (ValueError, TypeError): # Added TypeError as values might be None
        return None # Return None if conversion fails

def dms_to_degrees(dec_sign, dec_d, dec_m, dec_s):
    """Converts Declination from Sign, Degrees, Minutes, Seconds to Degrees."""
    try:
        d = float(dec_d)
        m = float(dec_m)
        s = float(dec_s)
        # Convert to total degrees
        total_degrees = d + m/60.0 + s/3600.0
        if dec_sign == '-':
            return -total_degrees
        elif dec_sign == '+':
            return total_degrees
        else:
            return None # Return None if sign is invalid or not '+' or '-'
    except (ValueError, TypeError): # Added TypeError
         return None # Return None if conversion fails

# --- Main Script ---
print(f"Reading data from '{BSC_DATA_FILENAME}'...")
if not os.path.exists(BSC_DATA_FILENAME):
    print(f"Error: Data file not found at '{BSC_DATA_FILENAME}'.")
    print(f"Please copy ONLY the array content ([...]) from the URL into '{BSC_DATA_FILENAME}'.")
    exit()

try:
    with open(BSC_DATA_FILENAME, 'r') as f:
        # Use json.load to parse the file directly as JSON
        bsc_catalog_data = json.load(f)

except FileNotFoundError:
     print(f"Error: '{BSC_DATA_FILENAME}' not found.")
     exit()
except json.JSONDecodeError as e:
     print(f"Error decoding JSON from '{BSC_DATA_FILENAME}': {e}")
     print("Please ensure the file contains only a valid JSON array ([...]).")
     exit()
except Exception as e:
     print(f"An unexpected error occurred while reading '{BSC_DATA_FILENAME}': {e}")
     exit()


if not isinstance(bsc_catalog_data, list):
     print(f"Error: Expected data to be a JSON array [...], but got {type(bsc_catalog_data)}.")
     print(f"Please ensure the file contains ONLY the array content ([...]).")
     exit()


print(f"Loaded {len(bsc_catalog_data)} entries from the file.")

# --- Filter and Process Stars ---
star_data_list = []
processed_entries = 0
skipped_count = 0

print(f"Processing and filtering for stars with Vmag <= {MAGNITUDE_LIMIT}...")

for entry in bsc_catalog_data:
    processed_entries += 1
    # Ensure the entry is a dictionary
    if not isinstance(entry, dict):
        # print(f"Skipping entry {processed_entries}: Not a dictionary ({type(entry)}).")
        skipped_count += 1
        continue

    # --- Extract and Convert Data ---
    # Get Magnitude (Vmag) - need to handle potential missing or non-numeric values
    # Use .get() with a default of None for safety
    vmag_str = entry.get('Vmag', None)
    if vmag_str is None or vmag_str == '': # Also check for empty string
        # print(f"Skipping entry {processed_entries}: Missing or empty 'Vmag'.")
        skipped_count += 1
        continue
    try:
        magnitude = float(vmag_str)
    except ValueError:
        # print(f"Skipping entry {processed_entries}: Non-numeric 'Vmag' ('{vmag_str}').")
        skipped_count += 1
        continue

    # Filter by Magnitude
    if magnitude > MAGNITUDE_LIMIT:
        # print(f"Skipping entry {processed_entries}: Vmag ({magnitude}) > {MAGNITUDE_LIMIT}.")
        skipped_count += 1
        continue

    # Get RA (RAh, RAm, RAs) - need to handle missing or non-numeric values
    rah_str = entry.get('RAh')
    ram_str = entry.get('RAm')
    ras_str = entry.get('RAs')
    # Check if any part is None or an empty string
    if any(val is None or val == '' for val in [rah_str, ram_str, ras_str]):
         # print(f"Skipping entry {processed_entries}: Missing RA (H, M, S) keys or empty values.")
         skipped_count += 1
         continue
    ra_degrees = hms_to_degrees(rah_str, ram_str, ras_str)
    if ra_degrees is None: # hms_to_degrees returns None on failure
         # print(f"Skipping entry {processed_entries}: Invalid RA (H, M, S) values ('{rah_str}h {ram_str}m {ras_str}s').")
         skipped_count += 1
         continue

    # Get Dec (DE-, DEd, DEm, DEs) - need to handle missing or non-numeric values
    dec_sign_str = entry.get('DE-')
    ded_str = entry.get('DEd')
    dem_str = entry.get('DEm')
    des_str = entry.get('DEs')
     # Check if any part is None or an empty string
    if any(val is None or val == '' for val in [dec_sign_str, ded_str, dem_str, des_str]):
         # print(f"Skipping entry {processed_entries}: Missing Dec (Sign, D, M, S) keys or empty values.")
         skipped_count += 1
         continue
    dec_degrees = dms_to_degrees(dec_sign_str, ded_str, dem_str, des_str)
    if dec_degrees is None: # dms_to_degrees returns None on failure
         # print(f"Skipping entry {processed_entries}: Invalid Dec (Sign, D, M, S) values ('{dec_sign_str}{ded_str}d {dem_str}m {des_str}s').")
         skipped_count += 1
         continue

    # Get a Name/Identifier - Try HR, then DM, otherwise use a generic name
    star_name = 'Unnamed Star' # Default
    hr_id = entry.get('HR')
    dm_id = entry.get('DM')

    # Check if HR exists and is not None, empty, or just whitespace
    if hr_id is not None and str(hr_id).strip():
        star_name = f"HR {hr_id}".strip()
    # Else, check if DM exists and is not None, empty, or just whitespace
    elif dm_id is not None and str(dm_id).strip():
         star_name = str(dm_id).strip()
    # Could add more fallbacks like SAO or use an index f"Star {processed_entries}"

    # Append the processed star data
    star_data_list.append({
        'name': star_name,
        'ra': ra_degrees,
        'dec': dec_degrees,
        'mag': magnitude
    })

print(f"Successfully processed {len(star_data_list)} stars.")
if skipped_count > 0:
    print(f"Skipped {skipped_count} entries due to missing data or invalid values.")


# --- Save the data to a JSON file ---
try:
    with open(OUTPUT_FILENAME, 'w') as f:
        # Use json.dump to write the list of dictionaries to the file
        json.dump(star_data_list, f, indent=2)

    print(f"\nSuccessfully wrote filtered star data to {OUTPUT_FILENAME}")
    print("\n--- Next Steps ---")
    print(f"1. Open the '{OUTPUT_FILENAME}' file ('{OUTPUT_FILENAME}').")
    print("2. Copy the entire content (including the square brackets `[]`).")
    print("3. Paste this content into the `STAR_DATA` constant in your `bg.js` file,")
    print("   replacing the existing small sample data.")
    print("4. The JavaScript projection logic expects RA/Dec in degrees (which this script provides).")


except Exception as e:
    print(f"Error writing JSON output to '{OUTPUT_FILENAME}': {e}")
# This python program works on MY picture directory tree, if you are interested.
# If you aren't familiar with Python, please use gatergps.html instead.
#
# This script gathers metadata for all images with GPS coordinates in them
# and puts the metadta in gpstagged.js, which gps.html loads to get all the picture metadata.
#
# It assumes the photos are organized the way I keep them organized on
# my computer, with a file "imagedata.cached" in each directory with the metadata already
# extracted into it (using jhead), and a subdirecory "_small" with thumbnails for the
# images from that directory.
#
# AI generated, Feb 2026

import os
import re

OUTPUT_FILE = "gpstagged.js"
ROOT_DIR = "."            

# Regex patterns
re_filename = re.compile(r"^File name\s*:\s*(.+)$", re.M)
re_datetime = re.compile(r"^Date/Time\s*:\s*(.+)$", re.M)
re_cameramodel = re.compile(r"^Camera model\s*:\s*(.+)$", re.M)
re_lat = re.compile(r"^GPS Latitude\s*:\s*([NS])\s*(\d+)d\s*(\d+)m\s*([\d.]+)s$", re.M)
re_lon = re.compile(r"^GPS Longitude\s*:\s*([EW])\s*(\d+)d\s*(\d+)m\s*([\d.]+)s$", re.M)

def dms_to_decimal(sign, deg, minutes, seconds):
    value = float(deg) + float(minutes) / 60.0 + float(seconds) / 3600.0
    if sign in ("S", "W"):
        value = -value
    return value

# Start the Javascript structure
print("Gathering GPS data to file:",OUTPUT_FILE)
outfile = open(OUTPUT_FILE, "w", encoding="utf-8")
print("thumbnailSubdir = '_small/'",file=outfile)
print("const rawImageData = `",file=outfile)

for root, dirs, files in os.walk(ROOT_DIR):
    # Logic to skip directories < 2011 at the first level
    if root == ROOT_DIR:
        # We only filter the 'dirs' list in place to prevent os.walk from entering them
        original_dirs = list(dirs)
        for d in original_dirs:
            # Check if directory starts with a number
            match = re.match(r"^(\d+)", d)
            if match:
                year = int(match.group(1))
                if year < 2011:
                    dirs.remove(d) # This stops os.walk from descending into this branch

    if "imagedata.cached" not in files:
        continue
    
    cache_path = os.path.join(root, "imagedata.cached")

    with open(cache_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    entries = re.split(r"\n\s*\n", content)

    for entry in entries:
        m_file = re_filename.search(entry)
        m_time = re_datetime.search(entry)
        m_model = re_cameramodel.search(entry)
        m_lat = re_lat.search(entry)
        m_lon = re_lon.search(entry)

        if not (m_file and m_time and m_lat and m_lon):
            continue

        lat = dms_to_decimal(*m_lat.groups())
        lon = dms_to_decimal(*m_lon.groups())

        if lat == 0.0 and lon == 0.0:
            continue

        base_filename = os.path.basename(m_file.group(1))
        try:
            camera_model = m_model.group(1)
        except:
            camera_model = "????"
            
        full_path = os.path.join(root, base_filename)
        full_path = full_path.replace("\\","/")
        if full_path.startswith("./"): full_path = full_path[2:]

        # Output in the format the HTML script expects
        print(f"{full_path}",file=outfile)
        print(f"Date/Time: {m_time.group(1)}",file=outfile)
        print(f"GPS: {lat:.7f},{lon:.7f}",file=outfile)
        print(f"Camera: {camera_model}\n",file=outfile)

# Close the Javascript string
print("`;",file=outfile)
outfile.close()
print("Done")
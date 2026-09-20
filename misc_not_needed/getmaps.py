# I used this script to grab some off-line basemaps to use for my gps browser.
# I recommend you don't use this, as I have since added the ability to use basemaps directly from the internet.
#
# Script to grab client area of google chrome on google maps.
# Start google crome in debug mode, then navigate to maps to capture, and run this script to grab a screenshot.
# cut off all the legend stuff, and save it with coordinates in a file.
# Post process PNG files with "mogrify -evaluate subtract 50% *.png" to make them darker
# Then to make them smaller:
# mogrify -colors 32 -quality 100 -format webp  *.png

# Must start google chrome with
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
import asyncio
import re
import io
from playwright.async_api import async_playwright
from PIL import Image

def sanitize_filename(url):
    # Strip protocol and illegal characters
    clean = re.sub(r'^https?://', '', url)
    print("cleaned URL:",clean)
    clean = re.sub(r'www.google.com/maps/', '', clean) # Remove URL prefix.
    print("cleaned URL subed:",clean)
    clean = clean.split("?")[0]
    clean = clean.split("/")[0]
    print("Truncated:",clean)
    clean = "basemap"+clean
    print("cleaned URL chars:",clean)
    return f"{clean[:100]}"

async def capture_chrome():
    async with async_playwright() as p:
        try:
            # Connect to the Chrome with debug instance.
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        except:
            print("Failed to connect to chrome browser in debug mode")
            print('run Chrome with: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"')
            return
        
        # Access the currently active context and page
        context = browser.contexts[0]
        page = context.pages[0] # This grabs the first open tab
        
        url = page.url
        filename = sanitize_filename(url)

        device_pixel_ratio = await page.evaluate("window.devicePixelRatio")
        #print(f"Current Display Scaling: {device_pixel_ratio}x")

        # Do the cropping from this script.
        img_bytes = await page.screenshot(type="png", full_page=False)
        
        # Load the bytes into Pillow (Image Processing) ---
        # We use io.BytesIO to treat the byte array like a file.
        original_image = Image.open(io.BytesIO(img_bytes))
        
        # Trim the google maps legend off the top and bottom of the caputred client area
        width, height = original_image.size
        page_trim = int(174*device_pixel_ratio)
        crop_box = (0,page_trim,width,height-page_trim)
        cropped_image = original_image.crop(crop_box)
        
        if 'z' in filename:
            filetype = ".png" # its a map
        else:
            filetype = ".jpg" # its an aerial photo (google sattelite)
        
        # Add dimensions and screen zoom factor to the filename
        final_w, final_h = cropped_image.size
        filename = filename+f" {final_w}x{final_h}x{device_pixel_ratio}"+filetype
        
        # Save it
        cropped_image.save("maps/"+filename)            
                
        print(f"Captured: {url}")
        print(f"Saved as: {filename}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_chrome())
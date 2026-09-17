<html>
<body>
<h1>An HTML / Javascript program for browsing large sets of GPS tagged images from phones, on a map.</h1>

There is also a video about this: <a href="https://youtu.be/xxxxxxxxxxx">https://youtu.be/xxxxxxxxxxx</a>
<p>
I like how phones can show heatmaps of where photos were taken on a map, but my photo collection on my PC encompasses photos from many devices.  I wanted to be able to browse photos by location on my PC, so I created this program.
I started by challenging AI (Google Gemini) to write such a program.  Over several months I have refined it and added features, mostly by requesting specific changes to the code and inspecting and tweaking the resulting code.
<p>
The program is intended to be run locally on your computer, all you need is the "gps.html" and "gathergps.html" files and place them into the root directory of your photo collection.
<p>
Scanning  thousands of files every time gps.html is opened would take very long.  Instead gps.html loads a file 'gpstagged.js' containing pre-gathered metadata for all images.  This file is created by 'gathergps.html'.  Due to various security limitations of html / javascript, gathergps.html needs you to browse to the root of your image tree.  After gathering all the metadata, it will create 'gpstagged.js" in your downloads folder.  You must then move this file to the root images directory, same directory as gps.html
<p>
For my own photo collection of 160,000 photos, only 10% have GPS coordinates, and I use a script "gathergps.py", but this python script assumes the files are organized the way they are on my computer.
<p>
<b>Typical view of GPSpix</b><br>
<img src="pix/view1.webp">
<br>
The large light blue circle on this view represents several thousand images at the family camp.
Unfortunately phones will often use a guess for the Latitude / Longitude coordinates if they don't have a GPS fix when a photo was taken.  This guess is often based on the current cell tower and cell sector that the phone is connected to.  This guess can be several kilometers off.  The circles towards the top left on the above map are mostly guesses.
In my experience iPhones are much less likely to just use a guess for Lat/Lon.
<p>
If you are taking photos and want to make sure they have proper coordinates, you can go into maps beforehand to make sure the phone gets a fix, as it will try harder to get a fix while in maps.  Or you can tell the phone to navigate to somewhere, at which point it will do its best to maintain a GPS fix even with maps in the background.
<p>
Images can be selected by clicking on them with a mouse.  Pan and zoom are done by dragging the map or rolling the mouse wheel.  You can also pinch in and out on mobile.
<p>
Images can be selected by clicking on them.  Large clusters of images will resolve into smaller clusters and eventually individual images as you zoom in on them.
<p>
At the top left of the map view is a scale bar indicating the map scale, plus a button to pop up the same map view on Google maps, though without the dots for image locations.
<p>
<b>Zoomed in on just a few days</b><br>
<img src="pix/time-zoomed.webp">
<br>
Below the scale bar is a time-scale and histogram of when images were taken.  You can drag the green sliders on the time scale to limit the images shown to a certain time range.  You can also zoom in on the time scale between the markers using the "time zoom in" button.  By successively zooming in, you can zoom the time scale to just a few days.
<br>
If an image is selected, a red mark is shown on the time scale indicating when the image was taken in addition to the red dot on the map.  You can also click on the time scale to select the image taken closest in time to where you clicked on the time scale.  You can also drag left and right on the time-scale to scrub through images time-wise.  The cursor left and right keys will also change the selection to the previous or next image time-wise.
<p>
<b>Zoomed in on just a few meters in a high geographic photo density area</b><br>
<img src="pix/scale-zoomed.webp">
<br>
This is zoomed in on the area of our house.  Due to coordinate rounding, many images may fall on the exact same Lat/Lon coordinates.  To allow selecting individual images, some "jitter" is added to the X Y coordinate of the image dot so that they appear as a circular cluster or spiral of dots.  Note that the Lat/Lon of selected images is not altered, only where the dot for the image is shown on the screen.
<p>
<b>If you want to edit the program</b>
I wrote the file 'what it does.txt' to help AI understand what the program is about when I have it re-ingest the code. 
<p>
I also used a free API key from <a href="https://carto.com/basemaps">carto.com/basemaps</a> for the openstreetmaps base maps.  If you modify the code, plan on using it a lot, or re-publish it, please get your own free carto.com API key so you don't end up with watermarks on your base maps from API key overuse.


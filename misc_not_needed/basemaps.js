// Javascript file I use to handle locally stored base maps,
// which must be captured from google maps and stored in the locabasemaps directory separately.
// This is complicated to do, so I don't expect anybody else to use this functionality.
// Put into subdirectory 'localbasemaps'
// Also need to include basemaplist.txt from gps.html to define the list of base maps
//
// basemaplst.txt looks like this:
// const BasemapsDir = `
//     basemap@43.4470922,-80.5010094,13.5z 2245x1724x1.webp
//     basemap@43.5494233,-79.9045283,11z 2245x1724x1.webp
//  .....
// ';

const baseMap_CapturedLocal = {
// Object for drawing selected base local basemap images captured from google maps
    maps: [],

    init() {
        if (typeof BasemapsDir === 'undefined') return;

        const lines = BasemapsDir.trim().split(/\r?\n/);
        lines.forEach(line => {
            // Regex captures: 1:fileName, 2:lat, 3:lon, 4:zoomVal, 5:unit(z/m), 6:width, 7:height
            const match = line.match(/(basemap@([\d.-]+),([\d.-]+),([\d.]+)([mz])\s+(\d+)x(\d+)x(\d+(?:\.\d+)?))\.(?:png|jpe?g|webp)/);

            let fudgeFactor = 1.0
            const ffi = line.indexOf("ff=");
            if (ffi > 0){
                fudgeFactor = parseFloat(line.slice(ffi+3));
                line = line.slice(0,ffi)
            }

            if (match) {
                const fileName = line.trim()
                const lat = parseFloat(match[2]);
                const lon = parseFloat(match[3]);
                const val = parseFloat(match[4]);
                const unit = match[5];
                const imgW = parseInt(match[6]);
                const imgH = parseInt(match[7]);
                const imgScale = parseFloat(match[8]);

                let latH;
                if (unit === 'z') {
                    // Geographic height of the image in degrees:
                    // (180 degrees * image pixel height) / (256 * 2^zoom)
                    latH = (180 * imgH) / (256 * Math.pow(2, val));
                    latH = latH * 1.39/imgScale; // Scale fudge factor.
                } else {
                    // Meter-based: vertical ground distance / meters per degree
                    latH = val / 111120 * 0.72 * fudgeFactor;
                }

                // Geographic width in degrees (accounting for image aspect ratio)
                const lonW = latH * (imgW / imgH) / Math.cos(lat/180*3.14159);

                const entry = {
                    fileName: fileName,
                    fullPath: "localbasemaps/" + fileName,
                    img: new Image(),
                    lat, lon,
                    latH,
                    minLat: lat - (latH / 2),
                    maxLat: lat + (latH / 2),
                    minLon: lon - (lonW / 2),
                    maxLon: lon + (lonW / 2)
                };

                // Set the source so the browser can load it when needed
                //entry.img.src = entry.fullPath; // don't set src so it won't load yet.
                this.maps.push(entry);

                // Print the extents to the console
                console.log(`Basemap Loaded: ${entry.fileName}  ${imgW}x${imgH}`);
                console.log(`  Lat,Lon: ${entry.minLat.toFixed(6)} to ${entry.maxLat.toFixed(6)},  ${entry.minLon.toFixed(6)} to ${entry.maxLon.toFixed(6)}`);
            }else{
                console.log("no match:" , line)
            }
        });
    },

    // Filter basemaps by what overlaps the view port.
    draw() {
        // Current view bounds
        const b1 = xy2latLon(0, 0);
        const b2 = xy2latLon(canvas.width, canvas.height);
        const viewMinLat = b2.lat;
        const viewMaxLat = b1.lat;
        const viewMinLon = b1.lon;
        const viewMaxLon = b2.lon;
        const viewHeight = viewMaxLat - viewMinLat;

        // 1. Filter for overlap
        let visible = this.maps.filter(m => {
            return !(m.minLat > viewMaxLat || m.maxLat < viewMinLat ||
                     m.minLon > viewMaxLon || m.maxLon < viewMinLon);
        });

        // 2. Sort by latitude extent (largest to smallest)
        visible.sort((a, b) => b.latH - a.latH);

        let finalSet = [];

        for (let m of visible) {
            // if an image covers less than 10% of view height, skip if we have larger ones
            if (finalSet.length > 0 && m.latH < (viewHeight * 0.2)) continue;

            // If this image completely covers the viewport, don't draw bigger ones behind it
            if (m.minLat <= viewMinLat && m.maxLat >= viewMaxLat &&
                m.minLon <= viewMinLon && m.maxLon >= viewMaxLon) {
                finalSet = []; // Clear set to discard larger ones behind this one.
            }
            finalSet.push(m);

        }

        if (finalSet.length === 0) return;

        ctx.save();

        finalSet.forEach(m => {
            // Trigger loading image on demand
            if (!m.srcSet) {

                m.img.addEventListener('load', () => {
                    console.log(`Finished loading: ${m.fileName}`);
                    draw(); // Force a redraw now that the pixels are ready
                }, { once: true }); // Use {once: true} to auto-cleanup the listener

                m.img.src = m.fullPath;
                m.srcSet = true;
                console.log(`Lazy loading: ${m.fileName}`);
            }

            const topLeft = latLon2xy(m.maxLat, m.minLon);
            const bottomRight = latLon2xy(m.minLat, m.maxLon);

            const w = bottomRight.x - topLeft.x;
            const h = bottomRight.y - topLeft.y;

            ctx.drawImage(m.img, topLeft.x, topLeft.y, w, h);

            // Draw a rectangle around the map
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 0.5;
            ctx.strokeRect(topLeft.x, topLeft.y, w, h);
        });

        ctx.restore();
    }
};

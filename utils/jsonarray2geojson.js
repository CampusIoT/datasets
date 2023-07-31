/**
* This program generates a GeoJSON object from an array of entries containing latitude and longitude properties
* Author: Didier DONSEZ
*/

function usage() {
    console.log(process.argv[1] + " <option> <filename> [<color> [<symbol>]]");
    console.log("   -l for linestring");
    console.log("   -p for points");
    console.log("   -a for both");
}

const args = process.argv;
if (args.length < 4) {
    usage();
    process.exit(1);
}

const filename = process.argv[3];
const option = process.argv[2];
const color = (args.length >= 4) ? process.argv[4] : "#0432ff";
const symbol = (args.length >= 5) ? process.argv[5] : "circle"; // https://gis.stackexchange.com/questions/219241/list-of-available-marker-symbols


// console.log("Loading JSON ...");
var fs = require('fs');
var positions = JSON.parse(fs.readFileSync(filename, 'utf8'));

// remove duplicate positions
var count = {};
const _positions = [];
positions.forEach(function (position, index, array) {
    if (position.latitude && position.longitude) {
        const idx = position.latitude + "," + position.longitude;
        var v = count[idx];
        if(v) {
            count[idx] = v + 1;
        } else {
            count[idx] = 1;
            _positions.push(position);
        }
    } else if (position.lat && position.lon) {
        const idx = position.lat + "," + position.lon;
        var v = count[idx];
        if(v) {
            count[idx] = v + 1;
        } else {
            count[idx] = 1;
            _positions.push(position);
        }
    }
});

positions = _positions;

// console.info(JSON.stringify(positions,undefined,2));

// TODO add count

//const strokes = [ "#0432ff", "#ff2600", "#aa7941", "#00fcff",  "#00f900", "#ff40ff", "#ff9200", "#932092", "#ff2600", "#fefb00"];
const stroke_width = 2;


function getCoord(position) {

    var coord;
    if (position.latitude && position.longitude) {
        coord = [
            position.longitude,
            position.latitude
        ];
    } else if (position.lat && position.lon) {
        coord = [
            position.lon,
            position.lat
        ];
    } else if (position.lat && position.long) {
        coord = [
            position.long,
            position.lat
        ];
    } else if (position.lat && position.lng) {
        coord = [
            position.lng,
            position.lat
        ];
    }


    if(coord) {
        // add altitude in third position
        if(position.altitude) {
            coord.push(position.altitude);
        } else if(position.elevation) {
            coord.push(position.elevation);
        } else if(position.alt) {
            coord.push(position.alt);
        } else if(position.z) {
            coord.push(position.z);
        }
    }
    
    return coord;    
}

function getRssiColor(rssi) {

    var color = '#7d8182'; //  # default to grey

    if(rssi < 0 && rssi >= -70) {
        color = '#005a32'
    } else if(rssi < -70) {
        color = '#238443';
    } else  if (rssi < -90) {
        color = '#41ab5d';
    } else if (rssi < -100) {
        color = '#78c679';
    } else if (rssi < -110) {
        color = '#addd8e';
    } if (rssi < -115) {
        color = '#d9f0a3';
    }

    return color;
}


function point(position, marker_symbol, marker_size, marker_color) {
    var f;

    var coord = getCoord(position);

    if(coord) {
        var f = {
            "type": "Feature",
            "properties": {

                // TODO set color according RSSI, SNR, ESP (for coverage map)
                "marker-color": position.color ? position.color : marker_color,
                "marker-size": marker_size,
                "marker-symbol": position.symbol ? position.symbol : marker_symbol,

                geocode: position.geocode ? position.geocode : undefined,
                hashcode: position.hashcode ? position.hashcode : undefined,

                altitude: position.altitude ? Number((position.altitude).toFixed(0)) : undefined,
                alt: position.alt ? Number((position.alt).toFixed(0)) : undefined,
                elevation: position.elevation ? Number((position.elevation).toFixed(0)) : undefined,
                z: position.z ? Number((position.z).toFixed(0)) : undefined,

                speed: position.speed ? position.speed : undefined,
                hspeed: position.hspeed ? position.hspeed : undefined,
                vspeed: position.vspeed ? position.vspeed : undefined,
                gtw_id: position.gtw_id ? position.gtw_id : undefined,
                gweui: position.gweui ? position.gweui : undefined,

                gmap: position.gmap ? position.gmap : undefined,
                osm: position.osm ? position.osm : undefined,

                date: position.date ? position.date : undefined,
                date_utc: position.date_utc ? position.date_utc : undefined,
                timestamp: position.timestamp ? position.timestamp : undefined,
                
                temperature: position.temperature ? position.temperature : undefined,
                pressure: position.pressure ? position.pressure : undefined,
                humidity: position.humidity ? position.humidity : undefined,
                
                snr: position.snr ? position.snr : undefined,
                lsnr: position.lsnr ? position.lsnr : undefined,
                esp: position.esp ? position.esp : undefined,
                rssi: position.rssi ? position.rssi : undefined,
                count: position.count ? position.count : undefined,
                cnt: position.cnt ? position.cnt : undefined,
                fcnt: position.fcnt ? position.fcnt : undefined,
                fCnt: position.fCnt ? position.fCnt : undefined,
                per: position.per ? position.per : undefined,
                lost_frames: position.lost_frames ? position.lost_frames : undefined,
                
                operator: position.operator ? position.operator : undefined,
                name: position.name ? position.name : undefined,
                place: position.place ? position.place : undefined,
                gwid: position.gwid ? position.gwid : undefined,
                gweui: position.gweui ? position.gweui : undefined,
                eui: position.eui ? position.eui : undefined,
                devaddr: position.devaddr ? position.devaddr : undefined,
                deveui: position.deveui ? position.deveui : undefined,
                dev_eui: position.dev_eui ? position.dev_eui : undefined,
                distance_los: position.distance_los ? position.distance_los : undefined,
                distance: position.distance ? position.distance : undefined
            },
            "geometry": {
                "type": "Point",
                "coordinates": coord
            }
        };

    }
    return f;
}

function linestring(positions, stroke, stroke_width, stroke_opacity) {
    var coordinates = [];
    positions.forEach(function (p, index, array) {
        const coord = getCoord(p);
        if(coord) {
            coordinates.push(coord);
        }
    });
    var feature = {
        type: "Feature",
        properties: {
            stroke: stroke,
            "stroke-width": stroke_width,
            "stroke-opacity": stroke_opacity,
            filename: filename
        },
        geometry: {
            type: "LineString",
            coordinates: coordinates
        }
    };
    return feature;
}

function generateGeojson(positions) {

    var features = [];
    var stroke = color;

    if (option === '-p' || option === '-a') {
        // add points
        const marker_symbol = symbol;
        const marker_color = stroke;
        const marker_size = "small";
        positions.forEach(function (p, index, array) {
            var pt = point(p, marker_symbol, marker_size, marker_color);
            if (pt) { features.push(pt); }
        });
    }

    if (option === '-l' || option === '-a') {
        // add LineString
        features.push(linestring(positions, stroke, 2, 1));
    }

    if (option === '-l' || option === '-a') {
        var first = point(positions[0], "embassy", "medium", "#00f900");
        if (first) { features.push(first); }
        var last = point(positions[positions.length - 1], "embassy", "medium", "#ff2600");
        if (last) { features.push(last); }
    }

    var geojson = {
        type: "FeatureCollection",
        features: features
    };

    console.log(JSON.stringify(geojson));
};

generateGeojson(positions);

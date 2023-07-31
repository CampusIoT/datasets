nvm use stable

LOGDIR='/Users/donsez/github/campusiot/datasets/Helium/'
toGeoJSON(){
    FILE=$1
    gunzip -c $FILE.ndjson.gz | jq -c '._devLocation' | grep -v null | sort -u | jq  -s '.' > $FILE.json
    node ../utils/jsonarray2geojson.js -p $FILE.json green > $FILE.endpoints.geojson
    rm $FILE.json
    gunzip -c $FILE.ndjson.gz | jq -c '.hotspots|first(.[])|{latitude:.lat,longitude:.long,name:.name}' | grep -v null | sort -u | jq  -s '.' > $FILE.json
    node ../utils/jsonarray2geojson.js -p $FILE.json red > $FILE.hotspots.geojson
    rm $FILE.json
    python ../utils/merge_geojson.py $FILE.hotspots.geojson $FILE.endpoints.geojson $FILE.all.geojson
}

FILE=$LOGDIR/FTD_0018B20000020
toGeoJSON $FILE

FILE=$LOGDIR/EMS_A81758FFFE04B1C1
toGeoJSON $FILE

FILE=$LOGDIR/IMST_33323431007C727B
toGeoJSON $FILE

FILE=$LOGDIR/POC_6081F9835853819F
toGeoJSON $FILE

 
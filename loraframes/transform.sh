#!/bin/sh

nvm use stable

DIR=~/mqtt_logs

FILE=msg-20240707

NODE_OPTIONS='--max-old-space-size=20000'

transform() {
  LOGFILE=$1
  gunzip -c $LOGFILE.log.gz \
    | grep -a '/up' \
    | node $NODE_OPTIONS streamLines.js - --s/log2json \
    --s/convertHex --s/addEsp \
    --s/addLoraPacket \
    --s/h/save "$LOGFILE.ndjson" \
    --s/h/emptyoutput
}


transform $DIR/$FILE

gunzip -c $DIR/$FILE.ndjson.gz | \
jq -c '. | {modulation:.txInfo.modulation,codeRate:.txInfo.loRaModulationInfo.codeRate,frequency:.txInfo.frequency,_datarate:.txInfo._datarate,rssi:.rxInfo.rssi,loRaSNR:.rxInfo.loRaSNR,_esp:.rxInfo._esp,crcStatus:.rxInfo.crcStatus,gatewayID:.rxInfo.gatewayID,_packet:._packet,_timestamp:._timestamp,_date:._date}' \
  > $DIR/$FILE-lite.ndjson

| jq . | more

gzip $DIR/$FILE-lite.ndjson

gunzip -c $DIR/$FILE-lite.ndjson.gz | grep BAD_CRC | wc -l
gunzip -c $DIR/$FILE-lite.ndjson.gz | grep CRC_OK | wc -l
gunzip -c $DIR/$FILE-lite.ndjson.gz | grep _packet | wc -l
gunzip -c $DIR/$FILE-lite.ndjson.gz | grep "Data Up" | gzip -c > $DIR/$FILE-lite-dataup.ndjson.gz
gunzip -c $DIR/$FILE-lite.ndjson.gz | grep "Join" | gzip -c > $DIR/$FILE-lite-join.ndjson.gz

gunzip -c $DIR/$FILE-lite-dataup.ndjson.gz | json2csv --ndjson --flatten-objects > $DIR/$FILE-lite-dataup.csv
gunzip -c $DIR/$FILE-lite-join.ndjson.gz | json2csv --ndjson --flatten-objects > $DIR/$FILE-lite-join.csv

#!/bin/bash

 # Author: Didier DONSEZ, Université Grenoble Alpes

# Parameter 1 : name of a CVS file containing credential for forging and sending PoC LoRaWAN messages

# GWEUI    : the Id of the gateway which sent the forged LoRaWAN frame)
# NAME     : the name of POC endpoint (useful for reading the log)
# DEVADDR  : the DevAddr of POC endpoint registered in ABP on the Chirpstack LNS
# APPSKEY  : the AppSKey of POC endpoint (used for cyphering the payload of LoRaWAN frame)
# NWKSKEY  : the NwkSKey of POC endpoint (used for signing the LoRaWAN frame)
# COMMENT  : a useful comment (description of the gateway's location)

# The uplink frame counter (`fCntUp`) is saved in a file mamed `<devaddr>.fcnt`

# Usage  : ./proof.sh <gateways.csv> <sf> <list of txpower> <txpower> <list of sf> >> proof.log 2>&1
# Example: ./proof.sh gateways_for_campusiot.csv 7 "2 5 8 11" 14 "7 8 9 10 11 12" >> proof.log 2>&1



GATEWAYS=$1

MQTT_BROKER=_MY.MQTT.BROKER_
MQTT_USERNAME=_MY_MQTT_USERNAME_
MQTT_PASSWORD=_MY_MQTT_PASSWORD_

# Frequencies for EU863-870
# See LaRaWAN regional parameters document for adapting the PoC script to your country
declare -a FREQPLAN=(867100000 867300000 867500000 867700000 867900000 868100000 868300000 868500000)

randArrayElement(){ arr=("${!1}"); echo ${arr["$[RANDOM % ${#arr[@]}]"]}; }

# fPort
FPORT=10

# Sleep time between 2 massages
SLEEP=0.5

send_proof(){
        while IFS=";" read -r GWEUI NAME DEVADDR APPSKEY NWKSKEY COMMENT
        do

        token=$(( $RANDOM % 64000 + 1 ))

        # get the last uplink frame counter
        FCNT_FILE=${DEVADDR}.fcnt
        if [ ! -f "$FCNT_FILE" ]; then
        echo 0  > $FCNT_FILE
        fi
        FCNT=$(cat $FCNT_FILE)
        (( FCNT++ ))
	if [ $FCNT -ge "65535" ]; then FCNT=0 ; fi

        echo $FCNT  > $FCNT_FILE

        # save the current uplink frame counter
        FREQ=$(randArrayElement "FREQPLAN[@]")
        echo $FREQ

        echo "Sending POC ($DEVADDR) for $NAME ($GWEUI) @ SF$SF ${TXPOWER}dBm Freq=$FREQ FCnt=$FCNT Token=$token"

        MESSAGE=$(node build_proof_frame.js \
                $DEVADDR \
                $FCNT \
                $FPORT \
                $token \
                $APPSKEY \
                $NWKSKEY \
                $FREQ \
                $SF 125 \
                $TXPOWER \
                $GWEUI)
        mqtt publish -h $MQTT_BROKER -p 8883 -u $MQTT_USERNAME -P $MQTT_PASSWORD -l mqtts -t "gateway/$GWEUI/command/down" "$MESSAGE"

        sleep $SLEEP

        done < <(tail -n +2 $GATEWAYS)
}


# SF=7 TXPOWER in 2 5 8 11 14
SF=$2
for TXPOWER in $3
do
        send_proof
done

# SF in 7 8 9 10 11 12
TXPOWER=$4
for SF in $5
do
        send_proof
done

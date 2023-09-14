# Proof of Coverage (LoRaWAN) :: Scripts

Author: Didier DONSEZ

Script for forging and for sending PoC LoRaWAN frames (to their neighbours) by gateways.

The parameter 1 is the name of a CVS file containing credential for forging and sending PoC LoRaWAN messages

The columns of the CVS file are :
* `GWEUI`    : the Id of the gateway which sent the forged LoRaWAN frame)
* `NAME`     : the name of POC endpoint (useful for reading the log)
* `DEVADDR`  : the `DevAddr` of POC endpoint registered in ABP on the Chirpstack LNS
* `APPSKEY`  : the `AppSKey` of POC endpoint (used for cyphering the payload of LoRaWAN frame)
* `NWKSKEY`  : the `NwkSKey` of POC endpoint (used for signing the LoRaWAN frame)
* `COMMENT`  : a useful comment (description of the gateway's location)

The uplink frame counter (`fCntUp`) is saved in a file mamed `<devaddr>.fcnt`

This script can be run periodically between a `crontab` entry.

Usage  : `./proof.sh <gateways.csv> <sf> <list of txpower> <txpower> <list of sf> >> proof.log 2>&1`

Example: `./proof.sh gateways_for_campusiot.csv 7 "2 5 8 11" 14 "7 8 9 10 11 12" >> proof.log 2>&1`





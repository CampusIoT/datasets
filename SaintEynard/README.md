# The Saint Eynard LoRaWAN frames dataset

The directory contains the log files of 79382 frames sent by two LoRaWAN endpoints installed on the top of [Fort du Saint Eynard](https://fr.wikipedia.org/wiki/Fort_du_Saint-Eynard). The time range is from 2023-06-23 to 2024-09-16 (~15 months)

The exact location is [45.23513,5.7617](https://www.openstreetmap.org/search?query=45.23513%2C5.7617#map=19/45.23513/5.76170). The GPS altitude is 1350 meters.

Keywords: LoRaWAN, LPWAN, LoRa, Internet of Things, Sensor networks

## LoRaWAN Emitter

Two [Wyres Base board](https://github.com/CampusIoT/RIOT-wyres/blob/main/boards/wyres_base/README.md) :
* `WYRES_32_SAINTEYNARD_DOOR`: `DevEUI`=`d1d1e80000000032`, `DevAddr`=`fc00ac77` (indoor into a technical room) [9786 messages between 2023-06-23 and 2023-09-28](logs/d1d1e80000000032_campusiot.ndjson.gz), [10102 messages between 2023-09-28 and 2024-04-26](logs/d1d1e80000000032_campusiot-2.ndjson.gz).
* `WYRES_33_SAINTEYNARD_STATION`: `DevEUI`=`d1d1e80000000033`, `DevAddr`=`fc00af46` (outdoor, on the station mast (see the picture)) [14204 messages between 2023-06-23 and 2023-09-28](logs/d1d1e80000000033_campusiot.ndjson.gz), [45290 messages between 2023-09-28 and 2024-09-16](logs/d1d1e80000000033_campusiot-2.ndjson.gz).

## Dataset from CampusIoT

The endpoint's frames has been received by indoor and outdoor gateways installed in the Grenoble area by [LIG Lab](https://www.liglab.fr/). The LNS is [Chirpstack](https://www.chirpstack.io/) v3.


The log files are compressed [ndjson](http://ndjson.org/) files (aka one JSON object per line).

The fields prefixed by `_` are calculated and  added to the dataset sent by the LNS.

* `deviceName` : the name of the endpoint
* `devEUI` : the devEUI of the endpoint (hashed)
* `_date` : the archive date (human-readable string)
* `_timestamp` : the millisecond epoch of the archive time
* `data` : the hex-formatted frame payload (plain)
* `object` : the frame payload decoded using the endpoint decoder
* `_devLocation` : the static location of the endpoint
* `txInfo` : the LoRaWAN transmission parameters 
* `rxInfo` : the array of the radio parameters of the duplicated receptions by the gateways
* `rxInfo[]._distance` : the set of distances between the endpoint and the gateway 
 
> The ```object``` field contains the measurement of the weather conditions at the top of the Fort. The weather conditions can be correlated with weather datas from services such as OpenWeatherMap.

> Several fields (gateway name, gateway EUI) are k-anonymized for the sake of privacy. The location of the gateways has been [geo-hashed](https://en.wikipedia.org/wiki/Geohash). The precision is 6 (±0.61 km (0.38 mi; 610 m)). Distance are computed with the GPS-acurate position of the gateways or from the static position set by the gateway installation. The gateway static position can be erroneous.

> Distances are computed with the original locations of the emitter and the receiver.

> Log files have been cleaned and obfuscated using the [scripts](https://gitlab.inria.fr/spelissi/wisec-2022-reproductibility/-/tree/master/code) developed by [Samuel Pélissier](https://orcid.org/0000-0002-3554-2585).

[ND-JSON logs](./logs)

## Dataset from [Requea](https://www.requea.com/)

The endpoint frames has been received by two Multitech MTCDT gateways installed at [Refuge du Goûter](https://en.wikipedia.org/wiki/Go%C3%BBter_Hut) [Location](https://www.openstreetmap.org/search?query=Refuge%20du%20gouter#map=19/45.85108/6.83059) and operated by [Requea](https://www.requea.com/) at Altitude: 3835 meters.

The `Timestamp` field is the relative unsigned 32-bits counter of microseconds of the SX130x concentrator chip.

> `MTCD_Refuge_du_Gouter_LeftSide` is a brand-new R3 model (with SX1303 and two SX1250) isntalled at 13/01/2024.

The distance is approximatly 109 kms in LoS (Line-of-Sight).

> The [Fresnel zone](https://en.wikipedia.org/wiki/Fresnel_zone) radius is 96 meters and the [free-space path loss (FSPL)](https://en.wikipedia.org/wiki/Free-space_path_loss) is 131.80 dB. For your information, FSPL is 145 dB for a [LEO satellite](https://en.wikipedia.org/wiki/Low_Earth_orbit) (500 kms) and 182 dB for a [GEO satellite](https://en.wikipedia.org/wiki/Geostationary_orbit) (35786 kms).

> LoRa Sensitivity is specified with a PER=10%, receiving 12 Byte packets, all under nominal temperature and voltage conditions. According the [Semtech SX1303 datasheet](https://semtech.file.force.com/sfc/dist/version/download/?oid=00DE0000000JelG&ids=0682R000009MnJmQAK&d=%2Fa%2F2R000000Hlli%2FTe0cB6.fNWAPfxRfoFz38R6LOTf3sLAJhD4CpS2RwFc&operationContext=DELIVERY&asPdf=true&viewId=05H3n000002u0NoEAI&dpt=), LoRa sensitivity is measured with a Semtech SX1250 front-end, an LNA with 18dB of gain and 1.5 dB of Noise Figure. The values given in the table 3-6 are : -141 dB @ ```SF12BW125``` (```DR0```) to -129 dB @ ```SF7BW125``` (```DR5```).

[CSV file](./logs)

## Citation

Didier Donsez, Pierre Dubois, Mickael Langlais, Olivier Alphand, "The Saint Eynard LoRaWAN frames dataset", 2024, DOI: Coming Soon [HAL](https://hal.science/hal-04737520)

## Utilities

### Jupyter Notebooks

[Notebooks](./notebooks)

### Grafana dashboards

[Dashboards to import](./grafana)

## Authors
* Didier Donsez (Université Grenoble Alpes LIG)
* Mickael Langlais (CNRS ISTERRE)
* Pierre Dubois (Requea)
* Olivier Alphand (Université Grenoble Alpes LIG)

## License
[ODbL-1.0](LICENSE.txt)

## Gallery

![Saint Eynard](https://github.com/CampusIoT/datasets/tree/main/SaintEynard/wyres_sainteynard.jpg)

Credit: Mickaël Langlais

![Gateway Multitech Refuge du Gouter](https://github.com/CampusIoT/datasets/tree/main/SaintEynard/multitech-refugegouter.jpg)

Credit: Pierre Dubois

![LOS Fort Saint Eynard - Refuge du Gouter](https://github.com/CampusIoT/datasets/tree/main/SaintEynard/maps-sainteynard-gouter.jpg)

![Grafana dashboard](https://github.com/CampusIoT/datasets/tree/main/SaintEynard/grafana.jpg)

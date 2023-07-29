# The Tour Perret LoRaWAN frames dataset

The directory contains the log files of frames sent by LoRaWAN endpoints installed on the top of [Tour Perret](https://en.wikipedia.org/wiki/Perret_tower_(Grenoble)) in Grenoble, France.

> The Tour Perret, originally called La tour pour regarder les montagnes ("The tower for watching the mountains"), is an observation tower located in Grenoble, in the Paul Mistral public park. It is the first tower built in reinforced concrete in Europe.

The endpoints' frames has been received by indoor and outdoor gateways installed in the Grenoble aera by [LIG Lab](https://www.liglab.fr/). The LNS is [Chirpstack](https://www.chirpstack.io/) v3.

Brands and models of the [indoor and outdoor gateways](https://campusiot.github.io/images/gallery.html) are : Multitech (MTCDTIP2, MTCDTIP TDOA, MTCAP), Kerlink (Wirnet, iStation, Femto), RAK Wireless (RAK5146), Mikrotik (LAP8), Strataggem (ecoSignal).

## Endpoints

* 4x [Elsys EMS](https://www.elsys.se/en/lora-ems/) 
* 1x [Wyres Base board](https://github.com/CampusIoT/RIOT-wyres/blob/main/boards/wyres_base/README.md) v2 revC (SX1272, RF switch Skynet new)

The endpoints are installed on four sides (SWW, SSE, NEE, NNW) of the top of the tower (into IP55 enclosures for Elsys EMS).

The endpoints are registered on [Chirpstack](https://www.chirpstack.io/) v3 LNS with as OTAA Class A endpoint. ADR is enabled.

## Dataset

The archive file is available on the [PerSCiDO plateform](https://perscido.univ-grenoble-alpes.fr/datasets/DS395).

The `tourperret.log.gz` [ndjson](http://ndjson.org/) file contains a dataset of 421937 messages received between June 2021 and June 2023 (2 years). 

The fields prefixed by `_` are calculated and  added to the dataset sent by the LNS.

* `applicationName` : the brand and the model of the endpoint
* `devEUI` : the devEUI of the endpoint (hashed)
* `_date` : the archive date (human-readable string)
* `_timestamp` : the millisecond epoch of the archive time
* `data` : the hex-formatted frame payload (plain)
* `object` : the frame payload decoded using the endpoint decoder
* `_devLocation` : the static location of the endpoint
* `txInfo` : the LoRaWAN transmission parameters 
* `rxInfo` : the array of the radio parameters of the duplicated receptions by the gateways
* `rxInfo[]._distance` : the set of distances between the endpoint and the gateway 
* `rxInfo[]._distance._timeOfEmission` : time of emission (in nanosecond) since the `time` of the reception by the gateway.  The `time` field is sometime missing in indoor gateways.

> Several fields are k-anonymized. The location of the gateways has been [geo-hashed](https://en.wikipedia.org/wiki/Geohash). The precision is 6 (±0.61 km (0.38 mi; 610 m)). Distance are computed with the GPS-acurate position of the gateways or from the static position set by the gateway installation. The gateway installation can be erroneous.

> The ```object``` field contains the measurement of the weather conditions at the top of the tower. For Elsys EMS endpoint, the ```accMotion``` field counts the shock inside the steel structure triggered by gusts of wind. The weather conditions can be correlated with weather datas from services such as OpenWeatherMap.

## Citation

Didier Donsez, Olivier Alphand, Nicolas Albarel, "The Tour Perret LoRaWAN frames dataset", 2023, https://doi.org/10.18709/perscido.2023.06.ds395

## Authors

* Didier Donsez (Université Grenoble Alpes LIG)
* Olivier Alphand (Université Grenoble Alpes LIG)
* Nicolas Albarel (ANS Innovation)

## Thanks

Special thanks to Valerie and Dorian, Direction Urbanisme et Aménagement de la ville de Grenoble.

## License
[ODbL-1.0](LICENSE.txt)

## Utilities

```bash
gunzip -c tourperret.log.gz | wc -l
gunzip -c tourperret.log.gz | jq . | more
```

## Gallery

Credit: Didier Donsez, Nicolas Albarel, Nicolas Palix
![Tour Perret](https://github.com/CampusIoT/datasets/blob/main/TourPerret/media/tourperret_01.jpg)
![Eastern panorama from the Tour Perret top roof](https://github.com/CampusIoT/datasets/blob/main/TourPerret/media/tourperret_top_pano_east.jpg)
![Elsys EMS](https://github.com/CampusIoT/datasets/blob/main/TourPerret/media/elsys_ems_tourperret_01.jpg)
![Elsys EMS](https://github.com/CampusIoT/datasets/blob/main/TourPerret/media/elsys_ems_tourperret_02.jpg)
![Elsys EMS and Wyres](https://github.com/CampusIoT/datasets/blob/main/TourPerret/media/elsys_ems_wyres_tourperret_03.jpg)

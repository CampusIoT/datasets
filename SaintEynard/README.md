# The Saint Eynard LoRaWAN frames dataset

The directory contains the log files of frames sent by a LoRaWAN endpoint installed on the top of [Fort du Saint Eynard](https://fr.wikipedia.org/wiki/Fort_du_Saint-Eynard).

The exact location is [45.23513,5.7617](https://www.openstreetmap.org/search?query=45.23513%2C5.7617#map=19/45.23513/5.76170). The GPS altitude is 1350 meters.

## LoRaWAN Emitter

* [Wyres Base board](https://github.com/CampusIoT/RIOT-wyres/blob/main/boards/wyres_base/README.md) 

## Log from CampusIoT

The endpoint's frames has been received by indoor and outdoor gateways installed in the Grenoble aera by [LIG Lab](https://www.liglab.fr/). The LNS is [Chirpstack](https://www.chirpstack.io/) v3. 

> The logs is k-anonymized for the gateway EUI and name. The location of the gateways has been [geo-hashed](https://en.wikipedia.org/wiki/Geohash). Distance are computed with the GPS-acurate position of the gateways.

Coming soon

## Log from Requea

The endpoint frames has been received by a Multitech gateway installed at [Refuge du Goûter](https://en.wikipedia.org/wiki/Go%C3%BBter_Hut) [Location](https://www.openstreetmap.org/search?query=Refuge%20du%20gouter#map=19/45.85108/6.83059) Altitude: 3835 meters.

The distance is approximatly 107 kms in LoS (Line-of-Sight).

> The [Fresnel zone](https://en.wikipedia.org/wiki/Fresnel_zone) radius is 96 meters and the [free-space path loss (FSPL)](https://en.wikipedia.org/wiki/Free-space_path_loss) is 131.80 dB.

Coming soon

## Citation
Didier Donsez, Mickael Langlais, Pierre Dubois, Olivier Alphand, "The Saint Eynard LoRaWAN frames dataset", 2023, DOI: TBC

## Authors
* Didier Donsez (Université Grenoble Alpes LIG)
* Mickael Langlais (CNRS ISTERRE)
* Pierre Dubois (Requea)
* Olivier Alphand (Université Grenoble Alpes LIG)

## License
[ODbL-1.0](LICENSE.txt)

## Gallery

![Saint Eynard](wyres_sainteynard.jpg)
Credit: Mickaël Langlais

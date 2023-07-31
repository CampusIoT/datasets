# The Proof Of Coverage LoRaWAN frames dataset

The directory contains the log files of frames sent by LoRa gateways to other gateways.

The gateways are installed in the Grenoble area by [LIG Lab](https://www.liglab.fr/). Brands and models of the [indoor and outdoor gateways](https://campusiot.github.io/images/gallery.html) are : Multitech (MTCDTIP2, MTCDTIP TDOA, MTCAP), Kerlink (Wirnet, iStation, Femto), RAK Wireless (RAK5146), Mikrotik (LAP8), Strataggem (ecoSignal), Semtech (Picocell, Corecell).

## Modus operandis

The gateways are registered as ABP endpoints on [Chirpstack](https://www.chirpstack.io/) v3 LNS. ADR is disabled.

The gateways send periodically frames to other gateways with various datarates and varions Tx powers.

## Dataset

The archive file is available on the [PerSCiDO plateform](https://perscido.univ-grenoble-alpes.fr/datasets/DS396).

The ```poc-*.log.gz``` files contains a dataset of 3418984 messages received between August 2021 and June 2023.

> The logfile is k-anonymized for the gateway EUI and name. The location of the gateways has been [geo-hashed](https://en.wikipedia.org/wiki/Geohash). The precision is 6 (±0.61 km (0.38 mi; 610 m)). Distance are computed with the GPS-acurate position of the gateways or from the static position set by the gateway installation. The gateway installation can be erroneous.

The fields prefixed by ```_``` are calculated and added to the dataset sent by the LNS.

* ```_date``` : the millisecond epoch of the archive date
* ```_timestamp``` : the millisecond epoch of the archive time
* ```object``` : the frame payload decoded using the PoC decoder. The fields are the gateway id of the sender, a token and the Tx power
* ```_devLocation``` : the location of the emitter
* ```_distance``` : the set of distances between the endpoint and the gateway 
* ```_timeOfEmission``` : time of emission (in nanosecond) since the ```time``` of the reception by the gateway. The ```time``` field is sometime missing in indoor gateways.

> Log files have been cleaned and obfuscated using the [scripts](https://gitlab.inria.fr/spelissi/wisec-2022-reproductibility/-/tree/master/code) developed by [Samuel Pélissier](https://orcid.org/0000-0002-3554-2585).

## Citation

Didier Donsez, Olivier Alphand, "The Proof Of Coverage LoRaWAN frames dataset", 2023, https://doi.org/10.18709/perscido.2023.06.ds396

## Authors

* Didier Donsez (Université Grenoble Alpes LIG)
* Olivier Alphand (Université Grenoble Alpes LIG)

## License
[ODbL-1.0](LICENSE.txt)

## Utilities

```bash
for i in poc-*.log.gz; do gunzip -c $i; done | wc -l
for i in poc-*.log.gz; do gunzip -c $i; done | jq . | more
```

## Gallery
![Kerlink 27 dBm @ Fort du Saint Eynard](https://campusiot.github.io/images/kerlink-sainteynard.jpg)
![Multitech TDOA @ Phitem](https://campusiot.github.io/images/multitech+rtk-01.jpg)
![Kerlink iStation + Taoglas Barracuda 12 dBi @ IMAG](https://campusiot.github.io/images/stations-kerlink-imag.jpg)
![Kerlink iStation @ Polytech Grenoble](https://campusiot.github.io/images/station-kerlink-polytech.jpg)
![Kerlink @ Col du Lautaret](https://campusiot.github.io/images/station-kerlink-lautaret.jpg)

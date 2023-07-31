# The Helium LoRaWAN frames dataset

The dataset contains 95795 LoRaWAN frames sent by endpoints registered on the [Helium LoRaWAN network](https://explorer.helium.com/). It enables to analyze the LoRaWAN link quality with hotspots.

Frames has been collected between Friday 23 July 2021 14:19:52.154 (1627049992.154) to Friday 23 July 2021 14:19:52.154 (1690271047.756)

## Endpoints

Endpoints are described into the `endpoints.csv` file:
* `ELSYS_EMS_B1C1_PERRET_SOO` (`A81758FFFE04B1C1`) : [Elsys EMS endpoint](https://www.elsys.se/en/lora-ems/) installed on the top of the Tour Perret. This endpoint is related to the [The Tour Perret LoRaWAN frames dataset](https://github.com/CampusIoT/datasets/tree/main/TourPerret). Outdoor.
* `IMST_C727B` (`33323431007C727B`) : [IMST iM880a protoboard](https://github.com/CampusIoT/tutorial/blob/master/im880a/im880a-ds75lx.md#figures) installed into the IMAG building rooms (fifth floor). Indoor.
* `FTD_20CBC` (`0018B20000020CBC`) : mobile [Adeunis Field Test Device](https://www.adeunis.com/en/produit/ftd-network-tester/). Indoor/Outdoor.
* `FTP_20CA0` (`0018B20000020CA0`) : mobile [Adeunis Field Test Device](https://www.adeunis.com/en/produit/ftd-network-tester/). Indoor/Outdoor.
* `FTP_20CAC` (`0018B20000020CAC`) : mobile [Adeunis Field Test Device](https://www.adeunis.com/en/produit/ftd-network-tester/). Indoor/Outdoor.
* `POC` (`6081F9835853819F`) : pseudo-endpoint for all the CampusIoT gateways. This endpoint is related to the [The Proof Of Coverage LoRaWAN frames dataset](https://github.com/CampusIoT/datasets/tree/main/ProofOfCoverage). mainly outdoor gateways.

## Distance

Distance are computed between the endpoints and the hotspots.

## Privacy

The location of the [Adeunis Field Test Device](https://www.adeunis.com/en/produit/ftd-network-tester/) are geo-obfuscated for the sake of privacy.

The location of the Helium hotspots are geo-obfuscated for the sake of privacy.

The location of the POC gateways are geo-obfuscated for the sake of privacy.

> Geo-obfuscation uses simply the [geohashing](https://en.wikipedia.org/wiki/Geohash) with a length equals to 6.

> Log files have been cleaned and obfuscated using the [scripts](https://gitlab.inria.fr/spelissi/wisec-2022-reproductibility/-/tree/master/code) developed by [Samuel Pélissier](https://orcid.org/0000-0002-3554-2585).

## GeoJSON

GeoJSON files has been generated from `*.ndjson.gz` files. Emitters are in green and hotspots are in red.

## Authors

* Didier Donsez (Université Grenoble Alpes LIG)
* Olivier Alphand (Université Grenoble Alpes LIG)

## Citation

Didier Donsez, Olivier Alphand, ["The Helium LoRaWAN frames dataset"](https://github.com/CampusIoT/datasets/tree/main/Helium), 2023, DOI is coming soon.

## License
[ODbL-1.0](LICENSE.txt)

## Kaggle

Visit [CampusIoT @ Kaggle](https://www.kaggle.com/campusiot/datasets)

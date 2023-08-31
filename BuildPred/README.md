# BuildPred: A Smart Tertiary Building Dataset

This dataset gathers indoor environmental data and HVAC power consumption collected on a monitored tertirary building over 232 days. The building located into the eastern suburbs of Grenoble (France). Sensors across the building send a measure every 10 minutes, leading to the creation this dataset, after preprocessing.

Several features are monitored over the building:
* 'CO2' monitored by [Adeunis Comfort CO2 sensors](https://www.adeunis.com/en/produit/iaq-co2-temperature-humidity/)
* 'Temperature' monitored by [Adeunis Comfort sensors](https://www.adeunis.com/en/produit/comfort-temperature-humidity-2/) and [Adeunis Comfort CO2 sensors](https://www.adeunis.com/en/produit/iaq-co2-temperature-humidity/)
* 'HVAC consumption' monitored by a [Adeunis Modbus Interface (for powermeter)](https://www.adeunis.com/en/produit/modbus-interface-for-modbus-slaves/)
* 'Particulate matter (PM) / VOC concentrations' monitored by [Adeunis Breath sensors](https://www.adeunis.com/en/produit/breath-indoor-air-quality/)

Around 90 days of data are available for HVAC consumption, without considering holes, from the 03/15/2023 at 16:20 to the 06/14/2023 at 7:30.

Around 232 days of data are available for other features, without considering holes, from the 10/24/2022 at 13:20 to the 06/14/2023 at 7:30.

The [map of sensors installed into the tertirary](https://github.com/CampusIoT/datasets/tree/main/BuildPred/ground_plan_sensors.jpg) building is provided.

![map of sensors installed into the tertirary](https://raw.githubusercontent.com/CampusIoT/datasets/main/BuildPred/ground_plan_sensors.jpg)

## Data format

Each feature listed above amounts to one CSV file. Since sensors are named by the location into the building.

The Adeunis Comfort CO2 sensors monitor temperature and CO2, names can be redundant between CO2 and temperature files.

The first column contains timestamps of measures in milliseconds and each next column contains the measurements of a different sensor.

Each line bring together the measures retrived at the same moment, which matches timestamp of the first column.

## Preprocessing

For the purpose of ML studies, the timestamps of the measurement has been regularized in order to align the timestamp. In order to have one value exactly each 10 minutes, data of corresponding timestamps are interpolated from the raw dataset, which has been deemed reasonable for thes studied features.

Missing data (aka holes) in the time series occur several times because of ponctual system and network problems during the data collection. Missing data has been filled on the left by linear interpolation for the first 40 minutes of the whole. Thus, a very few longer wholes are not filled.

## Contextual data

The installation of powermeters for monitoring the HVAC consumption took time due to compatibility problems.

One of the HVAC could not be monitored. This HVAC is located into the Tech_zone on the map of the building.

The monitored one is close to the window, and doesn't use inputs and outputs. All air input/output is done there, as explained by "all in one" written under the icon.

The break room's HVAC is not monitored yet at the time of the dataset publication

The HVAC from Zone 1 have been changed for a more efficient one, over the 21st and 22nd of march 2023. However, no information is available on the new device, as the owner (responsible for the change) and the inhabitant of the building are different and do not share information. Knowledge was also diluted between several stakeholders. This problem highlights a common situation where data could aim to complete lacking knowledge of the building.

## Notebooks

* [Jupyter notebooks](https://github.com/CampusIoT/datasets/tree/main/BuildPred/notebooks)

## Citation

Louis Closson, Didier Donsez, Jean-Luc Baudouin, Denis Trystram, Christophe Cerin, "A smart tertiary building dataset", 2023, DOI: [doi:10.18709/perscido.2023.08.ds398](https://doi.org/10.18709/perscido.2023.08.ds398)

## Authors

* [Louis Closson](https://www.linkedin.com/in/louis-closson-435341171/) (Adeunis & Université Grenoble Alpes - LIG)
* [Didier Donsez](https://www.linkedin.com/in/didierdonsez/) (Université Grenoble Alpes - LIG)
* [Jean-Luc Baudouin](https://www.linkedin.com/in/jean-luc-baudouin-08389614/) (Adeunis)
* [Denis Trystram](https://www.linkedin.com/in/denis-trystram-a211174/) (Université Grenoble Alpes - LIG)
* [Christophe Cérin](https://www.linkedin.com/in/christophe-c%C3%A9rin-829a3926/) (Université Sorbonne Paris Nord - LIPN)

## Licence

[ODbL-1.0](https://spdx.org/licenses/ODbL-1.0.html#licenseText)

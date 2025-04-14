# The Balloon LR-FHSS frames dataset

The dataset contains 2033 frames sent by 4 end devices during stratospheric balloons flights on May 24th, 2024. Frames were collected for 2 hours and 28 minutes.

**Keywords**: LoRa, LR-FHSS, LoRaWAN, Internet of Things, Stratospheric balloons

## End Devices :
We used 4 LR-FHSS devices dispatched aboard three stratospheric balloons gondolas

| Device Id | Balloon Id | DevAddr | DevEUI |
| --------- | ---------- | ------- | ------ |
| 1 | 1 | `260B5A7A` | `70B3D57ED0066609` | 
| 2 | 2 | `260BAE81` | `70B3D57ED0066806` | 
| 3 | 2 | `260B9030` | `70B3D57ED0066805` | 
| 4 | 3 | `260B83C4` | `70B3D57ED0066804` |

The end devices are four [LR1120 development kits](https://www.semtech.com/products/wireless-rf/lora-edge/lr1120dvk1tbks), from Semtech, runing a [modified version](https://github.com/thingsat/lr-fhss/tree/main/firmware) of the LR-FHSS [application sample code](https://github.com/Lora-net/SWSD003/tree/master/lr11xx/apps/lrfhss) found in the [Lora-net repository](https://github.com/Lora-net). 

> Remark: the devices were initially registered in ABP mode on TheThingsNetwork EU. However, for our experiments, we used a private instance of [Chirpstack v4.7 deployed on a Microsoft Azure virtual machine](https://github.com/thingsat/lr-fhss/tree/main/chirpstack). 


## Gateway
The gateway we used was a [Wirnet iBTS Compact gateway]() from Kerlink, running a custom LR-FHSS enabled firmware provided by semtech.
The gateway was running a custom LR-FHSS enabled firmware provided by Semtech.

## Dataset 

The dataset is available in the [dataset.json](https://github.com/CampusIoT/datasets/blob/main/LR-FHSS/balloons/dataset/dataset.json) file.
The gps data of the balloons is avaiable in the [raw_irma_log](https://github.com/CampusIoT/datasets/tree/main/LR-FHSS/balloons/dataset/raw_irma_logs) folder. It is used by the [notebook](https://github.com/CampusIoT/datasets/blob/main/LR-FHSS/balloons/notebooks/filtering_and_visualization.ipynb) to compute the `estimated_lat_lon_alt` field. The computation is done in the [irma_nacelle_position_parser](https://github.com/CampusIoT/datasets/blob/main/LR-FHSS/balloons/notebooks/irma_nacelle_position_parser.py) file, and is simply a linear interpolation of the positions over time.


### Fields

- `rx_timestamp_ms`: the milisecond timestamp of frame reception
- `dev_addr`: address of the device who sent the frame
- `frame_counter`: frame counter, counts from 0 on the first frame sent
- `coding_rate`: coding rate of the payload fragments, for our experiment, it takes only two values: `CR_2_6` and `CR_4_6` for a coding rate of respectively 1/3 and 2/3
- `channel_width`: the channel bandwidth, in hz, either `137000` or `336000`
- `data_rate`: The corresponding LoRa data rate, for LR-FHSS, it goes from `DR8` to `DR11`
- `tx_power_dbm`: Tx power of the frame, goes from 0 to 16 dBm.
- `rssi_dbm`: Received signal intensity, in dBm
- `balloon_id`: Id of the ballon that sent the frame, goes from 1 to 3
- `estimated_lat_lon_alt`: Estimated position of the ballon when the end device sent the frame. The position is computed from the GPS positions sent by the meteo sondes M20 installed aboard the gondolas

The values are directly avaliable from the gateway logs, except for: 
- the `data_rate`, which is infered from the `coding_rate` and `channel_width`.
- the `balloon_id`, infered from the `dev_addr`
- the `estimated_lat_lon_alt`, infered from the `rx_timestamp_ms` and the logs from the IRMA gps tracker on the balloons.


## Flights

A detailed explanation of the aim of the flights and modules installed on board is available on the [Thingsat repository](https://gricad-gitlab.univ-grenoble-alpes.fr/thingsat/public/-/tree/master/balloons/2024-05-24). There are also pictures.

## Citation

Florent Dobler, Didier Donsez, Léo Cordier, "The Balloon LR-FHSS frames dataset", 2025, https://doi.org/10.18709/perscido.2025.04.ds420
## Authors
- Florent Dobler (Université Genoble Alpes LIG)
- Didier Donsez (Université Genoble Alpes LIG)
- Leo Cordier (Université Genoble Alpes LIG)


![Balloon setup](https://gricad-gitlab.univ-grenoble-alpes.fr/thingsat/public/-/raw/master/balloons/2024-05-24/media/balloon_inflating-03.jpg)



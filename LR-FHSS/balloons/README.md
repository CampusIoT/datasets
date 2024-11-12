# The Balloon LR-FHSS frames dataset

The dataset contains 2033 frames sent by 4 end devices during a balloon flight on `May 24th, 2024`. Frames were collected for `2 hours and 28 minutes`.

**Keywords**: LoRa, LoRaWAN,LR-FHSS, Internet of Things, Balloon

## End Devices :
We used 4 devices, distributed on 3 ballons: 
``` sh
Device 1 (dev addr , dev EUI) Balloon 1
260B5A7A
70B3D57ED0066609

Device 2 (dev addr , dev EUI) Balloon 2
260BAE81
70B3D57ED0066806

Device 3 (dev addr , dev EUI) Balloon 2 
260B9030
70B3D57ED0066805

Device 4 (dev addr , dev EUI) Balloon 3
260B83C4
70B3D57ED0066804
```
The end devices were runing a [modified version](https://github.com/thingsat/lr-fhss/tree/main/firmware) of the LR-FHSS [application sample code](https://github.com/Lora-net/SWSD003/tree/master/lr11xx/apps/lrfhss) found in the [Lora-net repository](https://github.com/Lora-net). 

The gateway was running a custom LR-FHSS enabled firmware provided by semtech.

## Dataset 

The dataset is available in the [dataset.json](../balloons/dataset/dataset.json) file. 

### Fields

- `rx_timestamp_ms`: the milisecond timestamp of frame reception
- `dev_addr`: address of the device who sent the frame
- `frame_counter`: frame counter, counts from 0 on the first frame sent
- `coding_rate`: coding rate of the payload fragments, for our experiment, it takes only two values: `CR_2_6` and `CR_4_6` for a coding rate of respectively 1/3 and 2/3
- `channel_width`: the channel bandwidth, in hz, either `137000` or `336000`
- `data_rate`: The corresponding LoRa data rate, for LR-FHSS, it goes from `DR8` to `DR11`
- `tx_power_dbm`: Tx power of the frame, goes from 0 to 16 dBm.
- `rssi_dbm`: Received signal intensity, in dBm
- `ballon_id`: Id of the ballon that sent the frame, goes from 1 to 3
- `estimated_lat_lon_alt`: Estimated position of the ballon when the end device sent the frame

The values are directly avaliable from the gateway logs, except for: 
- the `data_rate`, which is infered from the `coding_rate` and `channel_width`.
- the `ballon_id`, infered from the `dev_addr`
- the `estimated_lat_lon_alt`, infered from the `rx_timestamp_ms` and the logs from the IRMA gps tracker on the balloons.


## Flight 

A detailed explanation of the aim of the flight and modules installed on board is available on the [Thingsat repository](https://gricad-gitlab.univ-grenoble-alpes.fr/thingsat/public/-/tree/master/balloons/2024-05-24). There are also pictures. 

## Authors
- Florent Dobler (Université Genoble Alpes LIG)
- Didier Donsez (Université Genoble Alpes LIG)
- Leo Cordier (Université Genoble Alpes LIG)

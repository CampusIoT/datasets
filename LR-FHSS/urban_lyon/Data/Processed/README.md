All of these directories contain CSV-like files with the processed frames, the process of analyzing the frames is sequential, and each directory represents one different step in the process. Usually, the final steps are the PDRs and/or PDRsFRQ.
There are different versions of the experiments:
* patches2, being the April's experiments
* patches5, being the July's experiments
* Bicycle experiments: velo5, velo24, velo24nigth, velo25, and velo25nigth.
For more details in different files look in the parent directory. 


## Patches2

Data from 2024-07-11 14:41:41 to 2024-07-23 10:44:25, with a total of 56876 frames.
Each folder represents a different point in the sequential process. The order is as follows:
* The data is divided for each device, devices are enumerated from 1 to 4. 
* The data is divided by DRs (LoRaWAN definitions).
* The data is divided by transmission power (PWS directory).
* The data is divided by frequency channel (FRQ directory).
* The PDR is calculated. Two versions can be done: separated by frequency channel or not. If the PDR is separated by frequency channel, it uses the data from the FRQ directory; if it isn't separated by frequency, the PWS directory is used.
The files are formatted as:
```
PDR_[{Frequency in MHz}]_{Transmission power in dBm}_{DR (LoRaWAN protocol}_{ID of the end-device}.csv
```
The csv files have the following format (except for the PDR files):
| DR | Date and time | payload |Frequency|RSSI (S)|Frequency Offset| SNR|channel S| 
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|...|...|...|

The payload is formatted as:

```
{counter}/{tranmission power}
```
The counter is used to calculate the PDR, and is unique to each set of configurations (dr, frequency and transmission power).

As the process goes on each column is deleted, for example, in the DRs folder the first column is missing (DR), and in the FRQ directory, the frequency and the DR columns are deleted.

The PDRs's csv files are formatted as follows:
| Initial Date and time | Final Date and time |received frames|frames sent|PDR| 
|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|

**PD1: The firmware starts with a payload that reads: '  START OF TEST '**

**PD2: The relationship between the device ID and the position is the following**
```
{1:"600 m", 2:"400 m", 3:"1.5 Km", 4:"770 m"}
```
**Where the key is the device ID and the value is the actual position of deployment**

**PD3: The gateway doesn't measure the SNR of the LR-FHSS physical layer, for this reason in the .csv files this field is filled with '0', but the real SNR is not 0, is unkown**
## Patches5

Data from 2024-07-26 11:17:37 to 2024-09-02 10:41:21, with a total of 226153 frames.
Each folder represents a different point in the sequential process. The order is as follows:
* The data is divided for each device, devices are enumerated from 1 to 4. 
* The data is divided by the physical layer, LR-FHSS or LoRa (modulations directory) 
* The data is divided by coding rate ( CRs directory ).
* The data is divided by transmission power (PWS directory).
* The data is divided by OCW or SF (BWsSFs directory)
* The data is divided by the length of the payload in bytes (LEN directory)
* The data is divided by frequency (FRQ directory)
* The PDR is calculated. Two versions can be done: separated by frequency channel or not. If the PDR is separated by frequency channel, it uses the data from the FRQ directory; if it isn't separated by frequency, the PWS directory is used.
The files are formatted as:
```
PDR_[{Frequency in MHz}]_{length of the payload}_{OCW or SF}_{Transmission power in dBm}_{coding rate}_{physical layer}_{ID of the end-device}.csv
```
The csv files have the following format (except for the PDR files):
| DR or OCW| Date and time | payload |Frequency|RSSI (S)|Frequency Offset| SNR|channel S| Coding rate |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------
|...|...|...|...|...|...|...|...|...|

The payload is formatted as:

```
{counter}/{tranmission power}/{length of the payload}
```
The counter is used to calculate the PDR, and is unique to each set of configurations (physical layer, coding rate, frequency, and length of the payload).

As the process goes on each column is deleted, for example, in the DRs folder the first column is missing (DR), and in the FRQ directory, the frequency and the DR columns are deleted.

The PDRs's csv files are formatted as follows:
| Initial Date and time | Final Date and time |received frames|frames sent|PDR| 
|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|

**PD1: The firmware starts with a payload that reads: '  START OF TEST '**
**PD2: The relationship between the device ID and the position is the following**
```
{1:"600 m", 2:"400 m", 3:"1.5 Km", 4:"770 m"}
```
**Where the key is the device ID and the value is the actual position of deployment**

**PD3: The length of the payload in the payload is calculated and appendedn to the payload during the first process of dividing the data, ig you would see the data in the raw files you wouldn't find the length of the payload, instead you would find a bunch of hash symbols '#' that were used as fillers**

**PD4: The gateway doesn't measure the SNR of the LR-FHSS physical layer, for this reason in the .csv files this field is filled with '0', but the real SNR is not 0, is unkown**
## Velo'x' files
Velos files contain information regarding the measurement of the bicycle experiments, the name of the directory is formatted as velo'x' where x is the number that represents a date of July.


Each folder represents a different point in the sequential process. The order is as follows:
* The data is divided for each device, devices are enumerated from 1 to 5, and only the data from files 4 or 5 are important. 
* The data is divided by DR (DRs directory)
* The PDRs are calculated in two different versions, the ranges are calculated by distance (PDRsDistance) or the ranges are calculated by the counter (PDRsTime, this name is not accurate and should be changed to PDRsCounter)
The files are formatted as:
```
PDR_{DR}_{ID of the end-device}.csv
```

The csv files have the following format (except for the PDR files):
| DR | Date and time | payload |Frequency|RSSI (S)|Frequency Offset| SNR|channel S| 
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|...|...|...|

The payload is formatted as:

```
{counter}
```
The counter is used to calculate the PDR.

As the process goes on each column is deleted, for example, in the DRs folder the first column is missing (DR), and in the FRQ directory, the frequency and the DR columns are deleted.

The PDRs's csv files are formatted as follows:
| Initial distance | Final distance |received frames|frames sent|PDR| 
|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|

As several other experiments were used in parallel with this experiment, you can also see the other devices's data, you should ignore them for this experiment, you can still find that data on the patches files. So no worries there!

The device that should be analyzed for each bicycle ride is the one with ID '5', except for the 5th of July,  on the fifth of July you should analyze device '4'.
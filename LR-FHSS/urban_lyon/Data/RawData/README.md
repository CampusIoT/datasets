# Content

In this directory, you can find .data and .gpx files, these files contain the raw data received from the gateway during the experiments, these files are necessary if:

* You want to recalculate the with different configurations.
* Generate different pictures in the bicycles rides.

The row data totals 1132272 frames. 


## Naming format and content of the data files


The files have a .data extension, this extension is arbitrary and was chosen by the intern (Marcos Rojas Mardones)

They only saved data from the 5 devices that belonged to the experiments.

The naming format of the files is the same as in the Processed directory, this means that the velo files are made in July and the number represent the date, patches2 and 5 are the 'official ones', patches 3 and 4 are contained inside patches5.

The rest of the names simply indicate the day on which that file was created and when it started recording data, the data that finishes or has some 'DRSeker' counted every frame received, independent of the origin, with these files it was possible to know which DR and frequency channels were the most used.

All the .data files are csv-like files and should be analyzed as such.

The format of the .csv files is as follows:

|DevEUI| DR | Date and time | payload |Frequency|RSSI (S)|Frequency Offset| SNR|channel S| 
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|...|...|...|...|...|...|...|...|...|


The relationship between DevEUI and Device ID is as follows:
* 1b24ff2: Device 1
* 2b24ff2: Device 2
* 3b24ff2: Device 3
* 4b24ff2: Device 4
* 5b24ff2: Device 5


## Naming format and content of the gpx files

The gpx files contains the data from gps information on the bicycle rides (positions and times).
There's a 2 hours offset between the hour in the gpx files and the real time on france
This means that you should add 2 hours to every hour in the gpx file.

The gpx file say the day and month of the measurement, if they had an extra '\_nigth' means that the measurement was done in the afternoon
For details for the exact time check each gpx file.

The '\_modify' files are modify version of the gpx file to cut the route until the maximun communication achieved.
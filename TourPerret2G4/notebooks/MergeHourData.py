import math, sys
import csv
from datetime import datetime, timedelta
import json

# *******************************************
DATE_FORMAT = "%Y-%m-%dT%H"


####################################################################
# 

if len(sys.argv) != 3:
    print("ERROR: Missing input parameters (filename test_list)")
    exit()

INPUT_FILE = sys.argv[1]

if (sys.argv[2][0] != '[') and (sys.argv[2][1] != '['):
    print("ERROR: Bad format for test lists")
    exit()
    
TEST_LIST_ALL = eval(sys.argv[2])
print("Test lists " + str(TEST_LIST_ALL), flush=True);

for TEST_LIST in TEST_LIST_ALL:
    target_filename = sys.argv[1][:-4] + "[" + "-".join([str(a) for a in TEST_LIST]) + "].hours.csv"
    DB = []

    print("Read from '" + INPUT_FILE + "' and Write into '" + target_filename + "'", flush=True);
    # Parse input file to merge data hour by hour
    with open(INPUT_FILE, "r") as fp:

        last_timestamp = None
        packet_count = 0
        first_fcount = 0
        last_fcount  = 0
        
        for line in fp:
            if line.startswith("{"):
                data = json.loads(line)
                
                timestamp = datetime.strptime(data['timestamp'][0:-12], DATE_FORMAT)
                if (timestamp != last_timestamp):
                    if (last_fcount-first_fcount) > 30:
                        target_count = ((last_fcount-first_fcount) + 1) * len(TEST_LIST)
                        if (packet_count != 0):
                            DB.append((last_timestamp.isoformat()+"+00:00", round((100 * (target_count - packet_count)) / target_count, 1), int(volt_sum/packet_count), rssi_min, int(rssi_sum/packet_count), rssi_max, snr_min, int(snr_sum/packet_count), snr_max, esp_min, int(esp_sum/packet_count), esp_max))
                        else:
                            DB.append((last_timestamp.isoformat()+"+00:00", 100))

                    # reset stats
                    packet_count = 0
                    snr_sum = 0
                    snr_min = 255
                    snr_max = -255
                    rssi_sum = 0
                    rssi_min = 255
                    rssi_max = -255
                    esp_sum = 0
                    esp_min = 255
                    esp_max = -255
                    volt_sum = 0

                    last_timestamp = timestamp
                    first_fcount = data['fcount']

                # update stats
                last_fcount = data['fcount']

                if data['test'] in TEST_LIST:
                    packet_count += 1
                    volt_sum += data['volt']

                    rssi = data['rssi']
                    rssi_sum += rssi
                    if rssi > rssi_max:
                        rssi_max = rssi
                    if rssi < rssi_min:
                        rssi_min = rssi

                    snr = data['snr']
                    snr_sum += snr
                    if snr > snr_max:
                        snr_max = snr
                    if snr < snr_min:
                        snr_min = snr
                        
                    esp = rssi if (snr >= 0) else (rssi + snr)
                    esp_sum += esp
                    if esp > esp_max:
                        esp_max = esp
                    if esp < esp_min:
                        esp_min = esp

        # last stats
        if (last_fcount-first_fcount) > 30:
            target_count = ((last_fcount-first_fcount) + 1) * len(TEST_LIST)
            if (packet_count != 0):
                DB.append((last_timestamp.isoformat()+"+00:00", round((100 * (target_count - packet_count)) / target_count, 1), int(volt_sum/packet_count), rssi_min, int(rssi_sum/packet_count), rssi_max, snr_min, int(snr_sum/packet_count), snr_max, esp_min, int(esp_sum/packet_count), esp_max))
            else:
                DB.append((last_timestamp.isoformat()+"+00:00", 100))


    # Write result in a CSV file
    with open(target_filename, "w") as tf:
        csv_writer = csv.writer(tf, 'unix', quoting=csv.QUOTE_NONNUMERIC)
        header = False
     
        TITLE = ("timestamp", "per", "voltage", "rssi_min", "rssi_moy", "rssi_max", "snr_min", "snr_moy", "snr_max", "esp_min", "esp_moy", "esp_max")
        csv_writer.writerow(TITLE)

        for sample in DB:
            csv_writer.writerow(sample)

print("Done!")


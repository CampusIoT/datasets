package main

import (
	lorawandecrypt "UDP_sniffer/lorawan_decrypt"
	"bytes"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

func main() {

	key := "CAFEBABE12345678CAFEBABE12345678"
	//QPJP
	finder := []byte{'Q', 'P', 'J', 'P'}

	acceptedDevAddr := []uint32{0x01b24ff2, 0x02b24ff2, 0x03b24ff2, 0x04b24ff2, 0x05b24ff2, 0x06b24ff2, 0x07b24ff2, 0x08b24ff2, 0x09b24ff2}

	currentExecDateTime := time.Now()
	currentExecDate := currentExecDateTime.Format("2006-01-02")

	f, _ := os.Create("outputs/" + currentExecDate + ".data")

	f.Close()

	lorawandecrypt.SetLoRaWANKey(key)

	// Resolve the UDP address
	udpAddr, err := net.ResolveUDPAddr("udp", ":1700")
	if err != nil {
		fmt.Println("Error resolving UDP address:", err)
		return
	}

	// Create a UDP listener
	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		fmt.Println("Error listening:", err)
		return
	}
	defer conn.Close()

	fmt.Println("Listening for UDP messages on port 1700...")

	// Continuously listen for incoming UDP messages
	for {
		// Buffer to hold incoming data
		buffer := make([]byte, 40024)

		// Read data from the connection
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error reading from UDP:", err)
			continue
		}

		// Print the received message
		//fmt.Printf("Received message from %s: %s\n", string(buffer[:n]))

		if bytes.Contains(buffer, finder) {
			fmt.Println("packet found")

			var Sx1302Map map[string]interface{}

			err := json.Unmarshal(buffer[12:n], &Sx1302Map)
			if err != nil {
				fmt.Printf("ERROR: %v\n", err)
			}

			rxpkArray, _ := Sx1302Map["rxpk"].([]interface{})

			for _, rxpk := range rxpkArray {
				rxpkMap, _ := rxpk.(map[string]interface{})

				datr, _ := rxpkMap["datr"].(string)

				codr, _ := rxpkMap["codr"].(string)

				freq, _ := rxpkMap["freq"].(float64)

				modu, _ := rxpkMap["modu"].(string)

				PhyPayload := rxpkMap["data"].(string)

				rsigMap, _ := rxpkMap["rsig"].([]interface{})[0].(map[string]interface{})

				rssi := rsigMap["rssic"].(float64)

				foff := 0.0
				if val, ok := rsigMap["foff"].(float64); ok {
					foff = val
				}

				lsnr := 0.0
				if val, ok := rsigMap["lsnr"].(float64); ok {
					lsnr = val
				}

				chanel := 0.0
				if val, ok := rsigMap["chan"].(float64); ok {
					chanel = val
				}

				LoRaWANData, _ := lorawandecrypt.GetLoRaWANData(PhyPayload)

				DR := DRTranslator(modu, datr, codr)

				if contains(acceptedDevAddr, LoRaWANData.DevAddr) {

					currentDateTimeT := time.Now()
					//currentDate := currentDateTimeT.Format("2006-01-02")
					//currentTime := currentDateTimeT.Format("15:04:05")
					currentDateTime := currentDateTimeT.Format("2006-01-02 15:04:05")

					/*
						fmt.Printf("Date: %v\n", currentDate)
						fmt.Printf("time: %v\n", currentTime)
						fmt.Printf("Date and Time: %v\n", currentDateTime)

						fmt.Printf("Frequency: %v\n", freq)
						fmt.Printf("DR: %v \n", DR)
						fmt.Printf("Payload: %v\n", LoRaWANData.FRMPayload)
						fmt.Printf("DevAddr: %x\n", LoRaWANData.DevAddr)
						fmt.Printf("rssi: %v\n", rssi)
					*/
					DevAddrs := fmt.Sprintf("%x", LoRaWANData.DevAddr)

					file, _ := os.OpenFile("outputs/"+currentExecDate+".data", os.O_WRONLY|os.O_APPEND, 0666)

					freqS := strconv.FormatFloat(freq, 'f', 1, 64)

					rssiS := strconv.FormatFloat(rssi, 'f', 0, 64)

					foffS := strconv.FormatFloat(foff, 'f', 0, 64)

					lsnrS := strconv.FormatFloat(lsnr, 'f', 0, 64)

					chanelS := strconv.FormatFloat(chanel, 'f', 0, 64)

					file.WriteString(DevAddrs + "," + DR + "," + currentDateTime + "," + LoRaWANData.FRMPayload + "," + freqS + "," + rssiS + "," + foffS + "," + lsnrS + "," + chanelS + "," + codr + "\n")

					file.Close()
				} else {
					fmt.Println("Not my device")
				}
			}

		}
	}
}

func DRTranslator(modu string, datr string, codr string) string {
	if modu == "LORA" {
		switch datr {
		case "SF12BW125":
			return "DR0"
		case "SF11BW125":
			return "DR1"
		case "SF10BW125":
			return "DR2"
		case "SF9BW125":
			return "DR3"
		case "SF8BW125":
			return "DR4"
		case "SF7BW125":
			return "DR5"
		case "SF7BW250":
			return "DR6"
		default:
			return "UNKNOWN DATA RATE ON " + datr
		}
	} else if modu == "LR-FHSS" {
		switch datr {
		case "M0CW137":
			switch codr {
			case "1/3":
				return "DR8"
			case "4/6":
				return "DR9"
			default:
				return "UNKNOWN CODING RATE ON " + datr
			}
		case "M0CW336":
			switch codr {
			case "1/3":
				return "DR10"
			case "4/6":
				return "DR11"
			default:
				return "UNKNOWN CODING RATE " + datr
			}
		default:
			return "UNKNOWN BANDWIDTH"
		}
	} else {
		return "UNKNOWN MODULATION"
	}
}

func contains(arr []uint32, target uint32) bool {
	for _, v := range arr {
		if v == target {
			return true
		}
	}
	return false
}

package main

import (
	lorawandecrypt "UDP_sniffer/lorawan_decrypt"
	"fmt"
)

func main() {
	base64String := "QPJPslcAAAAK9NQ6KeZIOMHPYWIBSrp8tx8=" // "Some example text" en base64

	key := "CAFEBABE12345678CAFEBABE12345678"

	lorawandecrypt.SetLoRaWANKey(key)

	// Llamar a la función para convertir base64 a bytes
	LoRaWANData, err := lorawandecrypt.GetLoRaWANData(base64String)
	if err != nil {
		fmt.Printf("Error: %v \n", err)
	}

	// Imprimir la representación en bytes
	fmt.Printf("Mtype: %v\n", LoRaWANData.Mtype)
	fmt.Printf("DevAddr: %x\n", LoRaWANData.DevAddr)
	fmt.Printf("FCtrl: %v\n", LoRaWANData.Fctrl)
	fmt.Printf("Fcnt: %v\n", LoRaWANData.Fcnt)
	fmt.Printf("Fport: %v\n", LoRaWANData.Fport)
	fmt.Printf("FRMPayload: %v \n", LoRaWANData.FRMPayload)

}

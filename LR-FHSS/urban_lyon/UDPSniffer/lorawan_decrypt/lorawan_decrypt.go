//package main

package lorawandecrypt

import (
	"encoding/base64"
	"encoding/binary"
	"encoding/hex"
	"unsafe"

	"github.com/brocaar/lorawan"
)

var Key lorawan.AES128Key

type LoRaWANPhyPayload_t struct {
	Mtype      uint8
	DevAddr    uint32
	Fctrl      byte
	Fcnt       uint16
	Fport      uint8
	FRMPayload string
}

func littleToBigEndian(value uint32) uint32 {
	// Convertir el uint32 a un array de bytes
	bytes := make([]byte, 4)
	binary.LittleEndian.PutUint32(bytes, value)

	// Reinterpretar los bytes en BigEndian
	return binary.BigEndian.Uint32(bytes)
}

func base64ToBytes(base64String string) ([]byte, error) {
	// Decodificar la cadena base64
	decodedBytes, err := base64.StdEncoding.DecodeString(base64String)
	if err != nil {
		return nil, err
	}
	return decodedBytes, nil
}

func decodeMhdr(phyPayload []byte) uint8 {
	mhdr_byte := phyPayload[0]
	mtype := (mhdr_byte >> 5) & 0x07

	return mtype
}

func decodeFhdr(phyPayload []byte) (devAddr uint32, Fctrl byte, Fcnt uint16) {
	fhdrBytes := phyPayload[1:8]

	devAddrInv := fhdrBytes[0:4]

	devAddr = binary.LittleEndian.Uint32(devAddrInv)

	Fctrl = fhdrBytes[4]

	Fcnt = binary.LittleEndian.Uint16(fhdrBytes[5:7])

	return devAddr, Fctrl, Fcnt

}

func SetLoRaWANKey(Cpykey string) error {

	key, err := hex.DecodeString(Cpykey)
	copy(Key[:], key)
	if err != nil {
		return err
	}
	return nil
}

func GetLoRaWANData(base64String string) (LoRaWANPhyPayload_t, error) {

	var LoRaWANData LoRaWANPhyPayload_t

	phyPayloadbytes, err := base64ToBytes(base64String)
	if err != nil {
		return LoRaWANData, err
	}

	//fmt.Printf("Payload: %v\n", phyPayloadbytes)
	//fmt.Printf("Payload: %v\n", base64String)

	if len(phyPayloadbytes) < 14 {
		return LoRaWANData, err
	}

	LoRaWANData.Fport = phyPayloadbytes[8]

	LoRaWANData.Mtype = decodeMhdr(phyPayloadbytes)

	LoRaWANData.DevAddr, LoRaWANData.Fctrl, LoRaWANData.Fcnt = decodeFhdr(phyPayloadbytes)

	endIndex := len(phyPayloadbytes) - 4

	encryptedPayload := phyPayloadbytes[9:endIndex]

	DevaddrBytes := (*lorawan.DevAddr)(unsafe.Pointer(&LoRaWANData.DevAddr))[:]

	for i, j := 0, len(DevaddrBytes)-1; i < j; i, j = i+1, j-1 {
		DevaddrBytes[i], DevaddrBytes[j] = DevaddrBytes[j], DevaddrBytes[i]
	}

	var devAddr_ lorawan.DevAddr

	copy(devAddr_[:], DevaddrBytes)

	decryptFRMPayload, err := lorawan.EncryptFRMPayload(Key, true, devAddr_, uint32(LoRaWANData.Fcnt), encryptedPayload)

	LoRaWANData.FRMPayload = string(decryptFRMPayload)

	LoRaWANData.DevAddr = littleToBigEndian(LoRaWANData.DevAddr)

	return LoRaWANData, err

}

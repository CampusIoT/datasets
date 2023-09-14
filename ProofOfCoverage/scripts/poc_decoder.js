/*
 * Decoder for proof of coverage paylaod
 *
 * @Author: Didier DONSEZ, Université Grenoble Alpes
 */

function byteToHexString(uint8arr, size) {    
    var hexStr = '';
    for (var i = size-1; i >= 0 ; i--) {
      var hex = (uint8arr[i] & 0xff).toString(16);
      hex = (hex.length === 1) ? '0' + hex : hex;
      hexStr += hex;
    }
    return hexStr;
}
  
function readUInt16BE(buf, offset) {
    offset = offset >>> 0;
    return (buf[offset] << 8) | buf[offset + 1];
}

function readUInt8(buf, offset) {
    offset = offset >>> 0;
    return (buf[offset]);
}
  
// For Chirpstack v3
// Decode decodes an array of bytes into an object.
//  - fPort contains the LoRaWAN fPort number
//  - bytes is an array of bytes, e.g. [225, 230, 255, 0]
// The function must return an object, e.g. {"temperature": 22.5}
function Decode(fPort, bytes) {

    // TODO add optional lattitude (float32), longitude (float32), altitude (uint16)
    return {
        gweui: byteToHexString(bytes, 8),
        token: readUInt16BE(bytes, 8),
        txpower: readUInt8(bytes, 10) // in dBm
    }
}

// For TTNv2
// Decode decodes an array of bytes into an object.
//  - bytes is an array of bytes, e.g. [225, 230, 255, 0]
//  - fPort contains the LoRaWAN fPort number
// The function must return an object, e.g. {"temperature": 22.5}
function Decoder(bytes, fPort) {
    return Decode(fPort, bytes);
}

// For TTNv3
function decodeUplink(input) {
    return {
        data: Decoder(input.bytes, input.fPort),
        warnings: [],
        errors: []
    };
}



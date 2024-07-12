# LoRa® & LoRaWAN® Frames Facts

Author: Didier DONSEZ

The LoRa frames has been catched mainly in the Grenoble area.

Time window: 2024-06-28T11:04:26.756Z to 2024-07-07T05:36:02.083Z

* 9520632 LoRa frames
* 2243921 LoRa frames with BAD_CRC
* 7276537 LoRa frames with CRC_OK
* 2472953 DataUp LoRaWAN frames
* 972206 JoinRequest LoRaWAN frames

> NB : ESP is Estimated Signal Power
```javascript
function esp(rssi, snr) {
    return Math.round(100*(rssi + snr - (10*Math.log10(1 + Math.pow(10,0.1*snr)))))/100;
}
console.log(esp(-112,-3));
// expected output: -116.76434862436486
```

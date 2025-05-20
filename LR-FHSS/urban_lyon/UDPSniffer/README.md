# Content
In this file you can see the code used to retrieve the frames from the gateway, this code was running as a service on a computed connected to the gateway that was receiving the frames.

The code was writted on golang in hopes to avoid any frames losses due to lack of speed.

The function used a list called 'finder', this 'finder' this magical number is a base64 code that correlate directly to the frames used in this experiments, i.e. all the frames sended by our devices during these experiments always started with 'Q', 'P', 'J', 'P', this allowed to retreive only the packages used by us with out having to decrypt the whole frame, this is only possible because all the devices had a devaddr like xxb24ff2.

Once this first fast filter is applied the packet is decrypt and filter again using the LoRaWAN protocol in order to only retreive our frames
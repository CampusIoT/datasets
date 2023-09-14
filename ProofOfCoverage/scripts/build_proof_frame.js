/*
 * Build a uplink LoRaWAN frame for testing gateways coverage
 *
 * @Author: Didier DONSEZ, Université Grenoble Alpes
 */

const lora_packet = require("lora-packet");

/*
    node build_proof_frame.js \
        fc00af01 \
        1 \
        10 \
        1234 \
        cafebabecafebabecafebabecafebabe \
        babecafebabecafebabecafebabecafe \
        868.5 \
        12 125 \
        14 \
        1234567890abcdef

*/

function usage(){
    console.error("node build_frame.js DevAddr FCnt FPort Token AppSKey NwkSKey Fraquency SF BW TxPower Gweui");
}

const args = process.argv;
if (args.length !== 13) {
  usage();
  process.exit(1);
}

const DevAddr = process.argv[2];
const FCnt = Number.parseInt(process.argv[3]);
const FPort = Number.parseInt(process.argv[4]);
const Token = Number.parseInt(process.argv[5]); // Token help to trace the sent frame and the received message
const AppSKey = process.argv[6]; 
const NwkSKey = process.argv[7];
const Frequency = Number.parseInt(process.argv[8]);
const SF = Number.parseInt(process.argv[9]);
const BW = Number.parseInt(process.argv[10]);
const TxPower = Number.parseInt(process.argv[11]);
const Gweui = process.argv[12];

const GweuiBuf = Buffer.from(Gweui, "hex");
GweuiBuf.swap64();
const Payload = Buffer.allocUnsafe(11);
GweuiBuf.copy(Payload, 0, 0, 8);
Payload.writeUInt16LE(Token, 8);
Payload.writeUInt8(TxPower, 10);
//console.log(Payload.toString("hex"));

// create a packet
const constructedPacket = lora_packet.fromFields(
  {
    MType: "Unconfirmed Data Up", // (default)
    DevAddr: Buffer.from(DevAddr, "hex"), // big-endian
    FCtrl: {
      ADR: false, // default = false
      ACK: false, // default = false
      ADRACKReq: false, // default = false
      FPending: false, // default = false
    },
    FPort: FPort, // can supply a buffer or a number
    FCnt: FCnt, // can supply a buffer or a number
    payload: Payload,
  },
  Buffer.from(AppSKey, "hex"), // AppSKey
  Buffer.from(NwkSKey, "hex") // NwkSKey
);
const wireFormatPacket = constructedPacket.getPHYPayload();

const hex = wireFormatPacket.toString("hex");
const base64 = wireFormatPacket.toString("base64");

const command_down = {
    "phyPayload": base64,
    "txInfo": {
      "gatewayID": Buffer.from(Gweui,"hex").toString("base64"),
      "frequency": Frequency,
      "power": TxPower,
      "modulation": "LORA",
      "loRaModulationInfo": {
        "bandwidth": BW,
        "spreadingFactor": SF,
        "codeRate": "4/5",
        "polarizationInversion": false // for uplink (endpoint --> gateways) 
      },
      "board": 0,
      "antenna": 0,
      "timing": "IMMEDIATELY",
      "context": "AnWqsw==" // TODO
    },
    "token": Token,
    "downlinkID": Payload.toString("base64")
  };

console.log(JSON.stringify(command_down,null,0));


#include <lmic.h>
#include <hal/hal.h>

const uint8_t GREEN_LED = 13;
const uint8_t YELLOW_LED = 11;
const uint8_t RED_LED = 2;

const uint8_t SWITCH_PIN = 14;

uint16_t counter = 0;
uint8_t currentState = 0;

uint32_t TX_INTERVAL_MSEC = 0;
uint32_t lastTx = 0;

static uint8_t payload[5];
static osjob_t initjob;
static osjob_t sendjob;
static lmic_event_cb_t handleEventCb;
static lmic_rxmessage_cb_t handleMessageReceivedCb;
static hal_failure_handler_t halFailureHandler;

// This EUI must be in little-endian format, so least-significant-byte
// first. When copying an EUI from ttnctl output, this means to reverse
// the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
// 0x70.
static const u1_t PROGMEM APPEUI[8] = { 0xE0, 0xA1, 0x03, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
void os_getArtEui (u1_t* buf) {
  memcpy_P(buf, APPEUI, 8);
}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8] = { 0x83, 0x67, 0xEA, 0xF5, 0x46, 0x0D, 0x12, 0x00 };
void os_getDevEui (u1_t* buf) {
  memcpy_P(buf, DEVEUI, 8);
}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
static const u1_t PROGMEM APPKEY[16] = { 0x7E, 0x86, 0x50, 0xA6, 0xAC, 0xE3, 0x84, 0x58, 0x59, 0x81, 0x10, 0xC7, 0xA9, 0x16, 0x63, 0x11 };
void os_getDevKey (u1_t* buf) {
  memcpy_P(buf, APPKEY, 16);
}

// Pinmap for Econode Gen3
const lmic_pinmap lmic_pins = {
  .nss = 8,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 31,
  .dio = {30, 5, 27},
};

void setup() {
  delay(1000);
  SerialUSB.begin(115200);
  SerialUSB.println(F("Starting"));

  writeDefaultValuesData();

  pinMode(SWITCH_PIN, INPUT_PULLUP);
  currentState = digitalRead(SWITCH_PIN);

  hal_set_failure_handler(hal_failure);
  os_init();
  os_setCallback(&initjob, initfunc);
  SerialUSB.println(F("Setup done."));
}

static void initfunc (osjob_t* j) {
  SerialUSB.println(F("LMIC init..."));
  LMIC_reset();
  LMIC_registerEventCb(handleEventCb, NULL);
  LMIC_registerRxMessageCb(handleMessageReceivedCb, NULL);
  LMIC_setClockError(MAX_CLOCK_ERROR * 2 / 100);
  LMIC_setAdrMode(1);
  LMIC_setLinkCheckMode(1);
  LMIC_setDrTxpow(DR_SF10, AU915_TX_EIRP_MAX_DBM);
  LMIC_selectSubBand(1);
  LMIC_startJoining();
  lastTx = millis();
  do_send(&sendjob);
  SerialUSB.println(F("LMIC initialised"));
}

void hal_failure(const char* const file, const uint16_t line) {
  SerialUSB.print(F("==================== ASSERTION ================="));
#if defined(LMIC_FAILURE_TO)
  LMIC_FAILURE_TO.println("FAILURE ");
  LMIC_FAILURE_TO.print(file);
  LMIC_FAILURE_TO.print(':');
  LMIC_FAILURE_TO.println(line);
  LMIC_FAILURE_TO.flush();
#endif
  for (;;) {
    // do nothing and wait for the eventual...
  }
}

static void handleMessageReceivedCb(void *pUserData, u1_t port, const u1_t *payload, size_t payloadSize) {
  SerialUSB.print(F("Received on port "));
  SerialUSB.print(port);
  SerialUSB.print(F(":"));
  for (uint8_t i = 0; i < payloadSize; i++) {
    SerialUSB.print(payload[i], HEX); SerialUSB.print(F(" "));
  }
  SerialUSB.println();

}

void do_send(osjob_t* j) {
  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    SerialUSB.println(F("OP_TXRXPEND, not sending"));
  } else {
    payload[0] = lowByte(counter);
    payload[1] = highByte(counter);
    payload[2] = currentState ? 0x00 : 0x01;

    payload[3] = 0;

    SerialUSB.print(F("Sending... "));
    lmic_tx_error_t sendResult = LMIC_setTxData2(1, payload, 4, 0);
    if (sendResult == LMIC_ERROR_SUCCESS) {
      // stay awake until TX complete and RX window closed
    } else {
      SerialUSB.print(F("Tx error: ")); SerialUSB.println(sendResult);
      // TX_COMPLETE will not be called, hence we need to enable sleep again, or we will stay awake.
    }
  }
  // reset, even when TxRx pending
  lastTx = millis();
}

static void handleEventCb(void *pUserData, ev_t ev) {
  switch (ev) {
    case EV_JOINING:
      SerialUSB.println(F("EV_JOINING"));
      break;
    case EV_JOINED:
      SerialUSB.println(F("EV_JOINED"));
      {
        u4_t netid = 0;
        devaddr_t devaddr = 0;
        u1_t nwkKey[16];
        u1_t artKey[16];
        LMIC_getSessionKeys(&netid, &devaddr, nwkKey, artKey);
        SerialUSB.print(F("netid: "));
        SerialUSB.println(netid, DEC);
        SerialUSB.print(F("devaddr: "));
        SerialUSB.println(devaddr, HEX);
        SerialUSB.print(F("artKey: "));
        for (uint8_t i = 0; i < sizeof(artKey); ++i) {
          if (i != 0) {
            SerialUSB.print(F("-"));
          }
          SerialUSB.print(artKey[i], HEX);
        }
        SerialUSB.println();
        SerialUSB.print(F("nwkKey: "));
        for (uint8_t i = 0; i < sizeof(nwkKey); ++i) {
          if (i != 0) {
            SerialUSB.print(F("-"));
          }
          SerialUSB.print(nwkKey[i], HEX);
        }
        SerialUSB.println();
      }
      break;
    case EV_JOIN_FAILED:
      SerialUSB.println(F("EV_JOIN_FAILED"));
      // todo: what shall we do? Sleep for some time and then try again?

      //      LMIC_startJoining();

      break;
    case EV_TXCOMPLETE:
      SerialUSB.println(F("EV_TXCOMPLETE"));
      if (LMIC.txrxFlags & TXRX_ACK) {
        SerialUSB.println(F("Received ack"));
      }
      // Schedule next transmission
      break;
    case EV_RXCOMPLETE:
      SerialUSB.println(F("EV_RXCOMPLETE"));
      break;
    case EV_LINK_DEAD:
      // No confirmation has been received from the network server for an extended period of time.
      // Transmissions are still possible, but their reception is uncertain.
      SerialUSB.println(F("EV_LINK_DEAD"));
      break;
    case EV_TXSTART:
      SerialUSB.println(F("EV_TXSTART"));
      break;
    case EV_RXSTART:
      /* do not print anything -- it wrecks timing */
      break;
    case EV_JOIN_TXCOMPLETE:
      SerialUSB.println(F("EV_JOIN_TXCOMPLETE"));
      break;
    default:
      SerialUSB.print(F("Unknown event: "));
      SerialUSB.println((unsigned) ev);
      break;
  }
}

void releaseDetected() {
  counter += 1;
  SerialUSB.print(F("Counter: ")); SerialUSB.println(counter);
  do_send(&sendjob);
}

void resetDetected() {
  return;
  do_send(&sendjob);
}

void probe() {
  uint8_t result = digitalRead(SWITCH_PIN);
  // only if different from last result
  if (currentState != result) {
    // trap status changed (released or re-set)
    currentState = result;
    if (currentState == 0) {
      // trap has released - bar is down
      SerialUSB.println(F("Trap has released"));
      releaseDetected();
    } else {
      SerialUSB.println(F("Trap has re-set"));
      resetDetected();
    }
  }
}

void loop() {
  os_runloop_once();
  probe();
  if (millis() -  lastTx > TX_INTERVAL_MSEC) {
    do_send(&sendjob);
  }
}



void writeDefaultValuesData() {
  counter = 0;
  TX_INTERVAL_MSEC = (uint32_t)60 * 60 * 2 * 1000;
}

import network
import urequests
import time
from machine import Pin
import dht

# ─────────────────────────────────────────
#  CONFIG  (edit these before uploading)
# ─────────────────────────────────────────
SSID       = "Robotic WIFI"
PASSWORD   = "rbtWIFI@2025"
BOT_TOKEN  = ""
CHAT_ID    = ""

TEMP_THRESHOLD = 33.0   # °C  – alert / auto-OFF boundary
POLL_INTERVAL  = 5      # seconds per loop

# ─────────────────────────────────────────
#  HARDWARE PINS  (matches wiring diagram)
#   DHT22 DATA → D4  |  Relay IN → D2
# ─────────────────────────────────────────
sensor = dht.DHT11(Pin(4))      # Task 1 – DHT11 on D4
relay  = Pin(2, Pin.OUT)        # Relay on D2
relay.value(0)                  # start with relay OFF

# ─────────────────────────────────────────
#  TELEGRAM ENDPOINTS
# ─────────────────────────────────────────
BASE_URL    = "https://api.telegram.org/bot{}".format(BOT_TOKEN)
URL_SEND    = BASE_URL + "/sendMessage"
URL_UPDATES = BASE_URL + "/getUpdates"

# ─────────────────────────────────────────
#  STATE
# ─────────────────────────────────────────
relay_on      = False   # mirrors physical relay state
last_update_id = 0      # Telegram polling offset

# ─────────────────────────────────────────
#  WI-FI  (simple connect; no auto-reconnect per lab scope)
# ─────────────────────────────────────────
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
print("Connecting to WiFi...")
while not wifi.isconnected():
    time.sleep(1)
print("WiFi connected:", wifi.ifconfig()[0])

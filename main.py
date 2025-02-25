import network
import time
import dht
import machine
from umqttsimple import MQTTClient

# Konfigurasi WiFi
SSID = "NAMA_WIFI"
PASSWORD = "PASSWORD_WIFI"

# Konfigurasi Ubidots
TOKEN = "UBIDOTS_TOKEN"
MQTT_BROKER = "industrial.api.ubidots.com"
TOPIC = "/v1.6/devices/esp32"  # Ganti dengan nama device Ubidots-mu

# Inisialisasi WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("Terhubung ke WiFi:", wlan.ifconfig())

# Inisialisasi DHT11 di GPIO14
dht_sensor = dht.DHT11(machine.Pin(14))

# Koneksi ke WiFi
connect_wifi()

# Koneksi ke MQTT Ubidots
client = MQTTClient("ESP32", MQTT_BROKER, user=TOKEN, password="", port=1883)
client.connect()

# Loop utama untuk membaca dan mengirim data
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print(f"Suhu: {temperature}°C, Kelembaban: {humidity}%")

        # Kirim data ke Ubidots dalam format JSON
        payload = '{"temperature": %s, "humidity": %s}' % (temperature, humidity)
        client.publish(TOPIC, payload)

        time.sleep(10)  # Kirim setiap 10 detik

    except Exception as e:
        print("Error:", e)

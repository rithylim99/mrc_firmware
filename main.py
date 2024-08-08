import paho.mqtt.client as mqtt
import json
import time
import joblib
import numpy as np
import asyncio
import logging
import serial  # Add this import for serial communication
from telegram import Bot
from telegram.request import HTTPXRequest

# Set up logging to console
logging.basicConfig(level=logging.DEBUG)

# Define Telegram Bot Token and Group Chat ID
TELEGRAM_BOT_TOKEN = '6838900751:AAEm24REbail8hJ7CHUmdksZzkyAK9oWWz4'  # Replace with your bot's API token
TELEGRAM_GROUP_CHAT_ID = '-1002200655323'  # Replace with your group's chat ID

# Threshold water level for alert
WATER_LEVEL_THRESHOLD = 0.6  # meters

# Create an HTTPXRequest instance with custom connection pool size
trequest = HTTPXRequest(connection_pool_size=20)

# Create a Telegram bot instance with the custom HTTPXRequest
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=trequest)

# Load the trained model
model = joblib.load('data_trainning/trained_model.joblib')

# Define ThingsBoard host and access token
THINGSBOARD_HOST = 'demo.thingsboard.io'  # Change this to your ThingsBoard host
ACCESS_TOKEN = 'EpqA2CCYSU2NXtidnoAe'  # Replace with your device access token

# Define the topic to publish data to
topic = f'v1/devices/me/telemetry'

# Create an MQTT client
client = mqtt.Client()

# Set the access token as username for authentication
client.username_pw_set(ACCESS_TOKEN)

async def send_alert(water_level, flood_probability):
    """Send an alert if the water level exceeds the threshold."""
    message = (
        f"សេចក្តីជូនដំណឹង! \n"
        f"កម្ពស់ទឹកបច្ចុប្បន្ន មានការកើនឡើងរហូតដល់ {water_level}m ដែលភាគរយអាចបង្កអោយមានគ្រោះទឹកជំនន់មានដល់ទៅ {flood_probability* 100:.2f}% ។ សម្រាប់ទន្និន័យលម្អិត សូមចុចដំណរខាងក្រោម: \n"
        f"http://surl.li/xjnjbd \n"
        f"Notice! \n"
        f"The current water level has risen to {water_level}m, which is {flood_probability* 100:.2f}% of the potential for flooding. For detailed data, please click the link below: \n"
        f"http://surl.li/xjnjbd \n"
    )
    try:
        # Send a message to the Telegram group
        await bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=message)
        print(f"Alert sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def predict_flood_probability(water_level):
    """Predict flood probability based on water level."""
    input_data = np.array([[water_level]])
    probabilities = model.predict_proba(input_data)
    flood_probability = probabilities[0][1]
    return flood_probability

# Define the callback functions (optional)
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")

# Assign the callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the ThingsBoard server
client.connect(THINGSBOARD_HOST, 1883, 60)

# Loop to maintain the connection and publish data
client.loop_start()

async def main():
    last_alert_time = 0
    alert_interval = 60  # 60 seconds for checking the alert

    # Configure the serial connection (adjust the port, baud rate, and timeout as needed)
    ser = serial.Serial('COM5', 9600, timeout=1)  # Replace 'COM3' with your port

    try:
        while True:
            # Read data from the serial port
            serial_data = ser.readline().decode('utf-8').strip()

            if serial_data:
                try:
                    water_level = float(serial_data)
                except ValueError:
                    print(f"Invalid data received: {serial_data}")
                    continue

                if water_level < 0.1 or water_level > 1.2:
                    print("Water level must be between 0.1 and 1.2 meters. Please try again.")
                    continue

                # Predict flood probability
                flood_probability = predict_flood_probability(water_level)
                percentage_flood = flood_probability * 100
                print(f'When Water Level = {water_level} meters, Probability of Flood: {percentage_flood:.2f}%')

                # Send Telegram alert if water level exceeds threshold
                current_time = time.time()
                if water_level > WATER_LEVEL_THRESHOLD and (current_time - last_alert_time >= alert_interval):
                    await send_alert(water_level, flood_probability)
                    last_alert_time = current_time

                # Define the telemetry data payload
                payload = {
                    'water level': water_level,  # Example data
                    'water level cm': water_level * 100,
                    'flood probability': percentage_flood  # Example data
                }

                # Convert the payload to a JSON string
                payload_json = json.dumps(payload)

                # Publish the data to the specified topic
                client.publish(topic, payload_json)
                await asyncio.sleep(0.01)  # Sleep for a bit before next input

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()  # Close the serial port
        client.loop_stop()
        client.disconnect()
        await bot.session.close()  # Ensure client is closed properly

if __name__ == "__main__":
    asyncio.run(main())

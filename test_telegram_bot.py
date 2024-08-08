import asyncio
import time
import logging
from telegram import Bot
from telegram.request import HTTPXRequest

# Set up logging to console
logging.basicConfig(level=logging.DEBUG)

# Define Telegram Bot Token and Group Chat ID
TELEGRAM_BOT_TOKEN = '6838900751:AAEm24REbail8hJ7CHUmdksZzkyAK9oWWz4'  # Replace with your bot's API token
TELEGRAM_GROUP_CHAT_ID = -1002200655323  # Replace with your group's chat ID

# Threshold temperature for alert
TEMP_THRESHOLD = 30.0  # Celsius

# Create an HTTPXRequest instance with custom connection pool size
trequest = HTTPXRequest(connection_pool_size=20)

# Create a Telegram bot instance with the custom HTTPXRequest
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=trequest)

async def send_alert(temperature):
    """Send an alert if the temperature exceeds the threshold."""
    message = (
        f"សេចក្តីជូនដំណឹង! \n"
        f"កម្ពស់ទឹកបច្ចុប្បន្ន មានការកើនឡើងរហូតដល់1m ដែលភាគរយអាចបង្កអោយមានគ្រោះទឹកជំនន់មានទៅដល់ 70% ។ សម្រាប់ទន្និន័យលម្អិត សូមចុចនូវដំណរខាងក្រោម: \n"
        f"http://surl.li/xjnjbd \n"
        f"Notice! \n"
        f"The current water level has risen to 1m, which is 70% of the potential for flooding. For detailed data, please click the link below: \n"
        f"http://surl.li/xjnjbd \n"
    )
    try:
        # Send a message to the Telegram group
        await bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=message)
        print(f"Alert sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def main():
    last_alert_time = 0
    alert_interval = 5  # 5 seconds for testing

    try:
        while True:
            # Read temperature input from the terminal
            raw_input = input("Enter a temperature reading: ")

            try:
                # Convert the input string to a float
                temperature = float(raw_input)

                current_time = time.time()
                if temperature > TEMP_THRESHOLD and (current_time - last_alert_time >= alert_interval):
                    # Send alert if temperature exceeds threshold
                    asyncio.run(send_alert(temperature))
                    last_alert_time = current_time

            except ValueError:
                print("Invalid input. Please enter a valid number.")

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()

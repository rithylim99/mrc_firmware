import serial
import csv
import datetime

# Replace 'COM3' with your port name and set the appropriate baud rate
port = 'COM12'
baud_rate = 9600
output_file = 'serial.csv'

try:
    # Open serial port
    ser = serial.Serial(port, baud_rate, timeout=1)
    print(f"Connected to {ser.portstr}")

    # Open the CSV file in write mode
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row (optional)
        writer.writerow(['Timestamp', 'Data'])

        while True:
            # Read a line of data from the serial port
            data = ser.readline().decode('utf-8').rstrip()
            if data:
                # Get the current timestamp
                timestamp = datetime.datetime.now().isoformat()
                print(f"Received at {timestamp}: {data}")
                # Write the data to the CSV file
                writer.writerow([timestamp, data])

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

import serial
import tkinter as tk
from tkinter import ttk

# Create a tkinter window
window = tk.Tk()
window.title("Distance Display")

# Create a label to display the distance
distance_label = tk.Label(window, text="Distance: ")
distance_label.pack()

# Create a label and a slider for the alarm limit
limit_label = tk.Label(window, text="Alarm Limit:")
limit_label.pack()
limit_slider = ttk.Scale(window, from_=0, to=100, length=200, orient="horizontal")
limit_slider.pack()

# Open the serial port
ser = serial.Serial('COM10', 9600)  # Update the port name if necessary

# Function to update the distance label
def update_distance():
    if ser.in_waiting > 0:
        # Read the data from serial port
        data = ser.readline().decode().strip()
        # Update the distance label
        distance_label.config(text=data)
    window.after(1, update_distance)  # Schedule the function to run after 1ms

# Function to update the alarm limit
def update_alarm_limit():
    ser.flush()
    # Read the value from the slider
    alarm_limit = limit_slider.get()
    # Send the new alarm limit to the Pi Pico
    data = str(int(alarm_limit))
    print(data)
    ser.write(f"L {data}".encode()) 

# Button to update the alarm limit
update_button = tk.Button(window, text="Update", command=update_alarm_limit)
update_button.pack()

# Start updating the distance label
update_distance()

# Start the tkinter event loop
window.mainloop()

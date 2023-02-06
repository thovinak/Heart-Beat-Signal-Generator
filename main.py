#
#  Copyright (c) 2023 - All rights reserved.
#  Created by Karthik Thovinakere for PROCTECH 4IT3/SEP 6IT3.
#
#  SoA Notice: I Karthik Thovinakere, 400140562 certify that this material is my original work.
#  I certify that no other person's work has been used without due acknowledgement.
#  I have also not made my work available to anyone else without their due acknowledgement.

# imports
import time

import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt


# MQTT server connection
def mqtt_server_connect(server_name):
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    try:
        client.connect(host=server_name)
        client.loop()  # Looping the server to be able to receive messages and publish
        return client

    except:
        return 1
    return 0


# Generate a heartbeat signal
def heartbeat_signal(t, amplitude, frequency, noise_level):
    y = amplitude * (np.sin(2 * np.pi * frequency * t) + 0.5 * np.sin(2 * np.pi * 2 * frequency * t))
    # Adds Gaussian noise to the signal
    noise = np.random.normal(0, noise_level, len(y))
    return y + noise


# Main function
def main():
    try:
        # Set the parameters
        t = np.linspace(0, 10, 1000)  # Evenly spaced numbers over a specified interval
        amplitude = 1  # 1V
        frequency = 1.25  # 1.25Hz
        plot_freq = 1000  # 1ms
        noise_level = 0.5  # 0.5V
        # Connect to the Local MQTT server
        mqtt_client = mqtt_server_connect("127.0.0.1")

        while True:
            # Get the current time and machine time for the particular package[floating point]
            start_time = time.time()
            # Generate a heartbeat signal
            noise = heartbeat_signal(t=t, amplitude=amplitude, frequency=frequency, noise_level=noise_level)

            # Convert the signal to a string
            noise_to_str_mqtt = str(noise)
            print(noise_to_str_mqtt)
            mqtt_client.publish(topic="noise/heartbeat", payload=noise_to_str_mqtt, qos=1)

            # Plot the signal
            plt.subplot(1, 1, 1)
            t = np.linspace(0, 10, plot_freq)
            plt.plot(t, noise)
            plt.title('Typical ECG Signal with Gaussian Noise ')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.show()

            # Sleep for 1 second
            stop_time = time.time()
            time.sleep(1 - (stop_time - start_time))
    except:
        return 1
    return 0


# Run the main function
if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)

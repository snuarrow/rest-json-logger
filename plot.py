import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random
import json
import threading
from time import sleep

data = None
running = False

def start_animation():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    y2s = []
    y3s = []
    


    def animate(i, xs, ys, y2s, y3s):
        # Read temperature (Celsius) from TMP102
        with open(f"latest_read.json") as f:
            data = json.load(f)
            print(json.dumps(data))
            f.close()
        temp_c = data["responses"][2]["temperature"]

        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        ys.append(temp_c)
        y2s.append(data["responses"][1]["temperature"])
        y3s.append(data["responses"][0]["temperature"])

        # Limit x and y lists to 20 items
        xs = xs[-50:]
        ys = ys[-50:]
        y2s = y2s[-50:]
        y3s = y3s[-50:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)
        ax.plot(xs, y2s)
        ax.plot(xs, y3s)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('TMP102 Temperature over Time')
        plt.ylabel('Temperature (deg C)')
        

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, y2s, y3s), interval=180000)
    plt.show()

def plot():
    sleep(20)
    print('plotting')
    start_animation()
    #global running
    #if not running:
    #    running = True
    #    thread = threading.Thread(name='daemon', target=start_animation)
    #    thread.setDaemon(True)
    #    thread.start()

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random
import json
import sys
import threading
from time import sleep
import numpy as np
import pandas as pd
import seaborn as sns

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


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def plot_24h():
    file_name = "/home/username/logs/2022_02_20_00.json"
    with open(file_name, "r") as f:
        logs = json.load(f)

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(30, 15))

    data = {}
    data["times"] = []
    data["temps"] = []

    for line in logs:
        ts = dt.datetime.strptime(line["t"],"%Y-%m-%d %H:%M:%S.%f")
        temperature = line.get("responses", [])[0]["humidity"]
        if temperature:
            data["times"].append(ts)
            data["temps"].append(temperature)
        #print(json.dumps(line, indent=4))
        #print(type(ts))
        #exit()


    data["temps"] = moving_average(data["temps"], 21)
    data["times"] = data["times"][10:-10]
    print(len(data["times"]))
    print(len(data["temps"]))
    plt.ylim(18,42)
    sns.lineplot(x=data["times"], y=data["temps"])
    plt.show()
    plt.savefig("matplotlib.png")

def main():
    #sleep(20)
    print('plotting')
    plot_24h()
    #start_animation()
    #global running
    #if not running:
    #    running = True
    #    thread = threading.Thread(name='daemon', target=start_animation)
    #    thread.setDaemon(True)
    #    thread.start()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

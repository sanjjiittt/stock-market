import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

x_data, y_data = [], []
price = 100  # starting price

def get_new_price():
    global price
    price += random.uniform(-1, 1)  # simulate price change
    return price

fig, ax = plt.subplots()
line, = ax.plot([], [], color='blue')
ax.set_title("Live Stock Price")
ax.set_xlabel("Time")
ax.set_ylabel("Price")

frame_count = 0

def update(frame):
    global frame_count
    y = get_new_price()
    x_data.append(frame_count)
    y_data.append(y)
    frame_count += 1
    line.set_data(x_data, y_data)
    ax.relim()
    ax.autoscale_view()
    return line,

ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
plt.show()
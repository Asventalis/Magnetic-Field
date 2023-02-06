import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import keyboard

p = 3
i = 1/p
n_arrows = 20
distance = 3

x,y = np.meshgrid(np.linspace(-5,5,n_arrows),np.linspace(-5,5,n_arrows))

fig, ax = plt.subplots(1, 1)
divnorm = colors.TwoSlopeNorm(vmin=0, vcenter=10, vmax=20)
color_map_name = 'hot'

def magnetic_field(cx, cy, i):
    Bx = i*(y-cy)/((x-cx)**2 + (y-cy)**2)
    By = -i*(x-cx)/((x-cx)**2 + (y-cy)**2)
    M = np.sqrt(Bx**2 + By**2)
    BNx = Bx/M
    BNy = By/M
    return BNx, BNy, M


vector_fields = []

def rotate_vector(x, y, theta):
    x_rot = x*np.cos(theta) - y*np.sin(theta)
    y_rot = x*np.sin(theta) + y*np.cos(theta)
    return x_rot, y_rot


time = 0.01
delta_time = 1
startx, starty = 0, distance
sum_x, sum_y = 0, 0
for k in range(p):
    vec_x, vec_y, M = magnetic_field(startx,starty,i*np.sin(2*np.pi/p*k+time))
    sum_x += vec_x*M
    sum_y += vec_y*M
    vec_x, vec_y, M = magnetic_field(-startx,-starty,-i*np.sin(2*np.pi/p*k+time))
    sum_x += vec_x*M
    sum_y += vec_y*M
    startx, starty = rotate_vector(startx, starty, 2*np.pi/p)
time += delta_time

tot_M = np.sqrt(sum_x**2 + sum_y**2)
sum_x, sum_y = sum_x/tot_M, sum_y/tot_M
tot_M = 1/tot_M
qr = ax.quiver(x,y,sum_x,sum_y, tot_M, cmap=color_map_name, norm=divnorm)

def animate(num, qr, x, y):
    global time
    global delta_time
    if keyboard.is_pressed('d'):
        delta_time = 1
    elif keyboard.is_pressed('a'):
        delta_time = -1
    elif keyboard.is_pressed('space'):
        if delta_time == 0:
            delta_time = 1
        else:
            delta_time = 0
    time += delta_time
    startx, starty = 0, distance
    sum_x, sum_y = 0, 0
    for k in range(p):
        vec_x, vec_y, M = magnetic_field(startx,starty,i*np.sin(2*np.pi/p*k+0.1*time))
        sum_x += vec_x*M
        sum_y += vec_y*M
        vec_x, vec_y, M = magnetic_field(-startx,-starty,-i*np.sin(2*np.pi/p*k+0.1*time))
        sum_x += vec_x*M
        sum_y += vec_y*M
        startx, starty = rotate_vector(startx, starty, 2*np.pi/p)
    tot_M = np.sqrt(sum_x**2 + sum_y**2)
    sum_x, sum_y = sum_x/tot_M, sum_y/tot_M
    tot_M = 1/tot_M
    qr.set_UVC(sum_x, sum_y, tot_M)

ani = animation.FuncAnimation(fig, animate, fargs=(qr, x, y), interval=100, blit=False)
plt.show()
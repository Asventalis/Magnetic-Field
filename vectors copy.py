import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import keyboard

p = 8
i = 1/p
n_arrows = 33
distance = 3
ring_distance = 2.8


p *= 2 if p%2 == 0 else 1
x,y = np.meshgrid(np.linspace(-5,5,n_arrows),np.linspace(-5,5,n_arrows))
angle, m = np.meshgrid(np.linspace(0,2*np.pi,3*n_arrows),np.linspace(0,0,1))


def magnetic_field(cx, cy, i):
    Bx = -i*(y-cy)/((x-cx)**2 + (y-cy)**2)
    By = i*(x-cx)/((x-cx)**2 + (y-cy)**2)
    M = np.sqrt(Bx**2 + By**2)
    return Bx, By, M


def magnetic_field_modules_at_distance(cx, cy, i, distance):
    x_coord = np.cos(angle)*distance
    y_coord = np.sin(angle)*distance
    BxD = -i*(y_coord-cy)/((x_coord-cx)**2 + (y_coord-cy)**2)
    ByD = i*(x_coord-cx)/((x_coord-cx)**2 + (y_coord-cy)**2)
    MD = np.sqrt(BxD**2 + ByD**2)
    return BxD, ByD, MD


def rotate_vector(x, y, theta):
    x_rot = x*np.cos(theta) - y*np.sin(theta)
    y_rot = x*np.sin(theta) + y*np.cos(theta)
    return x_rot, y_rot


def magnetic_field_on_couples(p, i, distance, time):
    startx, starty = 0, distance
    sum_x, sum_y = 0, 0
    for k in range(p):
        vec_x, vec_y, M = magnetic_field(startx,starty,i*np.sin(2*np.pi/p*k+time))
        sum_x += vec_x
        sum_y += vec_y
        vec_x, vec_y, M = magnetic_field(-startx,-starty,-i*np.sin(2*np.pi/p*k+time))
        sum_x += vec_x
        sum_y += vec_y
        startx, starty = rotate_vector(startx, starty, 2*np.pi/p)
    tot_M = np.sqrt(sum_x**2 + sum_y**2)
    return sum_x, sum_y, tot_M


def magnetic_field_modules_on_couples(p, i, distance, ring_distance, time):
    startx, starty = 0, distance
    ang_x, ang_y = 0, 0
    for k in range(p):
        vecd_x, vecd_y, dM = magnetic_field_modules_at_distance(startx,starty,i*np.sin(2*np.pi/p*k+time), ring_distance)
        ang_x += vecd_x
        ang_y += vecd_y
        vecd_x, vecd_y, dM = magnetic_field_modules_at_distance(-startx,-starty,-i*np.sin(2*np.pi/p*k+time), ring_distance)
        ang_x += vecd_x
        ang_y += vecd_y
        startx, starty = rotate_vector(startx, starty, 2*np.pi/p)
    tot_MD = np.sqrt(ang_x**2 + ang_y**2)
    return ang_x, ang_y, tot_MD


fig, (ax, ax2) = plt.subplots(1, 2)
divnorm = colors.TwoSlopeNorm(vmin=-1, vcenter=5, vmax=40)
color_map_name = 'plasma'


qr = ax.quiver(x,y, 0, 0, 0, cmap=color_map_name, norm=divnorm)
qr2 = ax2.quiver(angle,m,0,0, cmap=color_map_name, norm=divnorm)
qr2circle = ax2.quiver(np.cos(angle),np.sin(angle),0,0, cmap=color_map_name, norm=divnorm)


time = 1.01
delta_time = 0.1
show_circle = False
normalized = False


def iterate(first=False):
    global time
    global delta_time
    global ring_distance
    global show_circle
    global normalized
    if keyboard.is_pressed('d'):
        delta_time = 0.1
    elif keyboard.is_pressed('a'):
        delta_time = -0.1
    elif keyboard.is_pressed('space'):
        if delta_time == 0:
            delta_time = 0.1
        else:
            delta_time = 0
    elif keyboard.is_pressed('up'):
        ring_distance += 0.1
    elif keyboard.is_pressed('down'):
        ring_distance -= 0.1
    elif keyboard.is_pressed('c'):
        show_circle = not show_circle
    elif keyboard.is_pressed('n'):
        normalized = not normalized
    
    sum_x, sum_y, tot_M = magnetic_field_on_couples(p, i, distance, time)
    ang_x, ang_y, MD = magnetic_field_modules_on_couples(p, i, distance, ring_distance, time)
    mod = ang_x*np.cos(angle) + ang_y*np.sin(angle)
    
    if normalized:
        sum_x, sum_y = sum_x/tot_M, sum_y/tot_M
        ang_x, ang_y = ang_x/MD, ang_y/MD
        mod = mod/MD

    C1, C2, C3 = 1/tot_M, 1/MD, 1/MD
    if first:
        C1, C2, C3 = divnorm.vmax, divnorm.vmax, divnorm.vmax
    
    qr.set_UVC(sum_x, sum_y, C1)
    qr2circle.set_UVC(ang_x, ang_y, C2)
    qr2.set_UVC(0, mod, C3)

    if not first:
        if show_circle:
            ax2.set_xlim(-1.2, 1.2)
            qr2.set_UVC(0, 0, divnorm.vmax)
        else:
            ax2.set_xlim(0, 2*np.pi)
            qr2circle.set_UVC(0, 0, divnorm.vmax)
        time += delta_time


iterate(first=True)


def animate(num):
    iterate()


ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)
plt.show()
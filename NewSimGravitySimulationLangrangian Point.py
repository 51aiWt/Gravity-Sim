# Size scaled from real life to pixels:1px=0.005AU => 1px=7.48*10^8m

# Modules to run the code
import pygame
import math 
from sys import exit

# Pygame initialization
pygame.init()

# Set up the display

# The screen size is 800 by 600 pixels (width x height)
screen = pygame.display.set_mode((800, 600)) 

# Set the window title
pygame.display.set_caption("Gravitational Simulation")

# Creates a clock object to manage the frame rate
clock = pygame.time.Clock()                           

# Initial parameters of Earth

# meters x postion of the earth from the sun 1.496*10^11 meters original value
x_1=1.3*10**11 

# meter the y postion of the earth
y_1=0

# m/s the x velocity of the earth
v_x_1=0  

# 365.24 days Period of earth around the sun or 3.1553280 * 10^7 seconds
T=3.1553280 * 10**7 

# angular velocity of earth around the sun rad/s
w=(2 * math.pi)/T   

# m/s the y velocity of the earth (w is negative to flip to counter clockwise)
v_y_1=-w*x_1    

# Physical properties of the system

# kg mass of the sun original value 1.988*10^30 in case needed 
m_0=1.988*10**30

# kg mass of the earth original value 5.972*10^24 in case needed
m_1=5.972 *10**24   

# meters distance between the sun and the earth
r_10=(x_1**2 + y_1**2)**0.5 

# The third object/ satellite initial parameters

# meters x position of the satellite from the sun
x_2=x_1 * math.cos(math.sin(60))

# meter the y postion of the satellite from the sun
y_2=x_1 * math.sin(math.cos(60))

# m/s the x velocity of the satellite initially I set to 0
v_x_2=w*y_2 

# m/s the y velocity of the satellite (w negative to flip to counter clockwise)
v_y_2= -w*x_2 

# meters radius between the sun and the satellite
r_20=(x_2**2 + y_2**2)**0.5

# meters radius between the earth and the satellite
r_21=((x_2 - x_1)**2 + (y_2 - y_1)**2)**0.5

# Physical Set Constants relevant to the simulation

# Nm^2/kg^2 newton's gravitational constant 6.674 * 10^-11 original value
G=6.674 * 10**-11 

# time elapsed in seconds (s)
t=0      

# in seconds (s) used to speed up the simulation time not UI time
time_scaled=10**7

# a list to store the path points of the earth on a x,y coordinate system
path_points=[]   

# a list to store the path points of the satelite on a x,y coordinate system
path_points_two=[]

# store the false value to dictate when the simulation stops running
stopped=False    

# Sun representation

# Creates a surface with a name. Has a diameter of 50 pixels not to scale.
sun_surface = pygame.Surface((50, 50), pygame.SRCALPHA)    

# Yellow circle on the surface to represent the sun. With radius of 25 pixels.
pygame.draw.circle(sun_surface, (255, 255, 0), (25, 25), 25)

# Earth representation

# Creates a surface with a name. Has a diameter of 20 pixels not to scale.
earth_surface=pygame.Surface((20,20),pygame.SRCALPHA) 

# Blue circle on the surface to represent the earth. With radius of 10 pixels.
pygame.draw.circle(earth_surface,(0,0,255),(10,10),10)

# Satellite representation

# Creates a surface with a name. Has a diameter of 10 pixels not to scale.
satelite_surface=pygame.Surface ((10,10),pygame.SRCALPHA)

# Grey circle on the surface to represent the satellite. With radius of 5 pixels.
pygame.draw.circle(satelite_surface,(150,150,150),(5,5),5)

# Keep the simulation running to update the position of the Earth.

# A while true loop that if the user clicks the close button, quit the program.
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            exit()

# This simulation will do the following calculations if not stopped.
    if not stopped:

# Time in seconds by dt(10^-3 seconds) used time_scaled to speed up sim time.
        dt = (clock.tick(60) / 1000) *time_scaled

# Time in seconds by adding dt cumulatively to time t.
        t+= dt 

# These eq's finds the force of gravity and the angle of vectors.

# Gives the velocity of earth m/s based on forced applied to earth
        delta_v_one = (G * m_0 / (r_10**2)) * dt

# Gives the velocity of satellite m/s based on force applied to satellite
        delta_v_20=(G * m_0 / (r_20**2)) * dt
        delta_v_21=(G * m_1 / (r_21**2)) * dt

# Angle of the position using arccos,(uses y_1 as a quadrant check)
        if y_1 >= 0:
            theta_1 = math.acos(x_1 / r_10)
        else:
            theta_1 = -math.acos(x_1 / r_10)

# Angle of the position using arccos,(uses y_2 as a quadrant check)
        if y_2 >= 0:
            theta_2= math.acos(x_2 / r_20)
        else:  
            theta_2= -math.acos(x_2 / r_20)

# Using our calculated theta, delta_vx and y finds direction.Velocity is m/s
        delta_vx = -delta_v_one * math.cos(theta_1)
        delta_vy = -delta_v_one * math.sin(theta_1)

# Using our calculated theta_2, delta_vx and y finds direction.Velocity is m/s
        delta_vx_20=-delta_v_20 * math.cos(theta_2)
        delta_vy_20=-delta_v_20 * math.sin(theta_2)

# Angle between M1 and M2 using arccos,(uses y_2 as quadrant check)
        if y_2 >=0:
            alpha=math.acos((x_2-x_1)/r_21)
        else:
            alpha=-math.acos((x_2 - x_1)/r_21)

# Using our calculated alpha, delta_vx and y finds direction.Velocity is m/s
        delta_vx_21=delta_v_21 * math.cos(alpha)
        delta_vy_21=delta_v_21 * math.sin(alpha)

# Combined velocity changes for satellite
        delta_vx_2=delta_vx_20 + delta_vx_21
        delta_vy_2=delta_vy_20 + delta_vy_21

# New positions meter in x and y components for satellite
        delta_x_2=delta_vx_2 * dt
        delta_y_2=delta_vy_2 * dt
        x_prime_2=x_2 + delta_x_2
        y_prime_2=y_2 + delta_y_2

# new velocities (temporaries) m/s
        v_primex = v_x_1 + delta_vx
        v_primey = v_y_1 + delta_vy

# new positions (temporaries) meter in x and y components
        delta_x = v_primex * dt
        delta_y = v_primey * dt
        x_prime = x_1 + delta_x
        y_prime = y_1 + delta_y

# Switches new variable value to old variables updating the old variables

# The satellite position and velocity updates
        v_x_2=delta_vx_2 + v_x_2
        v_y_2=delta_vy_2 + v_y_2
        x_2 += v_x_2 * dt
        y_2+=v_y_2 * dt

# velocity x component m/s
        v_x_1 = v_primex

# velocity y compenent m/s
        v_y_1 = v_primey 

# x coordinate meters
        x_1 = x_prime 

# y coordinate meters
        y_1 = y_prime 

# update distance for next step
        r_10=(x_1**2 + y_1**2)**0.5

# update distances for next step concerning the satellite
# r20 (sun to satellite), r21 (earth to satellite)
        r_20=(x_2**2 + y_2**2)**0.5
        r_21=((x_2 - x_1)**2 + (y_2 - y_1)**2)**0.5

# meters => pixels x,y cordinates set eqal to scaled values and are centered
        x = (x_1 / (7.48*10**8)) + 400
        y = (y_1 / (7.48*10**8)) + 300

# meters => pixels, _obj describes satellite positions centered
        x_2obj=(x_2 / (7.48*10**8)) +400
        y_2obj=(y_2 / (7.48*10**8)) +300

# takes x,y points gives and appends to path_points list from 
        path_points.append((int(x), int(y)))

# takes x,y points of satellite and appends to path_points_two list
        path_points_two.append((int(x_2obj),int(y_2obj)))

# Makes the screen color black
    screen.fill((0, 0, 0))

# For point in path_points_two, draw purple path to repsent orbit of satellite
    for point in path_points_two:

# Draw small magenta circles at each point in the path with a radius of 2 pixels
        pygame.draw.circle(screen,(255,0,255),point,2)

# For points in the path list, draw a path to represent the orbit of the earth
    for point in path_points:

# Draw small cyan circles at each point in the path with a radius of 2 pixels
        pygame.draw.circle(screen, (0, 255, 255), point, 2)

# Draw Earth with a changing x,y position taking away 10 for centering Earth
    screen.blit(earth_surface, (x-10, y-10))

# Draw Satellite with changing x,y position taking away 5 for centering
    screen.blit(satelite_surface,(x_2obj -5,y_2obj -5))

# Draw Sun where it's in the center and taking away 25 for centering Sun
    screen.blit(sun_surface, (400 - 25, 300 - 25))

# Displays the screen updates and sets the frame rate to 60 FPS
    pygame.display.update()
    clock.tick(60)
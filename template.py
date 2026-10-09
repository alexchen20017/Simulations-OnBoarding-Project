
PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
class State:
    xvel: float 
    xpos: float
    ypos: float
    time: float
    propulsion_force: float
    lateral_vel: float = 0.0

time_step = 0.1 

def step (state:State) -> State:
    # radius = 0.216 Part 1 Variables
    # gear_ratio = 3
    # max_torque = 180
    mass = 300
    forward_speed = 15
    corner_stiffness = 36000
    air_density = 1.2 
    cross_sectional_area = 1.2
    drag_coeff = 0.7
    max_propulsion = 2000
    v_max = 27
    max_brake = 1850
    acc = 0.0

    # this is for part 1, simulating a driver holding down the pedal
    # if state.time <= 7:
    #     driver_input = state.time / 7
    # elif state.time <= 22:
    #     driver_input = 1.0
    # else:
    #     driver_input = 0.0
    
    if state.time <= 3: # Simulating a driver holding down the pedal to calc propulsion force
        driver_input = state.time / 3
    elif state.time <= 23:
        driver_input = 1.0
    else:
        driver_input = 0.0

    #Brakes
    if state.time <= 2:
        driver_brake = 0.0
    elif state.time > 2:
        driver_brake = 1.0

    if driver_brake > 0.0:
        driver_input = 0.0 # this is to not model accleration so no need for throttle

    # Steering Wheel
    if state.time <= 3:
        steer_angle = (state.time / 3 ) * 5 * (np.pi / 180) # converts deg to rad
    elif state.time <= 10:
        steer_angle = 5 * (np.pi / 180)
    else:
        steer_angle = 0.0

    #Drag
    if state.time <= 10:
        acc = 5.0
    else:
        acc = 0.0

    #part 1
    # command_torque = max_torque * driver_input
    # force_at_wheels = (command_torque * gear_ratio) / radius
    # acc = force_at_wheels / mass

    braking_force = driver_brake * max_brake 
    brake_acc = - (braking_force / mass) # negative so that it can actually slow down

    new_propulsion_force = max_propulsion * driver_input * (1 - (state.xvel / v_max))
    acc = new_propulsion_force / mass # rewrote F = ma, to a = F/m

    drag = 0.5 * cross_sectional_area * drag_coeff * air_density * (state.xvel * state.xvel)
    net_acc = acc - (drag / mass) # acc loses speed to air resistance
    total_acc = net_acc + brake_acc # need this because need to get total acc of the car when braking

    slip_angle = steer_angle - (state.lateral_vel / forward_speed)
    lateral_force = corner_stiffness * slip_angle
    lateral_acc = lateral_force / mass
    new_lateral_vel = state.lateral_vel + (lateral_acc * time_step)

    new_vel = state.xvel + total_acc * time_step 
    new_xpos = state.xpos + state.xvel * time_step # tracks where the car is on x-axis
    new_time = state.time + time_step # adds time to make the simulation run

    print(new_vel)
    if new_vel >= 0.0:
        new_state = State(
            xvel = new_vel,
            xpos = new_xpos,
            ypos = 0.0,            
            time = new_time,
            propulsion_force = new_propulsion_force,
            lateral_vel = new_lateral_vel
        )
        return new_state
    raise ValueError("Velocity is now less than 0")

def animate (i):
    global s0
    s0 = step(s0)
    ax.clear()
    ax.scatter([s0.xpos], [s0.ypos], s = 200, c = 'pink', marker = 's')
    ax.set_xlim(0,300) 
    ax.set_ylim(0,10)
    return ax,

s0 = State(
    # gives the object defult values of 0
    xvel = 25,
    xpos = 0,
    ypos = 0,
    time = 0,
    propulsion_force = 0,
    lateral_vel = 0,
)

fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
# these lines are so the animation doesnt zoom in or out
ani = animation.FuncAnimation(
    fig, 
    animate, 
    interval=30,  # Recommended: use a reasonable interval like 30ms instead of 0
    cache_frame_data=False
)

plt.show()
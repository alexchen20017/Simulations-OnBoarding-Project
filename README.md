# Simulations Onbaording Project
This is a simulation of a simplified physics car engine where the car has a throttle, brake, sterring wheel, and a motor. To make the engine realistic, the simulation must mimic real life and to do that, there will be drag and traction. In the code, we must update the state of the car during every time step, meaning we must update the velocity, position, time, and propulsion force.

## Description
**Throttle** 
The throttle is being simulated by having a driver press on the accleration pedal to move it forward. The speed at which the car is moving will be calculated by the equatations:
Command torque = driver input * maximum motor torque
Force at the wheels = (command torque * gear ratio) / radius of the wheels
accleration = Force at the wheels / mass. 

**Traction**
For a more realistic interpretation, the wheels of the car will need to slow down due to the friction of the road. To do this, we also must calculate the slip angle because the direction of the tires and the direction the car is moving is different. The slip angle is where the tire changes direction, which causes the car to turn. Lateral velocity is where the tire not being able to follow the steering wheel 100%, which causes part of the car's motion to slide perpendicular to the direction that it is pointing. These are the equations used:

Slip angle = steer angle - (lateral velocity / forward speed)
Lateral force = cornering stiffness * slip angle
Later acceleration = lateral force / mass
lateral velocity = lateral velocity (previous) + (lateral acceleration * timestep)

**Drag**
Drag is what happenes when the air resistance pushes the car when it is moving, either making it acclerate or de-accelerate. To calculate how fast the car is moving with drag, we must calculate the cross sectional area (how much air it needs to push out of the way) and the drag coefficient (how well the car moves in the air). These are the equations used:

Drag = 0.5 * cross sectional area * drag coefficient * air density * velocity^2
net acceleration = acceleration - (drag / mass)
velocity = velocity + (net acceration * timestep)

**Motor**
The motor is what causes the car to go forwards or backwards. When it runs, it causes back-EMF, which limits how much torque the motor can deliver. This makes it so the car cannot keep acclerating forever. These are the equations used:

Propulsion force = maximum propulsion force * throttle input * (1 - (v / max))
Acceleration = force / mass
Velocity = velocity + (acceration * timestep)

**Brakes**
The car will need to be able to slow down and to do that, there must be a brake pedal. The more the simulated driver steps onto the pedal, the slower the velocity of the car will get, eventually going to 0 m/s. These are the equations used:

Braking force = driver input * maximum braking capacity 
Acceleration = - (braking force /mass)
Velocity = velocity + (acceleration * timestep)
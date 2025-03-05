# Orbits Simulator

**Orbits Simulator** is an interactive Python application that **simulates gravitational systems** using a simplified approximation of physical laws.  
The project combines **VPython** for 3D visualization and **Tkinter** for the graphical user interface, allowing users to create, modify, and delete celestial objects in the simulation.

## Important Note
**Warning:** The simulation is based on a **simplified model** of gravity and interactions, so the results should be considered approximate and intended for **educational purposes** rather than an exact replication of a real system.

## Features
- Create and customize celestial bodies.
- Simulate gravitational forces between objects.
- Interactive controls to drag and move objects.
- Real-time visualization of orbits and object movement.
- Pause, play, and restart the simulation.

## Requirements
- **Python 3**
- **VPython:** For 3D visualization (more information at [VPython](https://vpython.org/))
- **Tkinter:** Typically included with Python installations

## How the code works
The simulation is built around basic physics formulas and a simple numerical integration scheme.  
Here’s a closer look at the underlying mechanics:

### Gravitational Force Calculation:
- **Newton's Law of Universal Gravitation**  
  Each celestial body computes the gravitational force exerted by every other body using the formula:

  $\mathbf{F} = G \frac{m_1 m_2}{r^2}$

  Where:
  - $G$ is the gravitational constant.
  - $m_1$ and $m_2$ are the masses of the two bodies.
  - $r$ is the distance between the bodies.

  This is implemented in the `calc_gravitational_force` method of the `Body` class.

### Numerical Integration:
- **Euler Integration Method**  
  The simulation updates the velocity and position of each body using the Euler method:  
  $\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \mathbf{a}(t) \Delta t$  
  $\mathbf{x}(t+\Delta t) = \mathbf{x}(t) + \mathbf{v}(t) \Delta t$

  Where:
  - $\mathbf{a}(t)\$ is the acceleration computed as the net force divided by the mass.
  - $\Delta t$ (referred to as 'DT' in the code) is the fixed time step.
  
  While the Euler method is simple and computationally inexpensive, it can introduce numerical errors over long simulation periods and may not conserve energy perfectly.

### Constants and Their Values:
In the simulation, some constants are set to values that simplify the calculations:
- **G = 1:** The gravitational constant is set to 1 for simplicity. This does not represent the actual gravitational constant, but it simplifies calculations for educational purposes.
- **DT = 0.01:** The time step is fixed at 0.01. This value provides a good balance between simulation accuracy and computational performance. Adjusting DT can affect the precision and stability of the simulation.


### Approximations and Limitations:
- **Simplified Dynamics**  
  - The simulation does not include effects such as relativistic corrections, collisions, or tidal forces.
  - It assumes point-mass interactions without considering rotational dynamics or other complex phenomena.

- **Integration Accuracy**  
  - Using a fixed time step and Euler integration, the simulation may show drifting or unstable orbits over time.
  - The calculated trajectories are approximate and best viewed as illustrative rather than exact.

- **Overall Accuracy**  
  Although the gravitational force calculation follows Newtonian mechanics accurately, the overall simulation accuracy is limited by the numerical integration and the simplified physical model.
  This means that while the simulation provides a good visual and educational representation of gravitational interactions, it is not suited for high-precision scientific computations.

## How to Run
1. Clone this repository:
   
   ```
   git clone https://github.com/camilafresitaa/OrbitsSimulator
   ```

2. Install the necessary libraries:

   ```
   pip install vpython
   pip install tkinter
   ```

3. Run the simulation:

   ```
   run orbits_simulator.py
   ```

## Controls
- **Play:** Start the simulation.
- **Pause:** Pause the simulation.
- **Restart:** Reset the simulation and all objects.
- **Add Objects:** Click the '**+**' button to add new celestial bodies.

Explore, experiment, and enjoy creating your own universe with Orbits Simulator!

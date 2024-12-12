### README for Particle Simulator

---

## **Particle Simulator**

A dynamic and interactive particle simulation created using Python and Pygame. Particles move, collide, and interact with the environment based on user input and physical principles like velocity and friction.

---

### **Features**

1. **Particle Behavior:**
   - Particles bounce off window boundaries.
   - Collisions between particles adjust their velocities.
   - Friction slows particle movement over time.

2. **User Interactions:**
   - Adjust simulation speed.
   - Spawn new particles dynamically.
   - Increase velocity of particles.
   - Push particles away from the mouse cursor.

3. **Responsive UI:**
   - Window resizing keeps particles within bounds.
   - Adjustable clock speed and friction for customized simulations.

---

### **Setup**

#### **Prerequisites**

- Python 3.8 or higher
- `pygame` library

Install Pygame by running:

```bash
pip install pygame
```

---

### **Usage**

1. Clone the repository or download the files.
2. Run the `main.py` file:

```bash
python main.py
```

3. Use the following controls to interact with the simulation:

---

### **Controls**

| **Key/Action**       | **Effect**                                                                                  |
|-----------------------|--------------------------------------------------------------------------------------------|
| **Mouse Click**       | Prints particle index and increases velocity for the particle under the cursor.            |
| **`+` Key**           | Increase simulation speed.                                                                |
| **`-` Key**           | Decrease simulation speed.                                                                |
| **`P` Key**           | Pause/unpause the simulation.                                                             |
| **`E` Key**           | Spawn a new particle at a random position.                                                |
| **`M` Key**           | Increase friction.                                                                        |
| **`N` Key**           | Decrease friction.                                                                        |
| **`F` Key**           | Push nearby particles away from the mouse cursor.                                         |
| **Number Keys (1-0)** | Set specific clock speeds (e.g., `1` for `0.001`, `2` for `0.002`, etc.).                  |

---

### **Project Structure**

```
ParticleSimulator/
│
├── lib/
│   ├── __init__.py         # Library initializer
│   ├── particle.py         # Particle class and collision handling
│   ├── utils.py            # Helper functions like spawning and finding particles
│   ├── config.py           # Global variables like window size, clock, and friction
│   ├── standalone.py       # The script in one file
│
├── main.py                 # Main script to run the simulation
└── README.md               # Documentation
```

---

### **Customization**

You can tweak the following variables in `/lib/config.py`:

- `window_size`: Set the initial window size.
- `clock`: Adjust the default simulation speed.
- `friction`: Change how quickly particles slow down.

---

### **License**

No license yet :(

---

Enjoy simulating and experimenting with particle behavior!<br>
This documentation was spell/grammar checked by ChatGPT, if you care.
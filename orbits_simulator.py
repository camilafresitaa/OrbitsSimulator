import vpython as vp
import tkinter as tk
from tkinter import ttk

vp.scene.background = vp.color.black
vp.scene.range = 20
vp.scene.userzoom = False

G = 1
DT = 0.01

colors = {
        "White": vp.color.white,
        "Red": vp.color.red,
        "Green": vp.color.green,
        "Blue": vp.color.blue,
        "Yellow": vp.color.yellow,
        "Cyan": vp.color.cyan,
        "Magenta": vp.color.magenta,
        "Orange": vp.vector(1, 0.5, 0),
        "Purple": vp.vector(0.5, 0, 0.5)
        }

rosita = "#edb1d0"

simulation_running = False

all_objects = []



# TEXTS

no_objects_text = vp.label(text='Press the + button to add objects', pos=vp.vector(0, 0, 0),
                          height=15, color=vp.color.white, align="center", box=False)

paused_text = vp.label(text='Simulation paused', pos=vp.vector(0, -16, 0),
                          height=15, color=vp.color.white, align="center", box=False, visible=False)

def update_texts():
    no_objects_text.visible = len(all_objects) == 0
    paused_text.visible = (simulation_running == False) and (len(all_objects) > 0)



# BODY CLASS

class Body():
    def __init__(self, name, position=(0,0,0), velocity=(0,0,0), mass=20, radio=2, colorcito=vp.color.white):
        self.name = name
        self.position = vp.vector(*position)
        self.velocity = vp.vector(*velocity)
        self.mass = mass
        self.object = vp.sphere(pos=self.position, radius=radio, color=colorcito, make_trail=False, trail_radius=0.1)
        self.force = vp.vector(0,0,0)

        self.initial_position = vp.vector(*position)
        self.initial_velocity = vp.vector(*velocity)

    def __repr__(self):
        return f"{self.name}"

    def calc_gravitational_force(self, other):
        r_vector = other.position - self.position
        r_mag = vp.mag(r_vector)
        if r_mag > 0:
            force_mag = G * self.mass * other.mass / r_mag**2
            return force_mag * vp.norm(r_vector)
        return vp.vector(0,0,0)
    
    def update_force(self, all_objects):
        self.force = vp.vector(0,0,0)
        for body in all_objects:
            if body != self:
                self.force += self.calc_gravitational_force(body)
    
    def update_position(self):
        acceleration = self.force / self.mass
        self.velocity += acceleration * DT
        self.position += self.velocity * DT
        self.object.pos = self.position



# MOVE OBJECT FUNCTION

def enable_drag(body):
    dragging = None

    def on_mouse_down(event):
        nonlocal dragging
        clicked_objects = []

        for body in all_objects:
            if vp.mag(event.pos - body.object.pos) < body.object.radius:
                clicked_objects.append(body)

        if clicked_objects:
                dragging = max(clicked_objects, key=lambda b: b.object.radius)
                notebook.select(dragging.tab)       
                notebook.update_idletasks()
         
    
    def on_mouse_move(event):
        nonlocal dragging
        if dragging:
            new_position = vp.vector(event.pos.x, event.pos.y, dragging.object.pos.z)
            dragging.object.pos = new_position
            dragging.position = new_position

    def on_mouse_up(event):
        nonlocal dragging
        if dragging:
            dragging.initial_position = vp.vector(dragging.position)
            dragging.initial_velocity = vp.vector(dragging.velocity)
        dragging = None

    vp.scene.bind("mousedown", on_mouse_down)
    vp.scene.bind("mousemove", on_mouse_move)
    vp.scene.bind("mouseup", on_mouse_up)



# CREATE NEW OBJECT FUNCTION

def create_new_object():
    # new object tab
    new_object_tab = tk.Frame(notebook)
    notebook.add(new_object_tab, text="New Object")
    notebook.select(new_object_tab)

    main_frame = tk.Frame(new_object_tab)
    main_frame.pack(expand=True)

    # label text
    text1 = tk.Label(main_frame, text="Name your new object:", anchor="center", font=("", 15))
    text1.pack(pady=10, expand=True)

    # entry name
    entry_name = tk.Entry(main_frame, width=10)
    entry_name.pack(pady=(0,10), expand=True)
    entry_name.focus()
    
    text2 = tk.Label()

    def confirm_name(event):
        nonlocal text2
        object_name = entry_name.get().strip()

        if object_name in [obj.name for obj in all_objects]:
            if text2:
                text2.destroy()
            text2 = tk.Label(main_frame, text=f'You already have an object named "{object_name}".\nPlease rename it :)', anchor="center")
            text2.pack(expand=True)            

        else:
            text2.destroy()
            main_frame.destroy()

            notebook.tab(new_object_tab, text=object_name)
            text1.destroy()
            entry_name.destroy()

            # new object controls
            new_object = Body(object_name)

            new_object.tab = new_object_tab

            all_objects.append(new_object)
            text_number_planets.config(text=f"Number of celestial bodies: {len(all_objects)}")
            print(all_objects) # DEBUGGING

            update_texts()
            
            # enable drag
            enable_drag(new_object)


            # update values
            def update_mass(value):
                new_object.mass = float(value)
                print(f"Updated mass of {new_object.name}: {new_object.mass}") # DEBUGGING

            def update_radius(value):
                new_object.object.radius = float(value)
                print(f"Updated radius of {new_object.name}: {new_object.object.radius}") # DEBUGGING

            def update_velocity(value):
                new_object.velocity.y = float(value)
                print(f"Updated velocity of {new_object.name}: {new_object.velocity}") # DEBUGGING

            def update_color(event):
                selected_color = color_var.get()
                new_object.object.color = colors.get(selected_color, vp.color.white)
                print(f"Updated color of {new_object.name}: {selected_color}") # DEBUGGING


            # mass
            frame_mass = tk.Frame(new_object_tab)

            label_mass = tk.Label(frame_mass, text="Mass", width=5, anchor="w")
            label_mass.pack(side="left", expand=True, fill="both", padx=(20,0))

            scale_mass = tk.Scale(frame_mass, from_=1, to=500, orient=tk.HORIZONTAL, command=update_mass, troughcolor=rosita, font=("", 10))
            scale_mass.set(new_object.mass)  # Valor inicial
            scale_mass.pack(side="left", expand=True, padx=(0,20), fill="both")

            frame_mass.pack(expand=True, fill="both", pady=(20,0))

            # radius
            frame_radius = tk.Frame(new_object_tab)

            label_radius = tk.Label(frame_radius, text="Radius", width=5, anchor="w")
            label_radius.pack(side="left", expand=True, fill="both", padx=(20,0))

            scale_radius = tk.Scale(frame_radius, from_=1, to=10, orient=tk.HORIZONTAL, command=update_radius, troughcolor=rosita, font=("", 10))
            scale_radius.set(new_object.object.radius)
            scale_radius.pack(side="left", expand=True, padx=(0,20), fill="both")

            frame_radius.pack(expand=True, fill="both")

            # velocity
            frame_velocity = tk.Frame(new_object_tab)

            label_velocity = tk.Label(frame_velocity, text="Velocity", width=5, anchor="w")
            label_velocity.pack(side="left", expand=True, fill="both", padx=(20,0))

            scale_velocity = tk.Scale(frame_velocity, from_=-10, to=10, orient=tk.HORIZONTAL, command=update_velocity, troughcolor=rosita, font=("", 10))
            scale_velocity.set(new_object.velocity.y)
            scale_velocity.pack(side="left", expand=True, padx=(0,20), fill="both")

            frame_velocity.pack(expand=True, fill="both")

            # color
            frame_color = tk.Frame(new_object_tab)

            label_color = tk.Label(frame_color, text="Color", width=5, anchor="w")
            label_color.pack(side="left", expand=True, fill="both", padx=(20,0))

            color_var = tk.StringVar()
            color_selector = ttk.Combobox(frame_color, textvariable=color_var, state="readonly", width=9)
            color_selector["values"] = ("White", "Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Magenta")
            color_selector.current(0)
            color_selector.bind("<<ComboboxSelected>>", update_color)
            color_selector.pack(side="left", expand=True, padx=(0,20), fill="both")

            frame_color.pack(expand=True, fill="both", pady=(0,3))

            
            # delete button
            def delete_object():
                new_object.object.visible = False
                new_object.object.clear_trail()
                all_objects.remove(new_object)
                del new_object.object

                new_object_tab.destroy()
                print(all_objects) # DEBUGGING
                text_number_planets.config(text=f"Number of celestial bodies: {len(all_objects)}")

                update_texts()

            delete_button = tk.Button(new_object_tab, text="Delete", command=delete_object, activebackground=rosita)
            delete_button.pack(expand=True, pady=(0,10))

    entry_name.bind("<Return>", confirm_name)



# UPDATE CAMERA RANGE

def update_camera():
    max_distance = 10
    for obj in all_objects:
        distance = vp.mag(obj.position)
        if distance > max_distance:
            max_distance = distance
    vp.scene.range = max_distance + 10

    if max_distance >= 16:
        factor = vp.scene.range / 20
        paused_text.pos.y = -16 * factor
    else:
        paused_text.pos.y = -16



# RUN SIMULATION

def run_simulation():
    if simulation_running:
        vp.rate(500)
        for object in all_objects:
            object.object.make_trail = True
            object.update_force(all_objects)
            object.update_position()

        update_texts()
        update_camera()

        window.after(1, run_simulation)

def play_simulation():
    global simulation_running
    global all_objects
    if all_objects:
        if simulation_running == False:
            for obj in all_objects:
                obj.initial_velocity = obj.velocity
            simulation_running = True
            update_texts()
            run_simulation()

def pause_simulation():
    global simulation_running
    simulation_running = False
    update_texts()
    update_camera()

def restart_simulation():
    global simulation_running
    simulation_running = False
    for object in all_objects:
        object.object.clear_trail()
        object.position = vp.vector(object.initial_position.x, object.initial_position.y, object.initial_position.z)
        object.velocity = vp.vector(object.initial_velocity.x, object.initial_velocity.y, object.initial_velocity.z)

        object.object.pos = object.initial_position
        object.object.clear_trail()
        object.object.make_trail = False

    update_texts()
    update_camera()



# TKINTER GUI

window = tk.Tk()
window.title("Gravitational Systems Simulator")
window.geometry("375x375")
window.configure(bg=rosita)

# notebook widegt
notebook = ttk.Notebook(window)

# main menu
main_menu = tk.Frame(notebook)

# main menu: title
title = tk.Label(main_menu, text="ORBITS SIMULATOR", font=("", 25))
title.pack(fill="both", pady=(15,15), padx=15, expand=True)

# main menu: buttons
frame_buttons = tk.Frame(main_menu)

frame_play = tk.Frame(frame_buttons)
play = tk.PhotoImage(file="play.png")
button_play = tk.Button(frame_play, image=play, width=50, height=50, command=play_simulation)
button_play.pack(expand=True)
play_text = tk.Label(frame_play, text="Play")
play_text.pack(expand=True)
frame_play.pack(side="left", padx=5, pady=5, expand=True)

frame_pause = tk.Frame(frame_buttons)
pause = tk.PhotoImage(file="pause.png")
button_pause = tk.Button(frame_pause, image=pause, width=50, height=50, command=pause_simulation)
button_pause.pack(expand=True)
pause_text = tk.Label(frame_pause, text="Pause")
pause_text.pack(expand=True)
frame_pause.pack(side="left", padx=5, pady=5, expand=True)

frame_restart = tk.Frame(frame_buttons)
restart = tk.PhotoImage(file="restart.png")
button_restart = tk.Button(frame_restart, image=restart, width=50, height=50, command=restart_simulation)
button_restart.pack(expand=True)
restart_text = tk.Label(frame_restart, text="Restart")
restart_text.pack(expand=True)
frame_restart.pack(side="left", padx=5, pady=5, expand=True)

frame_buttons.pack(pady=(0,15))

# main menu: number of planets
frame_number_planets = tk.Frame(main_menu)

text_number_planets = tk.Label(frame_number_planets, text=f"Number of celestial bodies: {len(all_objects)}", font=("", 15))
text_number_planets.pack(expand=True)

frame_number_planets.pack(pady=(0,5), expand=True)

# main menu: add and delete planets
frame_add_delete = tk.Frame(main_menu)

mas = tk.PhotoImage(file="add.png")
button_mas = tk.Button(frame_add_delete, image=mas, width=50, height=50, command=create_new_object)
button_mas.pack(side="left", padx=5, pady=5, expand=True)

frame_add_delete.pack(pady=(0,10), expand=True)

notebook.add(main_menu, text="Main")

notebook.pack(padx=15, pady=15, expand=True, fill="both")

# run
window.mainloop()

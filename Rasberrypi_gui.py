# --- Import required libraries ---
try:
    # Import gpiozero if running on Raspberry Pi
    from gpiozero import LED
    real_hw = True  # Flag to indicate hardware is available
except Exception:
    # Create a mock LED class for testing without Raspberry Pi hardware
    class LED:
        def __init__(self, pin):
            self.pin = pin
            self.state = False

        def on(self):
            """Simulate turning the LED ON."""
            self.state = True
            print(f"[MOCK] LED {self.pin} ON")

        def off(self):
            """Simulate turning the LED OFF."""
            self.state = False
            print(f"[MOCK] LED {self.pin} OFF")

    real_hw = False  # Indicate that mock mode is active

import tkinter as tk  # GUI library

# --- GPIO pin definitions (BCM numbering) ---
LED1_PIN = 17
LED2_PIN = 27
LED3_PIN = 22

# --- Create LED objects ---
# These control the LEDs connected to the specified GPIO pins.
led1 = LED(LED1_PIN)
led2 = LED(LED2_PIN)
led3 = LED(LED3_PIN)


def set_leds(led_num):
    """
    Turn one LED ON and switch OFF the others.
    
    Args:
        led_num (str): The selected LED number ("1", "2", "3").
    """
    if led_num == "1":
        led1.on(); led2.off(); led3.off()
        status_label.config(text="LED 1 is ON")
    elif led_num == "2":
        led1.off(); led2.on(); led3.off()
        status_label.config(text="LED 2 is ON")
    elif led_num == "3":
        led1.off(); led2.off(); led3.on()
        status_label.config(text="LED 3 is ON")
    else:
        led1.off(); led2.off(); led3.off()
        status_label.config(text="All LEDs OFF")


def on_exit():
    """
    Safely turn off all LEDs and close the GUI window.
    """
    try:
        led1.off(); led2.off(); led3.off()
    except Exception:
        pass
    root.destroy()


# --- GUI setup ---
root = tk.Tk()
root.title("LED Control - Same Color")
root.geometry("420x220")
root.resizable(False, False)
root.config(padx=16, pady=12)

# --- Title Label ---
tk.Label(root, text="Choose an LED to turn ON:", font=("Arial", 12)).pack(anchor="w")

# --- Radio button setup ---
sel = tk.StringVar(value="none")
frame = tk.Frame(root)
frame.pack(pady=8, anchor="w")

def make_radio(text, val):
    """
    Helper function to create radio buttons for each LED option.
    
    Args:
        text (str): Label text for the button.
        val (str): Value associated with the button.
    """
    rb = tk.Radiobutton(frame, text=text, variable=sel, value=val,
                        command=lambda v=val: set_leds(v))
    rb.pack(side="left", padx=8)

# Create three radio buttons for three LEDs
make_radio("LED 1", "1")
make_radio("LED 2", "2")
make_radio("LED 3", "3")

# --- Status label ---
status_label = tk.Label(root, text="All LEDs OFF", font=("Arial", 10))
status_label.pack(pady=12)

# --- Exit button ---
exit_btn = tk.Button(root, text="Exit", command=on_exit, width=10, bg="orange")
exit_btn.pack(side="bottom", pady=8)

# --- Window close event handler ---
root.protocol("WM_DELETE_WINDOW", on_exit)

# --- Start GUI main loop ---
root.mainloop()

try:
    from gpiozero import LED
    real_hw = True
except Exception:
    # Mock LED for testing on non-Raspberry Pi machines
    class LED:
        def __init__(self, pin):
            self.pin = pin
            self.state = False

        def on(self):
            self.state = True
            print(f"[MOCK] LED {self.pin} ON")

        def off(self):
            self.state = False
            print(f"[MOCK] LED {self.pin} OFF")

    real_hw = False

import tkinter as tk

# --- GPIO pins (BCM numbering) ---
LED1_PIN = 17
LED2_PIN = 27
LED3_PIN = 22

# LED objects
led1 = LED(LED1_PIN)
led2 = LED(LED2_PIN)
led3 = LED(LED3_PIN)

def set_leds(led_num):
    """Turn one LED on, others off."""
    if led_num == "1":
        led1.on(); led2.off(); led3.off()
        status_label.config(text="LED 1 ON")
    elif led_num == "2":
        led1.off(); led2.on(); led3.off()
        status_label.config(text="LED 2 ON")
    elif led_num == "3":
        led1.off(); led2.off(); led3.on()
        status_label.config(text="LED 3 ON")
    else:
        led1.off(); led2.off(); led3.off()
        status_label.config(text="None")

def on_exit():
    """Turn all LEDs off and close the GUI."""
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

tk.Label(root, text="Choose an LED to turn ON:", font=("Arial", 12)).pack(anchor="w")

sel = tk.StringVar(value="none")
frame = tk.Frame(root)
frame.pack(pady=8, anchor="w")

def make_radio(text, val):
    rb = tk.Radiobutton(frame, text=text, variable=sel, value=val,
                        command=lambda v=val: set_leds(v))
    rb.pack(side="left", padx=8)

make_radio("LED 1", "1")
make_radio("LED 2", "2")
make_radio("LED 3", "3")

status_label = tk.Label(root, text="None", font=("Arial", 10))
status_label.pack(pady=12)

exit_btn = tk.Button(root, text="Exit", command=on_exit, width=10, bg="orange")
exit_btn.pack(side="bottom", pady=8)

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()

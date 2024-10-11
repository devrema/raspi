import machine
import time

# Initializing Watchdog timer with a 5-second timeout (5000 ms)
# The Watchdog Timer (WDT) will reset the system if not "fed" within 5 seconds.
wdt = machine.WDT(timeout=5000)

# LEDs initialized with PWM to control brightness
# Using PWM to control LED brightness instead of just ON/OFF
led_r = machine.PWM(machine.Pin(15), freq=1000)  # Red LED on pin 15
led_g = machine.PWM(machine.Pin(14), freq=1000)  # Green LED on pin 14
led_b = machine.PWM(machine.Pin(13), freq=1000)  # Blue LED on pin 13

# Pins for controlling projector and screen movement
# Pins are initialized as output to control relays or motors
projector_power = machine.Pin(8, machine.Pin.OUT)
projector_up = machine.Pin(9, machine.Pin.OUT)
projector_down = machine.Pin(10, machine.Pin.OUT)
screen_up = machine.Pin(12, machine.Pin.OUT)
screen_down = machine.Pin(11, machine.Pin.OUT)

# Initial states for projector and screen
status_pro = "up"  # Projector starts in "up" position
status_scr = "up"  # Screen starts in "up" position

# Movement times (in milliseconds)
# Define how long it takes for projector and screen to move up/down
pro_d = 2000  # Time to move projector down
scr_d = 3000  # Time to move screen down
pro_u = 2300  # Time to move projector up
scr_u = 3400  # Time to move screen up

# Switches to control projector and screen
switch1 = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Switch for projector
switch2 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Switch for screen

# Debouncing configuration to avoid multiple signals due to mechanical switch bounce
debounce_time = 200  # Time in milliseconds to ignore extra switch presses
last_switch1_time = 0  # Time when switch1 was last pressed
last_switch2_time = 0  # Time when switch2 was last pressed

# Testing the pins by turning them on briefly and then off
# This section ensures all output pins are correctly wired and functioning
projector_power.value(1)
time.sleep(0.3)
projector_up.value(1)
time.sleep(0.3)
projector_down.value(1)
time.sleep(0.3)
screen_up.value(1)
time.sleep(0.3)
screen_down.value(1)
time.sleep(0.5)
# Turning everything off after test
projector_power.value(0)
projector_up.value(0)
projector_down.value(0)
screen_up.value(0)
screen_down.value(0)

# Main loop controlling projector and screen based on switch inputs
while True:
    # Feed the Watchdog Timer in every loop iteration
    # This resets the Watchdog's countdown and prevents a system reset.
    wdt.feed()

    # Get the current time for use in debouncing and time-based logic
    current_time = time.ticks_ms()

    # --- Projector controls ---

    # Checking if switch1 is pressed and the projector is in the "up" state
    # Using debounce logic to avoid multiple signals from one press
    if switch1.value() == 1 and status_pro == "up" and time.ticks_diff(current_time, last_switch1_time) > debounce_time:
        last_switch1_time = current_time  # Update the time for debounce
        start_pro_down = time.ticks_ms()  # Record the start time for the downward movement
        projector_down.value(1)  # Start moving projector down
        projector_power.value(1)  # Turn on projector power
        status_pro = "move down"  # Update status to indicate projector is moving down
    
    # Stop projector movement after the specified time has passed
    elif status_pro == "move down" and time.ticks_diff(time.ticks_ms(), start_pro_down) >= pro_d:
        projector_down.value(0)  # Stop moving projector down
        status_pro = "down"  # Update status to indicate projector is down
    
    # Checking if switch1 is released and projector is in the "down" state
    # Using debounce logic to prevent multiple triggers from switch bouncing
    elif switch1.value() == 0 and status_pro == "down" and time.ticks_diff(current_time, last_switch1_time) > debounce_time:
        last_switch1_time = current_time  # Update debounce time
        start_pro_up = time.ticks_ms()  # Record start time for upward movement
        projector_power.value(0)  # Turn off projector power
        projector_up.value(1)  # Start moving projector up
        status_pro = "move up"  # Update status to indicate projector is moving up
    
    # Stop projector upward movement after the specified time has passed
    elif status_pro == "move up" and time.ticks_diff(time.ticks_ms(), start_pro_up) >= pro_u:
        projector_up.value(0)  # Stop moving projector up
        status_pro = "up"  # Update status to indicate projector is up
    
    # --- Screen controls ---
    
    # Checking if switch2 is pressed and the screen is in the "up" state
    # Debouncing to avoid multiple triggers
    if switch2.value() == 1 and status_scr == "up" and time.ticks_diff(current_time, last_switch2_time) > debounce_time:
        last_switch2_time = current_time  # Update debounce time
        start_scr_down = time.ticks_ms()  # Record start time for downward movement
        screen_down.value(1)  # Start moving screen down
        status_scr = "move down"  # Update status to indicate screen is moving down
    
    # Stop screen downward movement after the specified time has passed
    elif status_scr == "move down" and time.ticks_diff(time.ticks_ms(), start_scr_down) >= scr_d:
        screen_down.value(0)  # Stop moving screen down
        status_scr = "down"  # Update status to indicate screen is down
    
    # Checking if switch2 is released and screen is in the "down" state
    # Using debounce logic to avoid multiple triggers
    elif switch2.value() == 0 and status_scr == "down" and time.ticks_diff(current_time, last_switch2_time) > debounce_time:
        last_switch2_time = current_time  # Update debounce time
        start_scr_up = time.ticks_ms()  # Record start time for upward movement
        screen_up.value(1)  # Start moving screen up
        status_scr = "move up"  # Update status to indicate screen is moving up
    
    # Stop screen upward movement after the specified time has passed
    elif status_scr == "move up" and time.ticks_diff(time.ticks_ms(), start_scr_up) >= scr_u:
        screen_up.value(0)  # Stop moving screen up
        status_scr = "up"  # Update status to indicate screen is up
    
    # --- LED control based on projector status ---
    
    # Control LEDs based on the status of the projector
    if status_pro == "down":
        led_r.duty(1023)  # Red LED fully on when projector is down
        led_g.duty(0)     # Green LED off
        led_b.duty(0)     # Blue LED off
    elif status_pro == "up":
        led_r.duty(0)     # Red LED off when projector is up
        led_g.duty(1023)  # Green LED fully on when projector is up
        led_b.duty(0)     # Blue LED off
    
    # --- LED control based on screen status ---
    
    # Blue LED turns on when the screen is down, off when it's up
    if status_scr == "down":
        led_b.duty(1023)  # Blue LED fully on when screen is down
    else:
        led_b.duty(0)     # Blue LED off when screen is up
    
    time.sleep(0.05)  # Short delay to reduce CPU usage

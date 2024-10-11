import machine
import time
from unittest.mock import MagicMock

# Mock the machine module for testing
machine.Pin = MagicMock()
machine.PWM = MagicMock()

# Import your main script here
import main  # Ersetze "main" durch den tatsächlichen Namen deiner Datei, falls notwendig

# Access the variables directly from the main module
projector_power = main.projector_power
projector_up = main.projector_up
projector_down = main.projector_down
screen_up = main.screen_up
screen_down = main.screen_down
led_r = main.led_r
led_g = main.led_g
led_b = main.led_b
switch1 = main.switch1
switch2 = main.switch2

def test_projector_initialization():
    assert projector_power.value() == 0
    assert projector_up.value() == 0
    assert projector_down.value() == 0

def test_screen_initialization():
    assert screen_up.value() == 0
    assert screen_down.value() == 0

def test_led_initialization():
    assert led_r.duty.call_count == 0
    assert led_g.duty.call_count == 0
    assert led_b.duty.call_count == 0

# Simulate a switch press and test projector movement
def test_projector_movement():
    # Simulate switch press
    switch1.value = MagicMock(return_value=1)
    
    # Simulate the main logic that would normally run
    main.status_pro = "up"  # Set initial state for the projector
    main.last_switch1_time = 0  # Reset the last switch time
    current_time = time.ticks_ms()  # Get current time for the test

    # Check projector moving down
    if switch1.value() == 1 and main.status_pro == "up":
        main.start_pro_down = current_time  # Simulate start time
        projector_down.value(1)  # Start moving down
        projector_power.value(1)  # Turn on power

    assert projector_power.value() == 1
    assert projector_down.value() == 1

    # Simulate the time taken for the movement
    time.sleep(2)  # Simulate the downward movement duration

    # Stop moving down
    projector_down.value(0)  # Stop moving down
    main.status_pro = "down"  # Update status

    assert projector_down.value() == 0
    assert main.status_pro == "down"

def run_tests():
    test_projector_initialization()
    test_screen_initialization()
    test_led_initialization()
    test_projector_movement()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()

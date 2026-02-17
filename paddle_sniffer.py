#!/usr/bin/env python3
import can
import time
import sys

print("Initializing CAN bus connection...")
try:
    bus = can.interface.Bus(channel='can0', interface='socketcan')
    print("✓ CAN bus connected successfully")
except OSError as e:
    print(f"✗ ERROR: Cannot connect to CAN bus - {e}")
    print("  This is normal if not connected to the car.")
    print("  Make sure the car is on and openpilot is running.")
    sys.exit(1)

prev_296 = None  # SCM_BUTTONS
prev_1a4 = None  # GEARBOX_AUTO (0x1a4 = 420 decimal)

print("\nMonitoring for paddle presses... Press Ctrl+C to stop")
print("Available message IDs:")
print("  0x296 (662) = SCM_BUTTONS")
print("  0x1a4 (420) = GEARBOX_AUTO (contains REGEN_STAGE_SELECTION)")
print("-" * 60)

try:
    while True:
        msg = bus.recv(timeout=0.01)
        if msg is None:
            continue

        # SCM_BUTTONS (0x296)
        if msg.arbitration_id == 0x296:
            if prev_296 != msg.data:
                print(f"[SCM_BUTTONS 0x296] {msg.data.hex()}")
                prev_296 = msg.data

        # GEARBOX_AUTO (0x1a4) - contains REGEN_STAGE_SELECTION
        if msg.arbitration_id == 0x1a4:
            if prev_1a4 != msg.data:
                print(f"[GEARBOX_AUTO 0x1a4] {msg.data.hex()}")
                print(f"  *** Did you just press a paddle? ***")
                prev_1a4 = msg.data

except KeyboardInterrupt:
    print("\n\nStopped by user")
    sys.exit(0)

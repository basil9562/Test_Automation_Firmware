import serial
import serial.tools.list_ports
import time

BAUDRATE = 9600
TIMEOUT = 1

expected_boot_lines = [
    "========== BOOT INFO ==========",
    "Firmware Version: 1.2",
    "System initialized successfully.",
    "================================"
]

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description or "ttyUSB" in port.device:
            return port.device
    return None

def read_serial_lines(ser, max_lines=50, timeout=5):
    lines = []
    start = time.time()
    while time.time() - start < timeout:
        while ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                lines.append(line)
        time.sleep(0.1)
    return lines

def wait_for_boot(ser):
    print("🔌 Waiting for Arduino boot info...")
    boot_output = read_serial_lines(ser)
    print("\n📥 Boot Output:")
    for line in boot_output:
        print("→", line)

    for expected in expected_boot_lines:
        if not any(expected in line for line in boot_output):
            print(f"❌ Missing: {expected}")
            return False
    print("✅ Boot Info validated.\n")
    return True

def send_command(ser, cmd):
    ser.write((cmd + "\n").encode('utf-8'))
    time.sleep(0.5)
    response = read_serial_lines(ser, max_lines=5, timeout=1)
    for line in response:
        print("→", line)
    return response

def automated_led_loop(ser):
    while True:
        print("🟢 Sending LED ON command...")
        send_command(ser, "LED ON")
        time.sleep(5)

        print("🔴 Sending LED OFF command...")
        send_command(ser, "LED OFF")
        time.sleep(10)

def main():
    print("🔁 Looking for Arduino. Press Ctrl+C to exit.")
    connected = False
    ser = None

    while True:
        try:
            if not connected:
                port = find_arduino_port()
                if port:
                    print(f"✅ Arduino found on {port}")
                    ser = serial.Serial(port, BAUDRATE, timeout=TIMEOUT)
                    time.sleep(2)
                    if wait_for_boot(ser):
                        connected = True
                        print("🚦 Starting LED automation...\n")
                else:
                    print("🔍 Arduino not found. Retrying...")
                    time.sleep(2)
            else:
                automated_led_loop(ser)
        except serial.SerialException:
            print("❌ Arduino disconnected. Reconnecting...")
            connected = False
            if ser:
                ser.close()
            time.sleep(2)
        except KeyboardInterrupt:
            print("🛑 Exiting program.")
            if ser:
                ser.close()
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()

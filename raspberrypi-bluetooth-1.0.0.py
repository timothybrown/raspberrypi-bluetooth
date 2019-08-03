#!/usr/bin/env python3

"""
********************************************************************************
Raspberrypi Bluetooth Helper v1.0.0 for Arch Linux ARM
(C) 2018-2019 @TimothyBrown - MIT License
--------------------------------------------------------------------------------
Attempts to determine the correct patchram firmware to use and loads it using.
the btattach tool. This enables the built-in Bluetooth of a Raspberry Pi 3B/3B+
without using legacy Bluez tools.
********************************************************************************
"""

import sys, subprocess, shutil
from socket import gethostname
from time import sleep
from pathlib import Path
from systemd import daemon
from rpinfo import RaspberryPi

### raspberrypi-bluetooth
## Setup and Verify:
# Verify we're running on a Raspberry Pi.
rpi = RaspberryPi()
if rpi.model not in ['3B', '3B+']:
    sys.stdout.write(f"Not running on a compatible Raspberry Pi model (3B, 3B+). Aborting!\n")
    sys.stdout.flush()
    sys.exit(1)
# Setup and verify firmware file paths.
firmware = {'BCM43430': Path('/usr/lib/firmware/updates/brcm/BCM43430A1.hcd'), 'BCM4345': Path('/usr/lib/firmware/updates/brcm/BCM4345C0.hcd')}
for fw_name, fw_path in firmware.items():
    if not fw_path.is_file():
        sys.stdout.write(f"Unable to locate firmware file {fw_name}. Aborting!\n")
        sys.stdout.flush()
        sys.exit(1)
# Setup and verify btattach binary path.
btattach_bin = Path(shutil.which('btattach'))
if not btattach_bin.exists():
    sys.stdout.write(f"Unable to locate btattach binary. Aborting!\n")
    sys.stdout.flush()
    sys.exit(1)
# Setup and verify UART device tree enteies.
uart0 = Path('/proc/device-tree/aliases/uart0')
serial1 = Path('/proc/device-tree/aliases/serial1')
if not uart0.is_file() or not serial1.is_file():
    sys.stdout.write(f"Unable to locate UART entries in Device Tree. Aborting!\n")
    sys.stdout.flush()
    sys.exit(1)
# Setup HCI device path.
for i in range(10):
    hci = Path(f'/sys/class/bluetooth/hci{i}')
    if not hci.exists(): break
    else: hci = None
if hci is None:
    sys.stdout.write("Unable to find free HCI slot. Aborting!\n")
    sys.stdout.flush()
    sys.exit(1)
# Table to hold the settings for the various configurations.
# True = BT on PL011, False = BT on mini UART.
bluetooth_table = {
                   True:  {
                           '3B+': {
                                   'radio'    : 'BCM4345',
                                   'uart_name': 'PL011',
                                   'uart_dev' : Path('/dev/ttyAMA0'),
                                   'uart_baud': '3000000',
                                  },
                           '3B': {
                                   'radio'    : 'BCM43430',
                                   'uart_name': 'PL011',
                                   'uart_dev' : Path('/dev/ttyAMA0'),
                                   'uart_baud': '921600',
                                  }
                          },
                   False: {
                           '3B+': {
                                   'radio'    : 'BCM4345',
                                   'uart_name': 'mini UART',
                                   'uart_dev' : Path('/dev/ttyS0'),
                                   'uart_baud': '460800',
                                  },
                           '3B':  {
                                   'radio'    : 'BCM43430',
                                   'uart_name': 'mini UART',
                                   'uart_dev' : Path('/dev/ttyS0'),
                                   'uart_baud': '460800',
                                  }
                          }
                  }
# Decode Bluetooth MAC from the RPi serial number.
bluetooth_mac = ':'.join([f'{i:02x}'.upper() for i in [0xB8, 0x27, 0xEB, int(rpi.serial[2:4], 16)^0xAA, int(rpi.serial[4:6], 16)^0xAA, int(rpi.serial[6:8], 16)^0xAA]])
# Grab bluetooth settings from the table. We do this by comparing the text returned from the
# uart0 and serial1 device-tree entries. If they're the same then the BT is on the PL011, if not
# we're using the mini UART.
settings = bluetooth_table[uart0.read_text() == serial1.read_text()][rpi.model]
# Verify UART device.
if not settings['uart_dev'].is_char_device():
    sys.stdout.write(f"Device {settings['uart_name']} not available. Aborting!\n")
    sys.stdout.flush()
    sys.exit(1)
# It's time to setup the controller!
sys.stdout.write(f"{settings['radio']} Controller {bluetooth_mac} on {settings['uart_name']} at {int(settings['uart_baud'])/1000}k\n")
sys.stdout.flush()
sleep(1)
# Put together the command string and start btattach.
# -P bcm = Select the Broadcom protocol.
# -S <baud> = Set the baud rate for our chipset and UART.
# -B <device> = Attach a primary controller to this serial device.
btattach_cmd = [
    btattach_bin,
    '-P', 'bcm',
    '-S', settings['uart_baud'],
    '-B', settings['uart_dev']
]
btattach = subprocess.Popen(btattach_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# Wait for firmware upload to complete and the HCI device to attach.
for i in range(10):
    if not hci.is_symlink(): sleep(1)
    else: break
if not hci.is_symlink():
    sys.stdout.write(f"Failed to attach {hci.name}. Aborting!\n")
    sys.stdout.flush()
    btattach.terminate()
    sys.exit(1)
# Log our status, notify systemd and exit; leave btattach running to manage the HCI port.
sys.stdout.write(f"Raspberry Pi {rpi.model} Bluetooth on {hci.name} is ready.\n")
sys.stdout.flush()
if daemon.booted():
    daemon.notify("READY=1")
    daemon.notify(f"STATUS=Raspberry Pi {rpi.model} Bluetooth on {hci.name} is ready.")
sys.exit(0)
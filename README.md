# raspberrypi-bluetooth 1.0.0-2 (2019.08.04)
Provides Bluetooth support for Raspberry Pi 3B/3B+/ZeroW without using legacy Bluez tools.

## About
This package provides a Python helper script that determines the chipset (BCM43430/BCM4345) and UART
(PL011/mini UART) of the installed Bluetooth adapter. That information is used to launch `btattach`
(from the `bluez-utils` package), which then takes care of loading the firmware and bringing up the
HCI interface.

To determine the correct chipset we use a custom Python library that decodes the Raspberry Pi's serial
number. The correct UART is determined by examing device tree entries for the two serial ports in the
exact same manner as the official shell script that ships with Raspbian.

The python helper script does *not* stay running. It simply hands off the information to `btattach`
(which *does* stay running) before terminating, so it won't use up any additional system resources.

Also included is a corrosponding systemd service file. It is set to run *before* the Bluez service
and will take care of bringing the rest of the Bluetooth system up by itself.

Please file a bug report if you run into problems. (I've been using this on three Pis for about six
months with no issues, so I figured it was time for a proper release!)

## Install
```
git clone https://github.com/timothybrown/raspberrypi-bluetooth.git
cd raspberrypi-bluetooth
makepkg -si
sudo systemctl enable raspberrypi-bluetooth
sudo reboot
```
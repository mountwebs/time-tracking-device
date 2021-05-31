
"""
Connect by BLEDevice
"""

import asyncio
import platform

temperature_uuid = "00002a6e-0000-1000-8000-00805f9b34fb"

from bleak import BleakClient, BleakScanner


async def print_services(mac_addr: str):
    device = await BleakScanner.find_device_by_address(mac_addr)
    async with BleakClient(device) as client:
        try:
          temp = await client.read_gatt_char(temperature_uuid)
          temp = int.from_bytes(bytes(temp), "little")
          print(temp)
        except Exception as e:
          print(e)


mac_addr = (
    "FC:F5:C4:05:31:0A"
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
)
loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(mac_addr))
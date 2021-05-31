
"""
Connect by BLEDevice
"""

import asyncio
import platform

from bleak import BleakClient, BleakScanner


async def print_services(mac_addr: str):
    device = await BleakScanner.find_device_by_address(mac_addr)
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


mac_addr = (
    "FC:F5:C4:05:31:0A"
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
)
loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(mac_addr))
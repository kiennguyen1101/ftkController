import wmi
import traceback
import time
start_time = time.time()

c = wmi.WMI()
sector_size = 512
usb = ''
for physical_disk in c.Win32_DiskDrive ():
    if 'Removable' in physical_disk.MediaType:
        usb = physical_disk

# with open(usb.DeviceID,'rb') as f:
#     with open("C:/test/test.dd", "wb") as i:
#         while True:
#             if i.write(f.read(512)) == 0:
#                 break
# print("--- %s seconds ---" % (time.time() - start_time))
import wmi
c = wmi.WMI ()

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

possible_drives = [
        r"\\.\PhysicalDrive1", # Windows
        r"\\.\PhysicalDrive2",
        r"\\.\PhysicalDrive3",
        "/dev/mmcblk0", # Linux - MMC
        "/dev/mmcblk1",
        "/dev/mmcblk2",
        "/dev/sdb", # Linux - Disk
        "/dev/sdc",
        "/dev/sdd",
        "/dev/disk1", #MacOSX
        "/dev/disk2",
        "/dev/disk3",
        ]

for physical_disk in c.Win32_DiskDrive ():
    if 'Removable' in physical_disk.MediaType:
        print(physical_disk)

#for physical_disk in c.Win32_DiskDrive ():
    #for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
        #print partition
        #for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
            ## print logical_disk
            #if logical_disk.DriveType is 2:
                #print logical_disk.Caption

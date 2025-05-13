import wmi
import psutil
import platform
import os
w = wmi.WMI()

ddr_map = {
    20: "DDR",
    21: "DDR2",
    22: "DDR2 FB-DIMM",
    24: "DDR3",
    26: "DDR4",
    34: "DDR5"
}

class CPU:
    def __init__(self):
        self.name = w.Win32_Processor()[0].Name
        self.cores = psutil.cpu_count(logical=False)
        self.threads = psutil.cpu_count(logical=True)
        
    def get_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_speed(self):
          speed = psutil.cpu_freq().current / 1000  
          return speed
        

class GPU:
    def __init__(self):
        self.gpus = []
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            if 'Intel' in gpu.Name or 'HD Graphics' in gpu.Name:
                vram = 0 
            else:
                vram = int(gpu.AdapterRAM) / (1024**3) 
            gpu_info = {
                "name": gpu.Name,
                "vram": vram if vram > 0 else 0
            }
            self.gpus.append(gpu_info)
            
            
class Memory:
    def __init__(self):
        self.sticks = []
        for mem in w.Win32_PhysicalMemory():
            size_gb = int(mem.Capacity) / (1024**3)
            mem_type_code = getattr(mem, 'SMBIOSMemoryType', 0)
            mem_type = ddr_map.get(mem_type_code, f"Unknown ({mem_type_code})")
            
            self.sticks.append({
                "size_gb": round(size_gb, 1),
                "type": mem_type
            })

class Disk:
    def __init__(self):
        self.disks = []
        w = wmi.WMI()
        for disk in w.Win32_LogicalDisk(DriveType=3):  
            free_gb = int(disk.FreeSpace) / (1024**3) 
            size_gb = int(disk.Size) / (1024**3) 
            disk_info = {
                "name": disk.DeviceID,  
                "size_gb": round(size_gb, 1),
                "free_gb": round(free_gb, 1),
            }
            self.disks.append(disk_info)

def get_os():
    windows_info = {
        "os": platform.system(),  
        "version": platform.version(),  
        "release": platform.release(),  
        "arch": platform.architecture()[0],  
        "computer": platform.node(), 
        "current_user": os.getlogin(),
    }
    return windows_info
import psutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    total_memory = round(memory_info.total / (1024 ** 3), 2)  # GB
    used_memory = round(memory_info.used / (1024 ** 3), 2)    # GB
    memory_usage_percent = memory_info.percent

    disk_info = psutil.disk_usage('/')
    total_disk = round(disk_info.total / (1024 ** 3), 2)      # GB
    used_disk = round(disk_info.used / (1024 ** 3), 2)        # GB
    disk_usage_percent = disk_info.percent

    return {
        "cpu_usage": cpu_usage,
        "total_memory": total_memory,
        "used_memory": used_memory,
        "memory_usage_percent": memory_usage_percent,
        "total_disk": total_disk,
        "used_disk": used_disk,
        "disk_usage_percent": disk_usage_percent
    }



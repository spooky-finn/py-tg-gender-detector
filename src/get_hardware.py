import psutil
import platform
import uuid

def getHardwareData():
    def get_size(bytes, suffix="B"): 
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    uname = platform.uname()
    return {
        "machine"      : uname.machine,
        "cpu"      : uname.processor,
        "node_name"     : uname.node,
        "physical_cores" : psutil.cpu_count(logical=False),
        "ram"          : get_size(psutil.virtual_memory().total),
        "uuids"         : hex(uuid.getnode())
    }
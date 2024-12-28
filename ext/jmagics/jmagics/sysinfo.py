import platform
import cpuinfo
import GPUtil
import psutil

from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, line_magic


cpu_info = cpuinfo.get_cpu_info()
gpus = GPUtil.getGPUs()

@magics_class
class SysInfoMagics(Magics):
    @line_magic
    def print_sysinfo(self, _=None):
        print("System Information:")
        print("-------------------")

        print("Processor:", cpu_info.get('brand_raw', 'N/A'))
        print("Architecture:", cpu_info.get('arch', 'N/A'))
        print("Bits:", cpu_info.get('bits', 'N/A'))
        print("Uname:", cpu_info.get('uname_string', platform.system()))

        print("Cores (Logical):", psutil.cpu_count(logical=True))
        print("Cores (Physical):", psutil.cpu_count(logical=False))

        ram = psutil.virtual_memory()
        print("Total RAM:", round(ram.total / (1024**3), 2), "GB")

        for gpu in gpus:
            print(f"GPU {gpu.id} Name: {gpu.name}")
            print(f"GPU {gpu.id} Total Memory: {gpu.memoryTotal} MB")


# Register the magic with IPython
ip = get_ipython()
sysinfo_magics = SysInfoMagics(shell=ip)
ip.register_magics(sysinfo_magics)

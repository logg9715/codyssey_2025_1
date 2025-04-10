import platform
import os
import json


class MissionComputer:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        settings = {
            'operating_system': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_core_count': True,
            'memory_size': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True
        }

        try:
            # 현재 파이썬 파일(mars_mission_computer.py) 기준 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            setting_path = os.path.join(current_dir, 'setting.txt')

            with open(setting_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().lower()
                        settings[key] = (value == 'true')
        except FileNotFoundError:
            pass  # 기본값 사용

        return settings

    def get_mission_computer_info(self):
        try:
            info = {}
            if self.settings.get('operating_system'):
                info['operating_system'] = platform.system()
            if self.settings.get('os_version'):
                info['os_version'] = platform.version()
            if self.settings.get('cpu_type'):
                info['cpu_type'] = platform.processor()
            if self.settings.get('cpu_core_count'):
                info['cpu_core_count'] = os.cpu_count()
            if self.settings.get('memory_size'):
                info['memory_size'] = self._get_memory_size()
        except Exception as e:
            info = {'error': str(e)}

        print(json.dumps(info, indent=4))
        return info

    def get_mission_computer_load(self):
        try:
            load = {}
            if self.settings.get('cpu_usage_percent'):
                load['cpu_usage_percent'] = self._get_cpu_usage()
            if self.settings.get('memory_usage_percent'):
                load['memory_usage_percent'] = self._get_memory_usage()
        except Exception as e:
            load = {'error': str(e)}

        print(json.dumps(load, indent=4))
        return load

    def _get_memory_size(self):
        try:
            if platform.system() == 'Windows':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                class MEMORYSTATUS(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_uint),
                        ('dwMemoryLoad', ctypes.c_uint),
                        ('dwTotalPhys', ctypes.c_size_t),
                        ('dwAvailPhys', ctypes.c_size_t),
                        ('dwTotalPageFile', ctypes.c_size_t),
                        ('dwAvailPageFile', ctypes.c_size_t),
                        ('dwTotalVirtual', ctypes.c_size_t),
                        ('dwAvailVirtual', ctypes.c_size_t),
                    ]
                memory_status = MEMORYSTATUS()
                memory_status.dwLength = ctypes.sizeof(MEMORYSTATUS)
                kernel32.GlobalMemoryStatus(ctypes.byref(memory_status))
                return memory_status.dwTotalPhys // (1024 ** 2)  # MB
            elif platform.system() == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            return int(line.split()[1]) // 1024  # kB to MB
            else:
                return 'Unsupported OS'
        except Exception as e:
            return str(e)

    def _get_memory_usage(self):
        try:
            if platform.system() == 'Linux':
                mem_total = 0
                mem_available = 0
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            mem_total = int(line.split()[1])
                        elif 'MemAvailable' in line:
                            mem_available = int(line.split()[1])
                if mem_total:
                    usage = ((mem_total - mem_available) / mem_total) * 100
                    return round(usage, 2)
            elif platform.system() == 'Windows':
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]
                memoryStatus = MEMORYSTATUSEX()
                memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
                return memoryStatus.dwMemoryLoad
            else:
                return 'Unsupported OS'
        except Exception as e:
            return str(e)

    def _get_cpu_usage(self):
        try:
            if platform.system() == 'Linux':
                with open('/proc/stat', 'r') as f:
                    fields = f.readline().split()[1:]
                    fields = list(map(int, fields))
                    idle_time = fields[3]
                    total_time = sum(fields)
                    import time
                    time.sleep(0.1)
                    with open('/proc/stat', 'r') as f2:
                        fields2 = f2.readline().split()[1:]
                        fields2 = list(map(int, fields2))
                        idle_time2 = fields2[3]
                        total_time2 = sum(fields2)

                    idle_delta = idle_time2 - idle_time
                    total_delta = total_time2 - total_time

                    usage = (1.0 - (idle_delta / total_delta)) * 100.0
                    return round(usage, 2)
            elif platform.system() == 'Windows':
                return '지원 안 함'
            else:
                return 'Unsupported OS'
        except Exception as e:
            return str(e)


# 인스턴스화 및 테스트 실행
if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

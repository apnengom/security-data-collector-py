import psutil

class cleaner:
    def __init__(self, pids_permitidos):
        self.pids = pids_permitidos
        self.eliminados = 0
        
    def clean(self):
        for pid in list(self.pids):
            try:
                p = psutil.Process(pid)
                p.terminate()
                p.wait(3)
                self.eliminados += 1
                self.pids.remove(pid)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                self.pids.remove(pid)


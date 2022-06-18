import pynvim
import psutil
import win32process
import win32gui
import win32con

def topWindowByPid(pidChk):
    def topWindowByPid_wrap(hwnd, top_windows):
        pid = win32process.GetWindowThreadProcessId(hwnd)[-1]
        if pid == pidChk:
            if win32gui.GetParent(hwnd) == 0:
                top_windows.append(hwnd)
    return topWindowByPid_wrap

@pynvim.plugin
class RaiseWindow(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("RaiseWindow")
    def raiseWindow(self, args):
        try:
            top_windows = []
            nvimPid = self.nvim.funcs.getpid()
            nvimQtPid = psutil.Process(nvimPid).ppid()
            win32gui.EnumWindows(topWindowByPid(nvimQtPid), top_windows)
            fore = win32gui.GetForegroundWindow()
            if top_windows:
                hwnd = top_windows[0]
                if hwnd != fore:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE) # Minimize
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) # Un-minimize
        except Exception as e:
            self.nvim.command('echom ""'.format(e))



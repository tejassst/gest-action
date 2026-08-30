import os
import subprocess
import platform

class ActionMapper:
    def __init__(self):
        self.platform = self.check_platform()
        self.linux_environ = None
        self.gesture_actions = self.action_mapping()

    def check_platform(self):
        os_name = platform.system()
        if os_name == "Darwin":
            return "MacOS"
        elif os_name == "Linux":
            return "Linux"
        else:
            print("Other OS")
            return ""

    def action_mapping(self):
        gesture_actions = {}
        if self.platform == "Linux":
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
            session = os.environ.get("XDG_SESSION_DESKTOP", "")
            if "HYPRLAND" in desktop or "hyprland" in session.lower():
                self.linux_environ = "Hyprland"
                gesture_actions = {
                    0: lambda: subprocess.run(["hyprctl", "dispatch", "exec", "kitty"]),
                    1: lambda: subprocess.run(["hyprctl", "dispatch", "workspace 1"]),
                    2: lambda: subprocess.run(["hyprctl", "dispatch", "workspace 2"]),
                    3: lambda: subprocess.run(["hyprctl", "dispatch", "exec", "nautilus"]),
                    4: lambda: subprocess.run(["hyprctl", "dispatch", "movetoworkspace", "+1"]),
                    5: lambda: subprocess.run(["hyprctl", "dispatch", "movetoworkspace", "-1"]),
                    6: lambda: subprocess.run(["hyprctl","dispatch", "cyclenext"]),
                    7: lambda: subprocess.run('grim -g "$(slurp)" - | wl-copy', shell=True),
                    8: lambda: subprocess.run(["hyprctl", "dispatch", "killactive"]),
                }
            elif "GNOME" in desktop or "gnome" in session.lower():
                self.linux_environ = "Gnome"
                gesture_actions = {
                    0: lambda: subprocess.run(["gnome-terminal"]),
                    1: lambda: subprocess.run(["xdotool","key","Super+1"]),
                    2: lambda: subprocess.run(["xdotool","key","Super+2"]),
                    3: lambda: subprocess.run(["xdotool","key","Super+3"]),
                    4: lambda: subprocess.run(["xdotool","key","Ctrl+Alt+Right"]),
                    5: lambda: subprocess.run(["xdotool","key","Ctrl+Alt+Left"]),
                    6: lambda: subprocess.run(["xdotool","key","Alt+Tab"]),
                    7: lambda: subprocess.run(["gnome-screenshot","-a","-c"]),
                    8: lambda: subprocess.run(["xdotool","key","Alt+F4"]),
                }
        elif self.platform == "MacOS":
            self.linux_environ = None
            gesture_actions = {
                0: lambda: subprocess.run(["open","-a","Terminal"]),
                1: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 18 using command down']),
                2: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 19 using command down']),
                3: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 20 using command down']),
                4: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 124 using control down']),
                5: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 123 using control down']),
                6: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to key code 48 using command down']),
                7: lambda: subprocess.run(["screencapture","-i","-c"]),
                8: lambda: subprocess.run(["osascript","-e",'tell application "System Events" to keystroke "w" using command down'])
            }
        else:
            print("Sorry, this application is not available on your desktop environment yet.")
        return gesture_actions

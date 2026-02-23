import os
import subprocess

gesture_actions = {
    0: lambda: subprocess.run(["hyprctl", "dispatch", "exec", "kitty"]),
    1: lambda: subprocess.run(["hyprctl", "dispatch", "workspace 1"]),
    2: lambda: subprocess.run(["hyprctl", "dispatch", "workspace 2"]),
    3: lambda: subprocess.run(["hyprctl", "dispatch", "workspace 3"]),
    4: lambda: subprocess.run(["hyprctl", "dispatch", "movetoworkspace", "+1"]),
    5: lambda: subprocess.run(["hyprctl", "dispatch", "movetoworkspace", "-1"]),
    6: lambda: subprocess.run(["hyprctl","dispatch", "cyclenext"]),
    7: lambda: subprocess.run(["hyprctl", "dispatch", "exec", "gthumb -f ~/Documents/heisenberg.gif"]),
    8: lambda: subprocess.run(["hyprctl", "dispatch", "killactive"]),
}
import subprocess
import keyboard
import sys

EXIT_KEY = 'end'

def launch_macro_script():
    macro_process = subprocess.Popen(['python', 'macro.py'])
    return macro_process

def emergency_exit(process):
    print('Emergency exit triggered')
    process.terminate()  # Terminate the subprocess
    sys.exit()  # Terminate the main script

# Launch the macro script in a subprocess
macro_process = launch_macro_script()

# Register a hotkey for emergency exit
keyboard.add_hotkey(EXIT_KEY, lambda: emergency_exit(macro_process))

# Wait for the macro process to complete
macro_process.wait()
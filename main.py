import keyboard
import time

# Global variables
RECORD_KEY = 'insert'
PLAY_KEY = 'delete'
EXIT_KEY = 'end'
RECORDINGS_FILE = 'recordings.txt'

is_recording = False
recorded_keys = []

def record_key(event):
  global is_recording, recorded_keys

  if is_recording:
    key = event.name
    event_time = event.time
    if (key == RECORD_KEY or key == PLAY_KEY or key == EXIT_KEY):
      return
    recorded_keys.append((key, event_time, event.event_type))
    print('Recorded:', key, 'Event Type:', event.event_type)


def play_back_keys():
  previous_time = None
  for key, event_time, event_type in recorded_keys:
    print('Playing:', key, event_type, event_time)
    if previous_time:
      delay = event_time - previous_time
      time.sleep(delay)  # Convert delay to seconds and introduce a delay
    if event_type == 'down':
      keyboard.press(key)
    elif event_type == 'up':
      keyboard.release(key)
    previous_time = event_time

def toggle_recording():
  global is_recording, recorded_keys
  if (not is_recording):
    recorded_keys = []
  is_recording = not is_recording
  print('Recording:', is_recording)

def emergency_exit():
  print('Emergency exit triggered')
  keyboard.unhook_all()  # Unhook all keyboard listeners
  raise SystemExit  # Terminate the script

def save_recordings(filename):
    with open(filename, 'w') as file:
        for key,  event_time, event_type in recorded_keys:
            file.write(f'{key},{event_time},{event_type}\n')
    print('Recordings saved to file:', filename)

def load_recordings(filename):
    global recorded_keys
    recorded_keys = []
    with open(filename, 'r') as file:
        for line in file:
            key, event_time, event_type = line.strip().split(',')
            recorded_keys.append((key, float(event_time), event_type))
    print('Recordings loaded from file:', filename)

# Register a hotkey to toggle recording
keyboard.add_hotkey(RECORD_KEY, toggle_recording)

# Register a hotkey to play back recorded keys
keyboard.add_hotkey(PLAY_KEY, play_back_keys)

keyboard.add_hotkey(EXIT_KEY, emergency_exit)

# Register a hotkey to save recordings
keyboard.add_hotkey('Ctrl+Shift+S', lambda: save_recordings(RECORDINGS_FILE))

# Register a hotkey to load recordings
keyboard.add_hotkey('Ctrl+Shift+L', lambda: load_recordings(RECORDINGS_FILE))

# Register a listener for both key press and key release events
keyboard.hook(record_key)

# Start the keyboard event listener
keyboard.wait()
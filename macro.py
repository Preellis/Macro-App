import keyboard
import time

# Global variables
RECORD_KEY = 'insert'
PLAY_KEY = 'delete'
RECORDINGS_FILE = 'recordings.txt'

is_recording = False
recorded_keys = []
start_time = None

def record_key(event):
  global is_recording, recorded_keys

  if is_recording:
    key = event.name
    event_time = event.time - start_time
    if (key == RECORD_KEY or key == PLAY_KEY):
      return
    recorded_keys.append((key, event_time, event.event_type))
    print('Recorded:', key, 'Event Type:', event.event_type)


def play_back_keys():
  play_back_start_time = time.time()
  for key, event_time, event_type in recorded_keys:
    print('Playing:', key, event_type, event_time)
    while (time.time() - play_back_start_time < event_time):
      pass
    if event_type == 'down':
      keyboard.press(key)
    elif event_type == 'up':
      keyboard.release(key)

def toggle_recording():
  global is_recording, recorded_keys, start_time
  if (not is_recording):
    start_time = time.time()
    recorded_keys = []
  is_recording = not is_recording
  print('Recording:', is_recording)

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
            split_line = line.strip().split(',')
            if (len(split_line) != 3):
              key = ','
              event_time = split_line[2]
              event_type = split_line[3]
            else:
              key, event_time, event_type = split_line
            recorded_keys.append((key, float(event_time), event_type))
    print('Recordings loaded from file:', filename)

# Register a hotkey to toggle recording
keyboard.add_hotkey(RECORD_KEY, toggle_recording)

# Register a hotkey to play back recorded keys
keyboard.add_hotkey(PLAY_KEY, play_back_keys)

# Register a hotkey to save recordings
keyboard.add_hotkey('Ctrl+Shift+S', lambda: save_recordings(RECORDINGS_FILE))

# Register a hotkey to load recordings
keyboard.add_hotkey('Ctrl+Shift+L', lambda: load_recordings(RECORDINGS_FILE))

# Register a listener for both key press and key release events
keyboard.hook(record_key)

# Start the keyboard event listener
keyboard.wait()
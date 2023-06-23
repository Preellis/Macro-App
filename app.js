const { app } = require('electron');
const robot = require('robotjs');
const ioHook = require('iohook');

let isRecording = false;
let recordedKeys = [];

function recordKey(event) {
  const { keycode, rawcode } = event;
  const key = rawcode.toString();

  if (isRecording) {
    recordedKeys.push(key);
    console.log('Recorded:', key);
  }
}

function playBackKeys() {
  for (const key of recordedKeys) {
    console.log('Playing:', key);
    robot.keyTap(key);
  }
}

app.whenReady().then(() => {
  // Start the ioHook key event listening
  ioHook.start();

  // Register a global shortcut for toggling recording mode
  ioHook.registerShortcut([ioHook.MOD_CONTROL, ioHook.MOD_ALT], (keys) => {
    if (keys[0] && keys[1]) {
      isRecording = !isRecording;
      console.log('Recording:', isRecording);
    }
  });

  // Register a global shortcut for playing back keys
  ioHook.registerShortcut([ioHook.MOD_CONTROL, ioHook.MOD_ALT], (keys) => {
    if (keys[0] && keys[1]) {
      playBackKeys();
      console.log('Playing back:', recordedKeys);
    }
  });

  // Register the key event handler
  ioHook.on('keydown', recordKey);

  // Handle the case when the app is about to quit
  app.on('will-quit', () => {
    // Unregister all shortcuts and stop ioHook
    ioHook.unregisterAllShortcuts();
    ioHook.stop();
  });
});
from pynput import keyboard

recording = False
v = [0]
m = 0

def start_recording():
    recording = True
    m = time.time()

def stop_recording():
    recording = False
    print("Stopped recording")

def on_press(key):
    if key == 'e':
        if recording:
            stop_recording()
        else:
            start_recording()
    elif key == keyboard.Key.space and recording:
        v.append(time.time() - m)

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join() # This will prevent main process to end
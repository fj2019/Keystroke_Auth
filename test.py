from pynput import keyboard
import time
def on_press(key):

    print(key)
    return False
def on_release(key):
    print(key)
    #print(time)
    #print('release',key,time.time()-last_time)
    return False

while 1:
     with keyboard.Listener(
            on_press=on_press,on_release=on_release) as listener:
        listener.join()
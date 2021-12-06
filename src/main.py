import pynput


MODIFIER_KEYS = (
    pynput.keyboard.KeyCode(65027), 
    pynput.keyboard.Key.alt_gr,
) # alt_gr

MODIFIABLE_KEYS = {
    'a': 'ä',
    'A': 'Ä',
    'o': 'ö',
    'O': 'Ö',
    'u': 'ü',
    'U': 'Ü',
}


modifier_pressed = False
shift_pressed = False
caps_lock_active = False

controller = pynput.keyboard.Controller()


def on_press(key: pynput.keyboard.KeyCode) -> None:
    global modifier_pressed
    global shift_pressed
    global caps_lock_active

    if modifier_pressed:

        if type(key) != pynput.keyboard.KeyCode:
            return

        modified = MODIFIABLE_KEYS.get(key.char)
        if modified:
            if shift_pressed and not caps_lock_active or not shift_pressed and caps_lock_active:
                modified = modified.upper()

            controller.tap(pynput.keyboard.Key.backspace)
            controller.tap(modified)
    
    elif key in MODIFIER_KEYS:
        modifier_pressed = True
    
    elif key == pynput.keyboard.Key.shift:
        shift_pressed = True
    
    elif key == pynput.keyboard.Key.caps_lock:
        caps_lock_active = not caps_lock_active
        if caps_lock_active:
            controller.press(pynput.keyboard.Key.caps_lock)
            controller.release(pynput.keyboard.Key.caps_lock)


def on_release(key: pynput.keyboard.Key) -> None:
    if key in MODIFIER_KEYS:
        global modifier_pressed
        modifier_pressed = False
    
    elif key == pynput.keyboard.Key.shift:
        global shift_pressed
        shift_pressed = False
        

def main() -> None:
    
    with pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()


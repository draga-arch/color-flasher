import tkinter as tk
import itertools

# list of colours to cycle through
COLORS = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black']

root = tk.Tk()
root.title("Flashing colours")
root.attributes('-fullscreen', True)      # make the window cover the screen
root.configure(bg=COLORS[0])

colour_iter = itertools.cycle(COLORS)

def flash():
    root.configure(bg=next(colour_iter))
    root.after(200, flash)                # change every 200 ms (adjust as needed)

root.after(0, flash)
root.mainloop()
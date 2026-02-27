"""
Smooth fullscreen color flasher using tkinter (no pygame required).

Usage examples:
    python color_flasher_tk.py               # fullscreen, default speed
    python color_flasher_tk.py --windowed    # windowed mode
    python color_flasher_tk.py --speed 5.0   # faster hue cycles per second
    python color_flasher_tk.py --fps 60      # update frequency
    python color_flasher_tk.py --duration 5  # run 5 seconds then exit

Press ESC to exit.
"""

import argparse
import colorsys
import time
import sys
import tkinter as tk


def run_tk_flasher(windowed=False, speed=0.05, fps=60, duration=None):
    root = tk.Tk()
    root.title('Color Flasher')

    if not windowed:
        try:
            root.attributes('-fullscreen', True)
            root.configure(cursor='none')
        except Exception:
            root.overrideredirect(True)
            w = root.winfo_screenwidth()
            h = root.winfo_screenheight()
            root.geometry(f"{w}x{h}+0+0")

    frame = tk.Frame(root, width=800, height=600)
    frame.pack(fill=tk.BOTH, expand=True)

    start = time.time()
    last = start
    hue = 0.0
    running = {'val': True}

    def stop(event=None):
        running['val'] = False
        try:
            root.destroy()
        except Exception:
            pass

    root.bind('<Escape>', stop)
    root.protocol('WM_DELETE_WINDOW', stop)

    interval_ms = max(5, int(1000 / fps))

    def update():
        nonlocal hue, last
        now = time.time()
        dt = now - last
        last = now
        # speed = hue cycles per second
        hue = (hue + speed * dt) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
        try:
            frame.config(bg=color)
        except Exception:
            pass

        if duration is not None and (now - start) >= duration:
            stop()
            return

        if running['val']:
            root.after(interval_ms, update)

    root.after(0, update)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        stop()


def main():
    parser = argparse.ArgumentParser(description='Tkinter fullscreen color flasher (no pygame)')
    parser.add_argument('--windowed', '-w', action='store_true', help='Run in a window instead of fullscreen')
    parser.add_argument('--speed', '-s', type=float, default=0.05, help='Hue cycles per second (default 0.05)')
    parser.add_argument('--fps', type=int, default=60, help='Update frequency cap (default 60)')
    parser.add_argument('--duration', '-d', type=float, help='Seconds to run before exiting')
    args = parser.parse_args()

    if args.speed <= 0:
        print('Speed must be > 0')
        sys.exit(1)

    run_tk_flasher(windowed=args.windowed, speed=args.speed, fps=max(15, args.fps), duration=args.duration)


if __name__ == '__main__':
    main()

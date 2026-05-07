"""

In this game you need to get the same color values as given to you, at the upmost left corner there is a hue that you need to match. (here you can also see the percentage of pixels that are that color)
Just move your mouse over the image to get values in the graph and get them inside the range.
you can get a new color if this one is too hard or you cannot find it.

DISCLAIMER:
yes when it reveals it is probably not where you found it, this is because there are a lot of options ofcourse.

"""
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import random

#Load the Image
try:
    img = Image.open("Pillars of Creation.png").convert("RGB")
    img_data = np.asarray(img)
    h, w, _ = img_data.shape
    total_pixels = h * w
except FileNotFoundError:
    print("Error: 'Pillars of Creation.png' not found, please add to folder.")
    exit()

#Make Game Class so we can boot
class PillarGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pillars of Creation: Spectral Range Hunter")
        self.root.attributes('-topmost', True)
        # --- make the window start maximized/fullscreen ---
        try:
            self.root.state('zoomed') # For Windows
        except:
            self.root.attributes('-fullscreen', True) # For Linux/Mac
        
        self.game_won = False
        self.percent = 5 #percentage you may differ from the actual value
        self.tolerance = self.percent/100 * 255 
        
        # Row 0 = Top UI, Row 1 = Graph/Image (Expands), Row 2 = Buttons
        self.root.grid_rowconfigure(1, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)

        # --- UI Top Panel ---
        self.ui_frame = tk.Frame(root)
        self.ui_frame.grid(row=0, column=0, pady=10, sticky="ew")

        # TOP UI with color and percentage
        tk.Label(self.ui_frame, text="Target Range:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        self.target_canvas = tk.Canvas(self.ui_frame, width=100, height=30, highlightthickness=1, highlightbackground="black")
        self.target_canvas.grid(row=0, column=1, padx=5)
        
        self.freq_label = tk.Label(self.ui_frame, text="Range Pop: 0.00%", fg="blue", font=('Arial', 10))
        self.freq_label.grid(row=0, column=2, padx=15)

        tk.Label(self.ui_frame, text="Your Color:", font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=5)
        self.current_swatch = tk.Canvas(self.ui_frame, width=30, height=30, highlightthickness=1, highlightbackground="black")
        self.current_swatch.grid(row=0, column=4, padx=5)
        
        tk.Label(self.ui_frame, text="Telemetry:", font=('Arial', 10, 'bold')).grid(row=0, column=5, padx=15)
        self.coord_label = tk.Label(self.ui_frame, text="[SCANNING...]", fg="gray", font=('Courier', 12, 'bold'))
        self.coord_label.grid(row=0, column=6, sticky="w")

        # --- Matplotlib Setup Scaling ---
        # constrained_layout ensures the labels/buttons don't overlap the axis
        self.fig, (self.ax_img, self.ax_spec) = plt.subplots(2, 1, constrained_layout=True)
        self.ax_img.imshow(img_data)
        self.ax_img.axis('off')
        
        self.channels = [1, 2, 3]
        self.target_line, = self.ax_spec.plot(self.channels, [0,0,0], 'k--', alpha=0.3, label="Target Center")
        self.live_line, = self.ax_spec.plot(self.channels, [0,0,0], 'r-o', linewidth=2, label="Your Signal")
        
        self.fill_area = None 
        self.win_markers = [] 

        self.ax_spec.set_ylim(0, 255)
        self.ax_spec.set_xticks(self.channels)
        self.ax_spec.set_xticklabels(['Red', 'Green', 'Blue'])
        self.ax_spec.legend(loc='upper right')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        # grid the canvas into row 1 (the expanding row)
        self.canvas_widget.grid(row=1, column=0, sticky="nsew")

        # --- Controls (Lock to bottom) ---
        self.btn_frame = tk.Frame(root)
        self.btn_frame.grid(row=2, column=0, pady=20, sticky="ew")
        self.btn_frame.grid_columnconfigure((0,1), weight=1) # Center buttons
        
        self.new_btn = tk.Button(self.btn_frame, text="START NEW MISSION", command=self.generate_target, 
                                 bg="#2196F3", fg="white", font=('Arial', 12, 'bold'), height=2, width=25)
        self.new_btn.grid(row=0, column=0, padx=20, sticky="e")
        
        self.exit_btn = tk.Button(self.btn_frame, text="EXIT SYSTEM", command=root.destroy, 
                                  bg="#f44336", fg="white", font=('Arial', 10), height=2, width=15)
        self.exit_btn.grid(row=0, column=1, padx=20, sticky="w")

        self.generate_target()
        self.fig.canvas.mpl_connect('motion_notify_event', self.track_mouse)

        #Define Gradient
    def draw_target_gradient(self, rgb):
        self.target_canvas.delete("all")
        width, height = 100, 30
        for i in range(width):
            shift = ((i / width) - 0.5) * 2 * self.tolerance
            shifted_rgb = np.clip(rgb + shift, 0, 255).astype(int)
            hex_c = "#%02x%02x%02x" % tuple(shifted_rgb)
            self.target_canvas.create_line(i, 0, i, height, fill=hex_c)
        self.target_canvas.create_line(width//2, 0, width//2, height, fill="white", dash=(2,2))
        
        #Generate new targets
    def generate_target(self):
        self.game_won = False
        self.current_swatch.config(highlightbackground="black", highlightthickness=1)
        self.coord_label.config(text="[SCANNING...]", fg="gray")

        for marker in self.win_markers:
            marker.remove()
        self.win_markers = []

        self.tx, self.ty = random.randint(0, w-1), random.randint(0, h-1)
        self.target_rgb = img_data[self.ty, self.tx].astype(float)
        
        diff = np.abs(img_data.astype(float) - self.target_rgb)
        matches = np.all(diff <= self.tolerance, axis=-1)
        percentage = (np.sum(matches) / total_pixels) * 100
        
        self.freq_label.config(text=f"Range Pop: {percentage:.2f}%")
        self.draw_target_gradient(self.target_rgb)
        self.target_line.set_ydata(self.target_rgb)
        
        if self.fill_area: self.fill_area.remove()
        self.fill_area = self.ax_spec.fill_between(
            self.channels, 
            np.clip(self.target_rgb - self.tolerance, 0, 255),
            np.clip(self.target_rgb + self.tolerance, 0, 255),
            color='gray', alpha=0.15, label="5% Buffer"
        )
        
        self.live_line.set_color('red')
        self.ax_spec.set_title("Scan the image for a spectral match")
        self.canvas.draw()
        #Track Mouse function. this goes on forever
    def track_mouse(self, event):
        if self.game_won or event.inaxes != self.ax_img:
            return
        
        ix, iy = int(event.xdata), int(event.ydata)
        if 0 <= ix < w and 0 <= iy < h:
            current_rgb = img_data[iy, ix]
            hex_color = "#%02x%02x%02x" % tuple(current_rgb)
            self.current_swatch.config(bg=hex_color)
            self.live_line.set_ydata(current_rgb)
            
            if np.all(np.abs(current_rgb.astype(float) - self.target_rgb) <= self.tolerance):
                self.game_won = True
                self.live_line.set_color('lime')
                self.reveal_target_location()
            
            self.canvas.draw_idle()
        #Whenever you win you get to see where it was.
    def reveal_target_location(self):
        self.ax_spec.set_title("SIGNAL LOCKED!")
        self.coord_label.config(text=f"[{self.tx}, {self.ty}]", fg="#d32f2f")
        target_hex = "#%02x%02x%02x" % tuple(self.target_rgb.astype(int))
        self.current_swatch.config(bg=target_hex, highlightbackground="lime", highlightthickness=3)

        circle = self.ax_img.scatter(self.tx, self.ty, s=1500, edgecolors='black', facecolors='none', linestyles='--')
        self.win_markers.append(circle)

        # Longer arrow for widescreen view
        arrow_and_text = self.ax_img.annotate(
            "SIGNAL SOURCE", 
            xy=(self.tx, self.ty),
            xytext=(self.tx + 400, self.ty + 400),
            color="white", fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='black', alpha=0.8, edgecolor='red', boxstyle='round,pad=0.5'),
            arrowprops=dict(facecolor='red', edgecolor='white', shrink=0.1, width=2, headwidth=10)
        )
        self.win_markers.append(arrow_and_text)
        self.canvas.draw_idle()

#Start the game
if __name__ == "__main__":
    root = tk.Tk()
    app = PillarGame(root)
    root.mainloop()
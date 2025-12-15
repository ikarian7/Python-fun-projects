import tkinter as tk
from tkinter import filedialog
import vlc
import os

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Video Player with Audio")
        self.root.geometry("800x600")
        
        # VLC player instance
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        
        # Video display
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Controls Frame
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Buttons
        self.open_button = tk.Button(self.controls_frame, text="Open Video", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_video, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause_video, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_video, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(self.controls_frame, variable=self.progress_var, from_=0, to=100, orient=tk.HORIZONTAL, length=300, command=self.seek_video)
        self.progress_bar.pack(side=tk.LEFT, padx=5, pady=5)

        # Volume Slider
        self.volume_var = tk.DoubleVar(value=50)  # Default volume
        self.volume_slider = tk.Scale(self.controls_frame, variable=self.volume_var, from_=0, to=100, orient=tk.HORIZONTAL, length=100, label="Volume")
        self.volume_slider.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Video Variables
        self.video_path = None
        self.is_playing = False

    def open_file(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if self.video_path:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)

    def play_video(self):
        if self.video_path and not self.is_playing:
            self.is_playing = True
            self.media = self.Instance.media_new(self.video_path)
            self.player.set_media(self.media)
            self.player.set_hwnd(self.video_frame.winfo_id())  # Embed video in the Tkinter window
            
            # Set volume
            self.player.audio_set_volume(int(self.volume_var.get()))
            
            self.player.play()
            self.update_progress()
            self.root.after(100, self.check_if_playing)

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()
        self.is_playing = False
        self.progress_var.set(0)

    def seek_video(self, value):
        self.player.set_time(int(float(value) * 1000))

    def update_progress(self):
        if self.is_playing:
            current_time = self.player.get_time() / 1000  # Convert to seconds
            total_time = self.player.get_length() / 1000  # Convert to seconds
            self.progress_var.set((current_time / total_time) * 100)
            self.root.after(100, self.update_progress)

    def check_if_playing(self):
        if self.player.get_state() == vlc.State.Ended:
            self.stop_video()
        else:
            self.root.after(100, self.check_if_playing)

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()

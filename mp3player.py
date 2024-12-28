import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import os
import random
import time
import json

# Initialize Pygame mixer
pygame.mixer.init()

# Create a simple Tkinter window
root = tk.Tk()
root.title("Enhanced MP3 Player")
root.geometry("400x600")

# Create a listbox to display the playlist
playlist = tk.Listbox(root, selectmode=tk.SINGLE, bg="black", fg="white", width=50, height=10)
playlist.pack(pady=20)

# Global variables
current_song = None
is_playing = False
songs = []
repeat_song = False
current_song_index = 0

# Function to load songs
def load_songs():
    global songs
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for file in files:
        songs.append(file)
        playlist.insert(tk.END, os.path.basename(file))
    if files:
        playlist.selection_set(0)  # Select the first song
        messagebox.showinfo("Success", f"{len(files)} song(s) added to playlist")
    else:
        messagebox.showwarning("No files selected", "Please select MP3 files to add to the playlist")

# Function to play selected song
def play():
    global current_song, is_playing, current_song_index
    if playlist.curselection():
        try:
            current_song_index = playlist.curselection()[0]
            selected_song = songs[current_song_index]
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
            current_song = selected_song
            is_playing = True
            update_progress()
        except pygame.error as e:
            messagebox.showerror("File Error", f"Could not play the selected file: {str(e)}")
    else:
        messagebox.showwarning("No Selection", "Please select a song from the playlist")

# Function to pause the music
def pause():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False

# Function to resume the music
def resume():
    global is_playing
    pygame.mixer.music.unpause()
    is_playing = True
    update_progress()

# Function to stop the music
def stop():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    progress_bar['value'] = 0
    duration_label.config(text="00:00 / 00:00")

# Function to set volume
def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

# Function to shuffle playlist
def shuffle():
    global songs
    random.shuffle(songs)
    playlist.delete(0, tk.END)
    for song in songs:
        playlist.insert(tk.END, os.path.basename(song))

# Function to update progress bar and duration label
def update_progress():
    if is_playing:
        current_time = pygame.mixer.music.get_pos() / 1000
        progress_bar['value'] = current_time
        update_duration_label(current_time)
        root.after(1000, update_progress)

# Function to toggle repeat
def toggle_repeat():
    global repeat_song
    repeat_song = not repeat_song
    if repeat_song:
        repeat_button.config(bg="lightgreen")
    else:
        repeat_button.config(bg="lightgray")

# Function to play next song
def next_song():
    global current_song_index
    if current_song_index < len(songs) - 1:
        current_song_index += 1
    else:
        current_song_index = 0
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(current_song_index)
    play()

# Function to play previous song
def previous_song():
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
    else:
        current_song_index = len(songs) - 1
    playlist.selection_clear(0, tk.END)
    playlist.selection_set(current_song_index)
    play()

# Function to save playlist
def save_playlist():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(songs, file)
        messagebox.showinfo("Success", "Playlist saved successfully")

# Function to load playlist
def load_playlist():
    global songs
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            songs = json.load(file)
        playlist.delete(0, tk.END)
        for song in songs:
            playlist.insert(tk.END, os.path.basename(song))
        messagebox.showinfo("Success", "Playlist loaded successfully")

# Function to update duration label
def update_duration_label(current_time):
    mins, secs = divmod(current_time, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    duration_label.config(text=f"{timeformat} / --:--")

# Create buttons for controlling playback
load_button = tk.Button(root, text="Load Songs", command=load_songs, bg="lightblue")
play_button = tk.Button(root, text="Play", command=play, bg="lightgreen")
pause_button = tk.Button(root, text="Pause", command=pause, bg="yellow")
resume_button = tk.Button(root, text="Resume", command=resume, bg="orange")
stop_button = tk.Button(root, text="Stop", command=stop, bg="red")
shuffle_button = tk.Button(root, text="Shuffle", command=shuffle, bg="pink")
repeat_button = tk.Button(root, text="Repeat", command=toggle_repeat, bg="lightgray")
next_button = tk.Button(root, text="Next", command=next_song, bg="lightblue")
previous_button = tk.Button(root, text="Previous", command=previous_song, bg="lightblue")
save_playlist_button = tk.Button(root, text="Save Playlist", command=save_playlist, bg="lightgreen")
load_playlist_button = tk.Button(root, text="Load Playlist", command=load_playlist, bg="lightgreen")

load_button.pack(pady=5)
play_button.pack(pady=5)
pause_button.pack(pady=5)
resume_button.pack(pady=5)
stop_button.pack(pady=5)
shuffle_button.pack(pady=5)
repeat_button.pack(pady=5)
next_button.pack(pady=5)
previous_button.pack(pady=5)
save_playlist_button.pack(pady=5)
load_playlist_button.pack(pady=5)

# Create volume control slider
volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_slider.set(50)  # Set default volume to 50%
volume_slider.pack(pady=10)

# Create progress bar
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

# Create duration label
duration_label = tk.Label(root, text="00:00 / --:--")
duration_label.pack(pady=5)

# Run the main loop
root.mainloop()

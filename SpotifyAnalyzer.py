import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
from collections import Counter
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


# Authenticate with Spotify (Client Credentials Flow)
auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to fetch all tracks from the playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    try:
        results = sp.playlist(playlist_id)
    except spotipy.exceptions.SpotifyException as e:
        messagebox.showerror(
            "Playlist Error",
            "Could not access playlist.\nPlease make sure it is set to public or unlisted."
        )
        return
    
    if not results or 'tracks' not in results:
        messagebox.showerror("Error", "Playlist data could not be retrieved.")
        return None

    tracks.extend(results['tracks']['items']) 
    while results['tracks']['next']:
        results['tracks'] = sp.next(results['tracks'])
        tracks.extend(results['tracks']['items'])
    return tracks

#Count all contributing artists
def count_artists(tracks):
    artist_count = Counter()
    for item in tracks:
        track = item['track']
        if track and track['artists']:
            for artist in track['artists']:
                artist_name = artist['name']
                artist_count[artist_name] += 1
    return artist_count

# Fetch the artist data and display based on user inputs
def fetch_and_display():
    playlist_url = playlist_url_entry.get()
    try:
        # Extract playlist ID
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
        if not match:
            match = re.search(r'([a-zA-Z0-9]{22})', playlist_url)
        if not match:
            messagebox.showerror("Error", "Invalid playlist URL.")
            return
        playlist_id = match.group(1)

        # Fetch tracks
        tracks = get_playlist_tracks(sp, playlist_id)
        if not tracks:
            return  # Stop if there was an error

        # Count artists
        artist_count = count_artists(tracks)

        # Ask for number of artists or all
        top_n = top_n_entry.get()
        if top_n.lower() == 'all':
           artist_data = artist_count.most_common()
        else:
            try:
                top_n = int(top_n)
                artist_data = artist_count.most_common(top_n)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for top artists.")
                return

        # Ask for display option (pie chart or list)
        display_option = display_option_var.get()

        # Clear previous content
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        #Display pie chart
        if display_option == 'pie':
            labels = [a for a, _ in artist_data]
            sizes = [c for _, c in artist_data]

            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
            ax.axis('equal')
            ax.set_title(f"Top {len(labels)} Artists by Number of Songs (All Contributors)")

            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        #Display list
        elif display_option == 'list':
            list_frame = tk.Frame(canvas_frame)
            list_frame.pack(fill=tk.BOTH, expand=True)

            # Scrollable canvas for the list
            list_canvas = tk.Canvas(list_frame)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
            list_canvas.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            list_canvas.pack(side="left", fill="both", expand=True)

            list_widget_frame = tk.Frame(list_canvas)
            list_canvas.create_window((0, 0), window=list_widget_frame, anchor="nw")

            # Populate the list of artists
            for artist, count in artist_data:
                label = tk.Label(list_widget_frame, text=f"{artist}: {count} songs", font=("Helvetica", 10))
                label.pack(anchor="w", padx=10, pady=5)

            list_widget_frame.update_idletasks()  # Update list size
            list_canvas.config(scrollregion=list_canvas.bbox("all"))  # Scroll region to fit content

        else:
            messagebox.showerror("Error", "Please select 'pie' or 'list'.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

#Tkinter GUI Setup
root = tk.Tk()
info_label = tk.Label(
    root,
    text="Playlist must be PUBLIC or UNLISTED to work!",
    fg="red",
    font=("Helvetica", 10, "bold"),
    wraplength=480,
    justify="center"
)
info_label.pack(pady=10)
root.title("Spotify Artist Display")
root.geometry("800x600")
root.config(bg="#ffffff")  # White background

# Frame for Inputs
input_frame = tk.Frame(root, bg="#ffffff")
input_frame.pack(padx=20, pady=20)

# Playlist URL Entry
tk.Label(input_frame, text="Enter Spotify Playlist URL:", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
playlist_url_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12), relief="solid")
playlist_url_entry.grid(row=0, column=1, padx=5, pady=5)

# Top N Artists Entry
tk.Label(input_frame, text="How many top artists to display? (Enter a number or 'all'):", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
top_n_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12), relief="solid")
top_n_entry.grid(row=1, column=1, padx=5, pady=5)

# Display Option (Pie Chart or List)
tk.Label(input_frame, text="Choose display option:", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
display_option_var = tk.StringVar(value='pie')  # Default to 'pie'
pie_radio = tk.Radiobutton(input_frame, text="Pie Chart", variable=display_option_var, value='pie', font=("Helvetica", 12), bg="#ffffff")
pie_radio.grid(row=2, column=1, padx=5, pady=5, sticky="w")
list_radio = tk.Radiobutton(input_frame, text="List", variable=display_option_var, value='list', font=("Helvetica", 12), bg="#ffffff")
list_radio.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Button to fetch and display data
fetch_button = tk.Button(root, text="Fetch and Display", command=fetch_and_display, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="solid", padx=10, pady=5)
fetch_button.pack(pady=20)

# Frame for canvas (pie chart or list)
canvas_frame = tk.Frame(root, bg="#f5f5f5")
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Start the Tkinter loop
root.mainloop()
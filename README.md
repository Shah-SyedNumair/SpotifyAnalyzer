# SpotifyAnalyzer

## Description
Simple looking aplication that requests a public spotify playlist from user and the amount of artists they wanna see within a pie chart or list. The application will return an output as a list or pie (per user request) of the artists and amount of songs they are on in the playlist given.

## Table of Contents  
- Prerequisites  
- Installation  
- Usage  
- Features  
- Technologies Used  
- Troubleshooting  

---

## Prerequisites  
Before you begin, ensure you have the following installed:  

- Python 3.10+  
- pip (Python package installer)  
- Spotify Developer API credentials (Client ID and Client Secret)  

### How to Get Spotify API Credentials  
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)  
2. Log in with your Spotify account.  
3. Click **Create an App**.  
4. Fill in the app name and description.  
5. After creating the app, you will find your **Client ID** and **Client Secret** on the app page.  
6. Use these values in your `.env` file.

---

## Installation  

### Step 1: Clone the Repository  
```bash
git clone https://github.com/yourusername/spotify-artist-analyzer.git
cd spotify-artist-analyzer
```

### Step 2: Install dependencies
Use the provided `requirements.txt` file to install all necessary packages:
```bash
pip install -r requirements.txt
```
### Step 3: Setup Spotify API Credentials
Create a .env file in the root directory with your Spotify API credentials:
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret

## Usage

Run the application with:

```bash
python spotify_gui.py
```

Paste a public or unlisted Spotify playlist URL.

Enter how many top artists to display (number or all).

Select display option: pie chart or list.

Click Fetch and Display.

## Features

Fetches all tracks from a Spotify playlist

Counts and ranks contributing artists

Visualizes data as pie chart or scrollable list

User-friendly Tkinter GUI

## Technologies Used

Python

Spotipy (Spotify Web API client)

Tkinter (GUI)

Matplotlib (Charts)

python-dotenv (Environment variable loading)

## Images

![image](https://github.com/user-attachments/assets/a379eebe-2fb2-4e35-bfcd-183e5cafbd4b)

![image](https://github.com/user-attachments/assets/188f77ae-50e1-4787-915d-2738e595f3e5)

![image](https://github.com/user-attachments/assets/9bb781f5-35ee-42b4-9b98-b294fb40b6ea)



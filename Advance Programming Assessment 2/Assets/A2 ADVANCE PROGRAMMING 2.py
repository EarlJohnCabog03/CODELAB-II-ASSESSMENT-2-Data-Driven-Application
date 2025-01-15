import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# TMDB API key (replace with your API key)
API_KEY = 'd32d5664b57890f2461a0c1c903c63da'
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'  # Base URL for movie posters

# Custom colors
PRIMARY_BG = "#2c3e50"  # Dark blue-gray
SECONDARY_BG = "#34495e"  # Lighter gray-blue
TEXT_COLOR = "#ecf0f1"  # Light gray
BUTTON_COLOR = "#3498db"  # Blue
BUTTON_TEXT_COLOR = "#000000"  # BLACK
HIGHLIGHT_COLOR = "#1abc9c"  # Teal

# Function to fetch movies by category
def fetch_movies(category):
    url = f"{BASE_URL}/movie/{category}"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data from TMDB! Error: {e}")
        return []

    data = response.json()
    return data.get('results', [])

# Function to populate category movies
def display_category_movies(category):
    movies = fetch_movies(category)
    category_listbox.delete(0, tk.END)
    category_details.clear()

    if not movies:
        category_listbox.insert(tk.END, "No movies found.")
        return

    for movie in movies:
        title = movie['title']
        release_date = movie.get('release_date', 'N/A')
        category_listbox.insert(tk.END, f"{title} ({release_date})")
        category_details[title] = movie

# Function to fetch movies by search query
def search_movie():
    query = search_entry.get()
    if not query.strip():
        messagebox.showerror("Error", "Please enter a movie name!")
        return

    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data from TMDB! Error: {e}")
        return

    data = response.json()
    results = data.get('results', [])
    movie_listbox.delete(0, tk.END)
    movie_details.clear()

    if not results:
        messagebox.showinfo("No Results", f"No movies found for '{query}'")
        return

    for movie in results:
        title = movie['title']
        release_date = movie.get('release_date', 'N/A')
        movie_listbox.insert(tk.END, f"{title} ({release_date})")
        movie_details[title] = movie

# Function to display styled movie details and poster
def show_movie_details(event, listbox, details_dict, text_widget, poster_label):
    selected_index = listbox.curselection()
    if not selected_index:
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "No movie selected.", "default")
        text_widget.config(state="disabled")
        poster_label.config(image="", text="No poster available.")
        return

    selected_movie = listbox.get(selected_index)
    movie_title = selected_movie.split(" (")[0]
    movie = details_dict.get(movie_title)

    if movie:
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, f"Title: ", "bold")
        text_widget.insert(tk.END, f"{movie['title']}\n\n", "title")
        text_widget.insert(tk.END, f"Release Date: ", "bold")
        text_widget.insert(tk.END, f"{movie.get('release_date', 'N/A')}\n\n", "default")
        text_widget.insert(tk.END, f"Rating: ", "bold")
        text_widget.insert(tk.END, f"{movie.get('vote_average', 'N/A')}/10\n\n", "rating")
        text_widget.insert(tk.END, "Overview:\n", "bold")
        text_widget.insert(tk.END, f"{movie.get('overview', 'No description available.')}", "default")
        text_widget.config(state="disabled")

        poster_path = movie.get('poster_path')
        if poster_path:
            poster_url = f"{IMAGE_BASE_URL}{poster_path}"
            try:
                response = requests.get(poster_url)
                response.raise_for_status()
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                img = img.resize((300, 450))
                poster_img = ImageTk.PhotoImage(img)
                poster_label.config(image=poster_img, text="")
                poster_label.image = poster_img
            except Exception as e:
                poster_label.config(image="", text="Failed to load image.")
        else:
            poster_label.config(image="", text="No poster available.")
    else:
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "No details available for the selected movie.", "default")
        text_widget.config(state="disabled")
        poster_label.config(image="", text="No poster available.")

# Function to populate the About tab
def populate_about_tab():
    about_text.set(
        "TMDB Movie Search\n"
        "Version: 1.0\n"
        "Developer: Earl\n\n"
        "This application allows you to search for movies, explore categories such as Popular, Top Rated, "
        "and Upcoming, and view detailed information about movies. Data is powered by TMDB (The Movie Database)."
    )

# GUI setup
root = tk.Tk()
root.title("TMDB Movie Search")
root.geometry("1000x700")
root.configure(bg=PRIMARY_BG)

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Search Tab
search_tab = ttk.Frame(notebook)
search_tab.configure(style="TFrame")
notebook.add(search_tab, text="Search")

# Categories Tab
categories_tab = ttk.Frame(notebook)
categories_tab.configure(style="TFrame")
notebook.add(categories_tab, text="Categories")

# About Tab
about_tab = ttk.Frame(notebook)
about_tab.configure(style="TFrame")
notebook.add(about_tab, text="About")

# Apply styling
style = ttk.Style()
style.configure("TFrame", background=PRIMARY_BG)
style.configure("TLabel", background=PRIMARY_BG, foreground=TEXT_COLOR, font=("Arial", 12))
style.configure("TButton", background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, font=("Arial", 12))
style.map("TButton", background=[("active", HIGHLIGHT_COLOR)])

# Search Tab Content
search_frame = ttk.Frame(search_tab)
search_frame.pack(pady=10, padx=10, fill=tk.X)

search_label = ttk.Label(search_frame, text="Search Movie:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = ttk.Button(search_frame, text="Search", command=search_movie)
search_button.pack(side=tk.LEFT, padx=5)

results_frame = ttk.Frame(search_tab)
results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

movie_listbox = tk.Listbox(results_frame, height=10, bg=SECONDARY_BG, fg=TEXT_COLOR, selectbackground=HIGHLIGHT_COLOR)
movie_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
movie_listbox.bind(
    '<<ListboxSelect>>',
    lambda event: show_movie_details(event, movie_listbox, movie_details, search_details_text, search_poster_label)
)

scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=movie_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
movie_listbox.config(yscrollcommand=scrollbar.set)

details_frame = ttk.Frame(search_tab)
details_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

search_details_text = tk.Text(details_frame, wrap=tk.WORD, height=15, bg=SECONDARY_BG, fg=TEXT_COLOR, font=("Arial", 12))
search_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
search_details_text.tag_configure("bold", font=("Arial", 12, "bold"))
search_details_text.tag_configure("title", font=("Arial", 14, "bold"), foreground=HIGHLIGHT_COLOR)
search_details_text.tag_configure("rating", font=("Arial", 12, "bold"), foreground="green")
search_details_text.tag_configure("default", font=("Arial", 12))
search_details_text.config(state="disabled")

search_poster_label = tk.Label(details_frame, bg=SECONDARY_BG, fg=TEXT_COLOR, text="No poster available.")
search_poster_label.pack(side=tk.RIGHT, padx=10, pady=10)


# Categories Tab Content
category_buttons_frame = ttk.Frame(categories_tab)
category_buttons_frame.pack(pady=10)

# Add buttons for each category with color styling
categories = {
    "Popular": "popular",
    "Top Rated": "top_rated",
    "Upcoming": "upcoming",
    "Now Playing": "now_playing"
}

for label, category in categories.items():
    ttk.Button(
        category_buttons_frame,
        text=label,
        command=lambda c=category: display_category_movies(c)
    ).pack(side=tk.LEFT, padx=10)

category_results_frame = ttk.Frame(categories_tab)
category_results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

category_listbox = tk.Listbox(category_results_frame, height=10, bg=SECONDARY_BG, fg=TEXT_COLOR, selectbackground=HIGHLIGHT_COLOR)
category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
category_listbox.bind(
    '<<ListboxSelect>>',
    lambda event: show_movie_details(event, category_listbox, category_details, category_details_text, category_poster_label)
)

category_scrollbar = ttk.Scrollbar(category_results_frame, orient=tk.VERTICAL, command=category_listbox.yview)
category_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
category_listbox.config(yscrollcommand=category_scrollbar.set)

category_details_frame = ttk.Frame(categories_tab)
category_details_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

category_details_text = tk.Text(category_details_frame, wrap=tk.WORD, height=15, bg=SECONDARY_BG, fg=TEXT_COLOR, font=("Arial", 12))
category_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
category_details_text.tag_configure("bold", font=("Arial", 12, "bold"))
category_details_text.tag_configure("title", font=("Arial", 14, "bold"), foreground=HIGHLIGHT_COLOR)
category_details_text.tag_configure("rating", font=("Arial", 12, "bold"), foreground="green")
category_details_text.tag_configure("default", font=("Arial", 12))
category_details_text.config(state="disabled")

category_poster_label = tk.Label(category_details_frame, bg=SECONDARY_BG, fg=TEXT_COLOR, text="No poster available.")
category_poster_label.pack(side=tk.RIGHT, padx=10, pady=10)

# About Tab Content
about_text = tk.StringVar()
populate_about_tab()

about_label = ttk.Label(about_tab, textvariable=about_text, justify=tk.LEFT, wraplength=750)
about_label.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
about_label.configure(background=PRIMARY_BG, foreground=TEXT_COLOR, font=("Arial", 12))

# Movie Details Dictionaries
movie_details = {}
category_details = {}

# Run the application
root.mainloop()

import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox, StringVar, IntVar
from PIL import Image, ImageTk, ImageDraw
import math
import cv2  # OpenCV for video handling
import math


# Setting up the main window
root = tk.Tk()
root.title("Hangman Game")

# Global variables
current_category = StringVar(value="Word Of The Day")
category_array = ["Word Of The Day", "Vegetables", "Cars", "Anime"]
shows = ['a', 'e', 'i', 'o', 'u']
word_display = StringVar()
current_word = ""
chances = IntVar(value=6)  # Number of chances for guessing
incorrect_guesses = []  # List to store incorrect guesses
csv_file = "Book1.csv"
used_words = []  # List to track words already used in the session

# Fetches the list of words for the current category
def get_category_list(category):
    try:
        df = pd.read_csv(csv_file, usecols=[category])
        return df[category].dropna().tolist()  # Return list of words for the current category
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

# Function to handle category selection
def select_category():
    category_window = tk.Toplevel(root)
    category_window.title("Select Category")
    
    tk.Label(category_window, text="Select a category:").pack(pady=10)
    
    for idx, category in enumerate(category_array):
        tk.Radiobutton(
            category_window,
            text=category,
            variable=current_category,
            value=category
        ).pack(anchor=tk.W)
    
    def confirm_selection():
        category_window.destroy()
        update_main_screen()
    
    tk.Button(category_window, text="OK", command=confirm_selection).pack(pady=10)

# Function to add a new word to the current category
def add_word():
    add_word_window = tk.Toplevel(root)
    add_word_window.title("Add Word")
    
    tk.Label(add_word_window, text=f"Add a new word to {current_category.get()}:").pack(pady=10)
    new_word_entry = tk.Entry(add_word_window)
    new_word_entry.pack(pady=5)
    
    def save_word():
        new_word = new_word_entry.get().strip()
        if new_word:
            try:
                # Append the new word to the CSV file under the appropriate category
                df = pd.read_csv(csv_file)
                if new_word not in df[current_category.get()].values:
                    df = df.append({current_category.get(): new_word}, ignore_index=True)
                    df.to_csv(csv_file, index=False)
                    messagebox.showinfo("Success", f"'{new_word}' has been added to {current_category.get()}!")
                else:
                    messagebox.showinfo("Duplicate", f"'{new_word}' is already in {current_category.get()}!")
            except Exception as e:
                print(f"Error updating CSV: {e}")
                messagebox.showerror("Error", "Could not add the word to the CSV file.")
        add_word_window.destroy()
    
    tk.Button(add_word_window, text="Add", command=save_word).pack(pady=10)

# Starts the game
def start_game():
    global current_word, shows, incorrect_guesses
    shows = ['a', 'e', 'i', 'o', 'u']  # Reset shown characters
    incorrect_guesses = []  # Reset incorrect guesses list
    current_word = get_word()
    if not current_word:
        messagebox.showinfo("End of Words", "No more words available in this category!")
        return
    chances.set(6)  # Reset chances for each new word
    word_display.set(" ".join(["_" if c.lower() not in shows else c for c in current_word.lower()]))
    
    def process_guess():
        usr_input = guess_entry.get().lower()
        if usr_input in current_word.lower() and usr_input not in shows:
            shows.append(usr_input)
            word_display.set(" ".join(["_" if c.lower() not in shows else c for c in current_word.lower()]))
            
            if "_" not in word_display.get().replace(" ", ""):
                victory()
        else:
            if usr_input not in incorrect_guesses:
                incorrect_guesses.append(usr_input)
                incorrect_guesses_label.config(text=f"Incorrect guesses: {', '.join(incorrect_guesses)}")
            chances.set(chances.get() - 1)
            chances_label.config(text=f"Chances left: {chances.get()}")
            if chances.get() == 0:
                game_over()
        
        guess_entry.delete(0, tk.END)
    
    game_frame = tk.Toplevel(root)
    game_frame.title("Hangman Game")
    
    tk.Label(game_frame, text="Guess the word:").pack(pady=10)
    tk.Label(game_frame, textvariable=word_display).pack(pady=10)
    
    guess_entry = tk.Entry(game_frame)
    guess_entry.pack(pady=5)
    
    tk.Button(game_frame, text="Submit", command=process_guess).pack(pady=5)
    
    # Display chances left
    global chances_label, incorrect_guesses_label
    chances_label = tk.Label(game_frame, text=f"Chances left: {chances.get()}")
    chances_label.pack(pady=5)

    # Display incorrect guesses
    incorrect_guesses_label = tk.Label(game_frame, text="Incorrect guesses: ")
    incorrect_guesses_label.pack(pady=5)

# Retrieves a random word from the selected category without repeating
def get_word():
    words_list = get_category_list(current_category.get())
    available_words = [word for word in words_list if word not in used_words]
    
    if available_words:
        chosen_word = random.choice(available_words)
        used_words.append(chosen_word)
        return chosen_word
    else:
        return None  # No more words available in the category

# Rotating Victory Screen

# Function to display rotating text and video within the circle
def rotating_victory_screen_with_video(guessed_word, video_path):
    victory_window = tk.Toplevel(root)
    victory_window.title("Victory!")

    # Create canvas for circle and video
    canvas_width, canvas_height = 500, 500
    canvas = tk.Canvas(victory_window, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Adjust circle radius and position for a larger display
    circle_radius = 100
    circle_center_x, circle_center_y = canvas_width // 2, canvas_height // 2 + 50
    circle_left_top_x, circle_left_top_y = circle_center_x - circle_radius, circle_center_y - circle_radius
    circle_right_bottom_x, circle_right_bottom_y = circle_center_x + circle_radius, circle_center_y + circle_radius

    # Draw a white circle (circle boundary only, video will go inside)
    canvas.create_oval(circle_left_top_x, circle_left_top_y, circle_right_bottom_x, circle_right_bottom_y, outline="black", width=2)

    # Static text at the top
    canvas.create_text(canvas_width // 2, 50, text="You've guessed the word!", font=("Arial", 18, "bold"), fill="green")

    # Load and play video
    cap = cv2.VideoCapture(video_path)

    # Variable to hold the current frame image
    frame_tk = None

    def update_frame():
        nonlocal frame_tk
        ret, frame = cap.read()

        if ret:
            # Resize frame to fit the circle size
            frame = cv2.resize(frame, (2 * circle_radius, 2 * circle_radius))

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert OpenCV image to PIL format
            frame_pil = Image.fromarray(frame_rgb)

            # Create mask for circle
            mask = Image.new("L", frame_pil.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 2 * circle_radius, 2 * circle_radius), fill=260)

            # Apply mask to the image
            frame_circular = Image.new("RGBA", frame_pil.size)
            frame_circular.paste(frame_pil, (0, 0), mask=mask)

            # Convert PIL image to ImageTk format
            frame_tk = ImageTk.PhotoImage(frame_circular)

            # Adjust the video position slightly lower
            canvas.create_image(circle_center_x, circle_center_y , image=frame_tk)  # Move video down by 20 pixels

            # Loop to continuously update frames
            victory_window.after(30, update_frame)
        else:
            # Restart video from beginning if end is reached
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            update_frame()

    # Start the video frame update loop
    update_frame()

    # Increase radius for text rotation to keep it outside the video circle
    text_radius = circle_radius + 50  # Increase the text radius by 40 pixels

    # Rotating guessed word along the edge of the circle
    text = canvas.create_text(circle_center_x- text_radius, circle_center_y - text_radius, text=guessed_word, font=("Arial", 24, "bold"), fill="blue")

    def rotate_text(angle=0):
        # Calculate new position using trigonometry for circular motion
        x = circle_center_x + text_radius * math.cos(math.radians(angle))
        y = circle_center_y + text_radius * math.sin(math.radians(angle))
        canvas.coords(text, x, y)
        victory_window.after(50, rotate_text, angle + 5)


    rotate_text()

    

# Handles victory condition and starts the next word
def victory():
    rotating_victory_screen_with_video(current_word, "Screen Recording 2024-08-31 at 1.35.28 pm.mp4")
  # Show rotating screen with the guessed word
    start_game()  # Start a new game immediately

# Handles game over condition and restarts the game
def game_over():
    messagebox.showinfo("Game Over", f"Game over! The word was: {current_word}")
    start_game()  # Start a new game immediately

# Updates the main screen based on current category selection
def update_main_screen():
    main_category.set(f"Current Category: {current_category.get()}")

# Resets the game to start over
def reset_game():
    global shows
    shows = ['a', 'e', 'i', 'o', 'u']
    word_display.set("")
    update_main_screen()

# Main Screen Setup
main_category = StringVar(value=f"Current Category: {current_category.get()}")

tk.Label(root, textvariable=main_category).pack(pady=10)

tk.Button(root, text="Select Category", command=select_category).pack(pady=5)
tk.Button(root, text="Add Word", command=add_word).pack(pady=5)
tk.Button(root, text="Start Game", command=start_game).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
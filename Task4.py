import pandas as pd
import tkinter as tk
from tkinter import messagebox
from sklearn.metrics.pairwise import cosine_similarity

# Load movie data and ratings
movies_df = pd.read_csv('ml-100k/u.item', sep='|', header=None, encoding='latin-1', usecols=[0, 1, 5], names=['movie_id', 'title', 'genre'])
ratings_df = pd.read_csv('ml-100k/u.data', sep='\t', header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Mapping genre codes to genre names
genre_dict = {
    0: 'Action', 1: 'Adventure', 2: 'Animation', 3: 'Children', 4: 'Comedy',
    5: 'Crime', 6: 'Documentary', 7: 'Drama', 8: 'Fantasy', 9: 'Film-Noir',
    10: 'Horror', 11: 'Musical', 12: 'Mystery', 13: 'Romance', 14: 'Sci-Fi',
    15: 'Thriller', 16: 'War', 17: 'Western'
}

# Add genres to the movies dataframe
movies_df['genre'] = movies_df['genre'].apply(lambda x: [genre_dict[int(i)] for i in str(x).split()])

# Create a content-based filtering recommendation system
def recommend_movies(user_preferences):
    user_genres = set(user_preferences)
    
    # Check if movie genres match user's preferences
    movies_df['match'] = movies_df['genre'].apply(lambda x: len(user_genres.intersection(set(x))) > 0)
    
    recommended_movies = movies_df[movies_df['match'] == True]
    
    return recommended_movies[['title', 'genre']].head(10)

# GUI for user interaction
def on_recommend():
    user_input = genre_entry.get().split(',')  # Accepting genres separated by commas
    user_input = [genre.strip() for genre in user_input]  # Remove extra spaces
    recommended = recommend_movies(user_input)
    
    result_text.delete(1.0, tk.END)  # Clear previous results
    if recommended.empty:
        result_text.insert(tk.END, "No recommendations found.")
    else:
        for index, row in recommended.iterrows():
            result_text.insert(tk.END, f"Title: {row['title']}, Genres: {', '.join(row['genre'])}\n")

# Setting up the GUI
root = tk.Tk()
root.title("Movie Recommendation System")

# Genre input label
genre_label = tk.Label(root, text="Enter your preferred genres (comma separated):")
genre_label.pack()

# Genre input entry
genre_entry = tk.Entry(root, width=50)
genre_entry.pack()

# Recommend button
recommend_button = tk.Button(root, text="Get Recommendations", command=on_recommend)
recommend_button.pack()

# Text area for displaying recommendations
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Run the application
root.mainloop()

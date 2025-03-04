import pandas as pd
import numpy as np

# Sample dataset: Movies with genres
movies_data = {
    'Title': ['Inception', 'Interstellar', 'The Dark Knight', 'The Matrix', 'Avatar'],
    'Genre': ['Sci-Fi Thriller', 'Sci-Fi Drama', 'Action Crime', 'Sci-Fi Action', 'Sci-Fi Adventure']
}
movies_df = pd.DataFrame(movies_data)

# Function to compute TF-IDF manually
def compute_tfidf(corpus):
    """
    Compute Term Frequency-Inverse Document Frequency (TF-IDF) without sklearn.
    
    Parameters:
        corpus (list): List of genre strings.
        
    Returns:
        tfidf_matrix (ndarray): TF-IDF matrix.
        vocab (list): List of unique words.
    """
    # Tokenize genres
    tokenized_genres = [genre.lower().split() for genre in corpus]
    
    # Create vocabulary
    vocab = sorted(set(word for genre in tokenized_genres for word in genre))
    
    # Compute Term Frequency (TF)
    tf_matrix = np.zeros((len(corpus), len(vocab)))
    for i, genre in enumerate(tokenized_genres):
        for word in genre:
            tf_matrix[i, vocab.index(word)] += 1
    
    # Compute Inverse Document Frequency (IDF)
    doc_count = np.sum(tf_matrix > 0, axis=0)
    idf = np.log((1 + len(corpus)) / (1 + doc_count)) + 1  # Adding 1 for smoothing
    
    # Compute TF-IDF
    tfidf_matrix = tf_matrix * idf
    return tfidf_matrix, vocab

# Compute TF-IDF for genres
tfidf_matrix, vocab = compute_tfidf(movies_df['Genre'])

# Compute cosine similarity manually
def cosine_similarity_manual(matrix):
    """
    Compute the cosine similarity between rows of a matrix manually.
    
    Parameters:
        matrix (ndarray): TF-IDF matrix.
        
    Returns:
        sim_matrix (ndarray): Cosine similarity matrix.
    """
    norm = np.linalg.norm(matrix, axis=1, keepdims=True)
    normalized_matrix = matrix / (norm + 1e-9)  # Avoid division by zero
    return np.dot(normalized_matrix, normalized_matrix.T)

# Get cosine similarity matrix
cosine_sim_matrix = cosine_similarity_manual(tfidf_matrix)

def get_movie_recommendations(movie_title, df, sim_matrix, top_n=3):
    """
    Recommend similar movies based on the provided movie title.
    
    Parameters:
        movie_title (str): The title of the movie to search recommendations for.
        df (DataFrame): The dataframe containing movies data.
        sim_matrix (ndarray): Precomputed cosine similarity matrix.
        top_n (int): Number of top recommendations to return.
    
    Returns:
        list: A list of recommended movie titles.
    """
    if movie_title not in df['Title'].values:
        return f"Movie '{movie_title}' not found in the dataset."
    
    index = df[df['Title'] == movie_title].index[0]
    similar_scores = list(enumerate(sim_matrix[index]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    
    # Exclude the first entry (itself)
    recommendations = [df['Title'][i[0]] for i in similar_scores[1:top_n+1]]
    return recommendations

# Example usage
movie_to_search = "Inception"
recommended = get_movie_recommendations(movie_to_search, movies_df, cosine_sim_matrix, top_n=3)
print(f"Movies similar to '{movie_to_search}': {recommended}")
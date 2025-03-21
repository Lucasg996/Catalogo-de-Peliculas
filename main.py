import pandas as pd
import numpy as np
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset 'data.csv'
df = pd.read_csv('D:\\Users\\PC\\Downloads\\data.csv')

# Seleccionar características relevantes
features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']
df_features = df[features]

# Normalizar las características
scaler = MinMaxScaler()
df_normalized = scaler.fit_transform(df_features)

# Reducir dimensionalidad con IncrementalPCA
pca = IncrementalPCA(n_components=5)
df_pca = pca.fit_transform(df_normalized)

def recommend_songs_with_dynamic_filters(song_name, top_n=10, year_tolerance=2, dynamic_range=0.1):
    """
    Recomienda canciones basándose en similitudes con la canción seleccionada, ajustando dinámicamente
    los rangos de energía y valencia a los valores de la canción base.

    Args:
        song_name (str): Nombre de la canción base.
        top_n (int): Número de canciones a recomendar.
        year_tolerance (int): Rango de tolerancia en años para las recomendaciones.
        dynamic_range (float): Rango dinámico de ajuste para energía y valencia.

    Returns:
        pd.DataFrame: Canciones recomendadas o mensaje de error.
    """
    # Verificar si la canción existe en el dataset
    song_indices = df[df['name'].str.lower() == song_name.lower()].index
    if len(song_indices) == 0:
        return f"La canción '{song_name}' no se encuentra en el dataset."
    
    # Obtener el índice de la canción seleccionada
    song_index = song_indices[0]
    year_of_song = df.loc[song_index, 'year']
    energy_of_song = df.loc[song_index, 'energy']
    valence_of_song = df.loc[song_index, 'valence']
    
    # Ajustar dinámicamente los rangos de energía y valencia
    energy_range = (energy_of_song - dynamic_range, energy_of_song + dynamic_range)
    valence_range = (valence_of_song - dynamic_range, valence_of_song + dynamic_range)
    
    # Filtrar canciones por año, energía y valencia
    df_filtered = df[
        (np.abs(df['year'] - year_of_song) <= year_tolerance) &
        (df['energy'].between(*energy_range)) &
        (df['valence'].between(*valence_range))
    ]
    
    # Verificar si hay canciones filtradas
    if df_filtered.empty:
        return f"No se encontraron canciones similares para '{song_name}' con los filtros actuales."
    
    # Calcular la similitud con las canciones filtradas
    filtered_indices = df_filtered.index
    similarity_scores = cosine_similarity(df_pca[song_index].reshape(1, -1), df_pca[filtered_indices])[0]
    
    # Ordenar las canciones por similitud en orden descendente
    similarity_scores = list(zip(filtered_indices, similarity_scores))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Seleccionar las canciones más similares
    similar_songs_indices = [i[0] for i in similarity_scores if i[0] != song_index][:top_n]
    
    # Eliminar duplicados por nombre y artista
    recommendations = df.iloc[similar_songs_indices][['name', 'artists', 'year', 'energy', 'valence']].drop_duplicates(subset=['name', 'artists'])
    
    return recommendations

# Programa interactivo
if __name__ == "__main__":
    while True:
        print("\nBienvenido al recomendador de canciones 🎵")
        print("Escribe el nombre de una canción o 'salir' para terminar.")
        song_name = input("Introduce el nombre de la canción: ").strip()
        
        if song_name.lower() == 'salir':
            print("¡Gracias por usar el recomendador de canciones! 🎧")
            break
        
        # Obtener recomendaciones
        recommendations = recommend_songs_with_dynamic_filters(song_name, top_n=21, year_tolerance=2, dynamic_range=0.1)
        
        # Mostrar las recomendaciones
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print(f"\nRecomendaciones para '{song_name}':")
            print(recommendations.to_string(index=False))

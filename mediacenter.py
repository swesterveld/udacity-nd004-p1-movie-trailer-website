import fresh_tomatoes # module to render movies
import media # module with classes for movies

# Initialize some favorite movies to be rendered, and put them in a list
starwars_iv = media.OMDbMovie(
        'http://www.imdb.com/title/tt0076759/',
        'https://www.youtube.com/watch?v=vZ734NWnAHA'
        )

princess_mononoke = media.OMDbMovie(
        'http://www.imdb.com/title/tt0119698/',
        'https://www.youtube.com/watch?v=4OiMOHRDs14'
        )

the_dark_knight = media.OMDbMovie(
        'http://www.imdb.com/title/tt0468569/',
        'https://www.youtube.com/watch?v=EXeTwQWrcwY'
        )

letters_from_iwo_jima = media.OMDbMovie(
        'http://www.imdb.com/title/tt0498380/',
        'https://youtu.be/U6rUr0mKwhc'
        )

inception = media.OMDbMovie(
        'http://www.imdb.com/title/tt1375666/',
        'https://www.youtube.com/watch?v=8hP9D6kZseM'
        )

zwartboek = media.OMDbMovie(
        'http://www.imdb.com/title/tt0389557/',
        'https://www.youtube.com/watch?v=DIklvGsU7bM'
        )

favorites = [princess_mononoke, starwars_iv, zwartboek, the_dark_knight,
        inception, letters_from_iwo_jima]

# Let the list of movies render on a webpage and open it in the web
# browser
fresh_tomatoes.open_movies_page(favorites)

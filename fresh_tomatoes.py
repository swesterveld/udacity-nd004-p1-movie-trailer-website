import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        /* Outline to help with alignment etc.
        * {
            outline: 1px solid red !important;
        }*/
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .col-centered {
            float: none;
            margin: 0 auto;
        }
        h2 {
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
        .key {
            font-weight: bold;
        }
        .movie-plot {
            height: 6em;
            overflow: hidden;
            text-align: justify;
        }
        .poster {
            max-height: 324px;
            max-width: 220px;
        }
        .rating-overlay {
            position:relative;
            top: -42px;
            margin-left: auto;
            margin-right: auto;
            width: 200px;
            height: 0;
            opacity: 0.50;
        }
        .rating-overlay img {
            display: block;
            max-height: 32px;
            background: white;
        }
        .row-movie-facts {
            padding: 15px 0 15px;
        }
    </style>
    <script type="text/javascript">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer" title="{movie_title}">
    <div class="row">
        <div class="col-xs-6 col-md-8 col-lg-10 col-centered movie-title text-center">
            <h2>{movie_title}</h2>
        </div>
    </div>
    <div class="row text-center">
        <div><img src="{poster_image_url}" alt="Poster of {movie_title}" class="poster"></div>
        <div class="rating-overlay">{rating_img}</div>
    </div>
    <div class="row row-movie-facts">
        <div class="col-xs-6 col-md-8 col-lg-10 col-centered"><span class="key">Released:</span> {movie_released}</div>
        <div class="col-xs-6 col-md-8 col-lg-10 col-centered"><span class="key">Director:</span> {movie_director}</div>
        <div class="col-xs-6 col-md-8 col-lg-10 col-centered movie-plot" title="{movie_plot}"><span class="key">Plot:</span> {movie_plot_limited}</div>
        <div class="col-xs-6 col-md-8 col-lg-10 col-centered"><span class="key">IMDb:</span> {movie_imdb_rating}/10 <span style="font-weight:bold">Metascore:</span> {movie_metascore}/100</div>
    </div><hr>
</div>
'''

def create_rating_img_content(movie):
    # http://en.wikipedia.org/wiki/Motion_Picture_Association_of_America_film_rating_system
    if movie.omdb['Rated'] in movie.VALID_RATINGS:
        return '<img src="{source}" alt="Rated {rating}">'.format(source=movie.get_rating_symbol(),rating=movie.omdb['Rated'])
    else:
        return ''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            trailer_youtube_id=trailer_youtube_id,
            poster_image_url=movie.poster_image_url,
            rating_img = create_rating_img_content(movie),
            movie_released = movie.get_release_date(),
            movie_director = movie.omdb['Director'],
            movie_plot=movie.omdb['Plot'],
            movie_plot_limited=movie.limit_plot(21),
            movie_imdb_rating = movie.omdb['imdbRating'],
            movie_imdb_votes = movie.omdb['imdbVotes'],
            movie_metascore = movie.omdb['Metascore']
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

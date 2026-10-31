from utils.data_generator import DataGenerator


def movie_payload():
    return{
    "name": DataGenerator.generate_random_name_movie(),
    "imageUrl": DataGenerator.generate_random_image_url(),
    "price": DataGenerator.generate_random_price(),
    "description": DataGenerator.generate_description(),
    "location": DataGenerator.generate_location(),
    "published": DataGenerator.generate_random_published_status(),
    "genreId": DataGenerator.generate_genre_id(),
    }

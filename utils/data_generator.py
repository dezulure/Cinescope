from faker import Faker

fake = Faker("en_US")


class DataGenerator:
    @staticmethod
    def generate_random_password(length: int = 12):
        return fake.password(
            length=length,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def generate_random_email():
        return fake.email()

    @staticmethod
    def generate_random_name():
        return fake.name()

    @staticmethod
    def generate_random_verified_status():
        return fake.random_element([True, False])

    @staticmethod
    def generate_random_banned_status():
        return fake.random_element([True, False])

    @staticmethod
    def generate_random_name_movie():
        adjectives = ["Dark", "Silent", "Lost", "Eternal", "Hidden"]
        nouns = ["Knight", "World", "Dream", "Legacy", "Secret"]
        return f"{fake.random.choice(adjectives)} {fake.random.choice(nouns)} {fake.random_int(min=1, max=9999)}"

    @staticmethod
    def generate_random_image_url():
        return fake.url()

    @staticmethod
    def generate_random_price():
        return fake.random_int(min=100, max=50000)

    @staticmethod
    def generate_description():
        description = ["A young hero discovers a hidden power that could change the world forever.",
                       "A detective investigates a mysterious disappearance in a small town.",
                       "Two strangers fall in love during an unexpected journey.",
                       "A group of friends must survive a terrifying night in an abandoned house.",
                       "A family moves into a house with a terrifying supernatural secret.", ]
        return fake.random_element(description)

    @staticmethod
    def generate_location():
        location = ["SPB", "MSK"]
        return fake.random_element(location)

    @staticmethod
    def generate_random_published_status():
        return fake.random_element([True, False])

    @staticmethod
    def generate_genre_id():
        ids = [5, 7, 9]
        return fake.random_element(ids)

    @staticmethod
    def generate_random_int(min: int = 1, max: int = 9999):
        return fake.random_element([min, max])
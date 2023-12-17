from init import db
import logging

class Film:
    def __init__(self, id, name, description, budget, rating, dateFound):
        self.id = id
        self.name = name
        self.description = description
        self.budget = budget
        self.rating = rating
        self.dateFound = dateFound

    def get_genres(self):
        query = "SELECT idGenre FROM FilmsGenres WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        genres = []
        if data:
            for genre_id in data:
                genres.append(Genre.get_by_id(genre_id[0]))

        return genres

    def get_countries(self):
        query = "SELECT idCountry FROM FilmsCountries WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        countries = []
        if data:
            for country_id in data:
                countries.append(Country.get_by_id(country_id[0]))

        return countries

    def get_studios(self):
        query = "SELECT idStudio FROM FilmsStudios WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        studios = []
        if data:
            for studio_id in data:
                studios.append(Studio.get_by_id(studio_id[0]))

        return studios

    @staticmethod
    def get_film_count():
        query = "SELECT COUNT(id) from Films"
        data = db.db_select(query, [])

        return data[0][0]

    def get_actors(self):
        query = "SELECT idActor FROM FilmsActors WHERE idFilm = ?"
        data = db.db_select(query, [self.id])

        actors = []
        if data:
            for actor_id in data:
                actors.append(Actor.get_by_id(actor_id[0]))

        return actors

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Films WHERE id = ?"
        data = db.db_select(query, [id])

        if data:
            film_data = data[0]
            return Film(film_data[0], film_data[1], film_data[2], film_data[3], film_data[4], film_data[5])

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Films WHERE name = ?"

        try:
            data = db.db_select(query, [name])
            film_data = data[0]
        except:
            logging.error("failed to get by name")

        if data:
            return Film(film_data[0], film_data[1], film_data[2], film_data[3], film_data[4], film_data[5])

    @staticmethod
    def get_page(n):
        i = 1 + 20 * (n - 1)
        film = Film.get_by_id(i)
        films = []

        while film and (i - 20 * (n - 1)) < 20:
            films.append(film)
            i = i + 1
            film = Film.get_by_id(i)

        return films


class Studio:
    def __init__(self, id, name, wikiLink, dateFound):
        self.id = id
        self.name = name
        self.wikiLink = wikiLink
        self.dateFound = dateFound

    def get_films(self):
        query = "SELECT idFilm FROM FilmsStudios WHERE idStudio = ?"
        data = db.db_select(query, [self.id])

        films = []
        if data:
            for film_id in data:
                films.append(Film.get_by_id(film_id[0]))

        return films

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Studios WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            studio_data = data[0]
            return Studio(studio_data[0], studio_data[1], studio_data[2], studio_data[3])


class Actor:
    def __init__(self, id, surname, name, wikiLink, genderId, dateBirth):
        self.id = id
        self.surname = surname
        self.name = name
        self.wikiLink = wikiLink
        self.genderId = genderId
        self.dateBirth = dateBirth

    def get_countries(self):
        query = "SELECT idCountry FROM ActorsCountries WHERE idActor = ?"
        data = db.db_select(query, [self.id])

        countries = []
        if data:
            for country_id in data:
                countries.append(Country.get_by_id(country_id[0]))

        return countries

    def get_films(self):
        query = "SELECT idFilm FROM FilmsActors WHERE idActor = ?"
        data = db.db_select(query, [self.id])

        films = []
        if data:
            for film_id in data:
                films.append(Film.get_by_id(film_id[0]))

        return films

    @staticmethod
    def get_actors_count():
        query = "SELECT COUNT(id) from Actors"
        data = db.db_select(query, [])

        return data[0][0]

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Actors WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            actor_data = data[0]
            return Actor(actor_data[0], actor_data[1], actor_data[2], actor_data[3], actor_data[4], actor_data[5])


class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_films(self):
        query = "SELECT idFilm FROM FilmsGenres WHERE idGenre = ?"
        data = db.db_select(query, [self.id])

        films = []
        if data:
            for film_id in data:
                films.append(Film.get_by_id(film_id[0]))

        return films

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Genres WHERE name = ?"

        try:
            data = db.db_select(query, [name])
            genre_data = data[0]
        except:
            logging.error("failed to get by name")

        if data:
            return Genre(genre_data[0], genre_data[1])

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Genres WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            genre_data = data[0]
            return Genre(genre_data[0], genre_data[1])

    @staticmethod
    def get_all_genres():
        i = 1
        genre = Genre.get_by_id(i)
        genres = []

        while genre:
            genres.append(genre)
            i = i + 1
            genre = Genre.get_by_id(i)

        return genres


class Country:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_films(self):
        query = "SELECT idFilm FROM FilmsCountries WHERE idCountry = ?"
        data = db.db_select(query, [self.id])

        films = []
        if data:
            for film_id in data:
                films.append(Film.get_by_id(film_id[0]))

        return films

    def get_actors(self):
        query = "SELECT idActor FROM ActorsCountries WHERE idCountry = ?"
        data = db.db_select(query, [self.id])

        actors = []
        if data:
            for actor_id in data:
                actors.append(Actor.get_by_id(actor_id[0]))

        return actors

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Countries WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            country_data = data[0]
            return Country(country_data[0], country_data[1])

    @staticmethod
    def get_by_name(name: str):
        query = "SELECT * FROM Countries WHERE name = ?"

        try:
            data = db.db_select(query, [name])
            country_data = data[0]
        except:
            logging.error("failed to get by name")

        if data:
            return Country(country_data[0], country_data[1])

    @staticmethod
    def get_all_countries():
        i = 1
        country = Country.get_by_id(i)
        countries = []

        while country:
            countries.append(country)
            i = i + 1
            country = Country.get_by_id(i)

        return countries


class Gender:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_by_id(id: int):
        query = "SELECT * FROM Genders WHERE id = ?"
        data = db.db_select(query, [id])
        if data:
            gender_data = data[0]
            return Gender(gender_data[0], gender_data[1])

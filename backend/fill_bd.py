from init import db


def initial_fill():
    db.fill_from_csv(csv_path="csv_base/genders.csv", tablename="Genders")
    db.fill_from_csv(csv_path="csv_base/genres.csv", tablename="Genres")
    db.fill_from_csv(csv_path="csv_base/countries.csv", tablename="Countries")
    db.fill_from_csv(csv_path="csv_base/studios.csv", tablename="Studios")

    db.fill_from_csv(csv_path="csv_base/films.csv", tablename="Films")
    db.fill_from_csv(csv_path="csv_base/actors.csv", tablename="Actors")

    db.fill_from_csv(csv_path="csv_base/actorscountries.csv", tablename="ActorsCountries")
    db.fill_from_csv(csv_path="csv_base/filmscountries.csv", tablename="FilmsCountries")
    db.fill_from_csv(csv_path="csv_base/filmsgenres.csv", tablename="FilmsGenres")
    db.fill_from_csv(csv_path="csv_base/filmsstudios.csv", tablename="FilmsStudios")
    db.fill_from_csv(csv_path="csv_base/filmsactors.csv", tablename="FilmsActors")


if __name__ == '__main__':
    initial_fill()

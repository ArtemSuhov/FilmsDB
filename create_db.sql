CREATE TABLE Films
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  budget INT,
  rating INT,
  dateFound DATE
);

CREATE TABLE Genders
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE Actors
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surname VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  wikiLink VARCHAR(255),
  genderId INT NOT NULL,
  dateBirth DATE,
  FOREIGN KEY (genderId) REFERENCES Genders (id)
);

CREATE TABLE Countries
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE Studios
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,
  wikiLink VARCHAR(255),
  dateFound DATE
);

CREATE TABLE Genres
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE FilmsActors
(
  idFilm INT NOT NULL,
  idActor INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id),
  FOREIGN KEY (idActor) REFERENCES Actors (id)
);

CREATE TABLE ActorsCountries
(
  idActor INT NOT NULL,
  idCountry INT NOT NULL,
  FOREIGN KEY (idActor) REFERENCES Actors (id),
  FOREIGN KEY (idCountry) REFERENCES Countries (id)
);

CREATE TABLE FilmsStudios
(
  idFilm INT NOT NULL,
  idStudio INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id),
  FOREIGN KEY (idStudio) REFERENCES Studios (id)
);

CREATE TABLE FilmsCountries
(
  idFilm INT NOT NULL,
  idCountry INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id),
  FOREIGN KEY (idCountry) REFERENCES Countries (id)
);

CREATE TABLE FilmsGenres
(
  idFilm INT NOT NULL,
  idGenre INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id),
  FOREIGN KEY (idGenre) REFERENCES Genres (id)
);

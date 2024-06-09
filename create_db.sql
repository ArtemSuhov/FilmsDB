-- Таблица фильмов
CREATE TABLE Films
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  budget INT,
  rating REAL,
  dateFound TEXT
);

-- Таблица полов
CREATE TABLE Genders
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

-- Таблица актеров
CREATE TABLE Actors
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surname VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  wikiLink VARCHAR(255),
  genderId INT NOT NULL,
  dateBirth TEXT,
  FOREIGN KEY (genderId) REFERENCES Genders (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица стран
CREATE TABLE Countries
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

-- Таблица студий
CREATE TABLE Studios
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,
  wikiLink VARCHAR(255),
  dateFound TEXT
);

-- Таблица жанров
CREATE TABLE Genres
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL
);

-- Таблица связывающая фильмы и актеров
CREATE TABLE FilmsActors
(
  idFilm INT NOT NULL,
  idActor INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idActor) REFERENCES Actors (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица связывающая актеров и страны
CREATE TABLE ActorsCountries
(
  idActor INT NOT NULL,
  idCountry INT NOT NULL,
  FOREIGN KEY (idActor) REFERENCES Actors (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idCountry) REFERENCES Countries (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица связывающая фильмы и студии
CREATE TABLE FilmsStudios
(
  idFilm INT NOT NULL,
  idStudio INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idStudio) REFERENCES Studios (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица связывающая фильмы и страны
CREATE TABLE FilmsCountries
(
  idFilm INT NOT NULL,
  idCountry INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idCountry) REFERENCES Countries (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица связывающая фильмы и жанры
CREATE TABLE FilmsGenres
(
  idFilm INT NOT NULL,
  idGenre INT NOT NULL,
  FOREIGN KEY (idFilm) REFERENCES Films (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idGenre) REFERENCES Genres (id) ON DELETE CASCADE ON UPDATE CASCADE
);

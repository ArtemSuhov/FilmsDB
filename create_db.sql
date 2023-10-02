CREATE TABLE Films
(
  	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,  
    name VARCHAR(255) NOT NULL,
  	description TEXT,
    budget INT,
  	rating INT,
	dateFound DATE
);

CREATE TABLE Genders
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Actors
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    surname VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
  	wikiLink VARCHAR(255),
  	genderId INT NOT NULL,
  	dateBirth DATE,
    FOREIGN KEY (genderId) REFERENCES Genders (id),
);

CREATE TABLE Countries
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Studios
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
  	wikiLink VARCHAR(255),
  	dateFound DATE
);

CREATE TABLE Genres
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
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
  	Foreign key (idActor) references Actors (id),
    foreign key (idCountry) references Countries (id)
);

CREATE TABLE FilmsStudios
(
    idFilm INT NOT NULL,
    idStudio INT NOT NULL,
    FOREIGN KEY (idFilm) REFERENCES Films (id),
  	foreign key (idStudio) references Studios (id)
);

CREATE TABLE FilmsCountries
(
    idFilm INT NOT NULL,
    idCountry INT NOT NULL,
  	FOREIGN KEY (idFilm) REFERENCES Films (id),
  	foreign key (idCountry) references Countries (id)
);

CREATE TABLE FilmsGenres
(
    idFilm INT NOT NULL,
    idGenre INT NOT NULL,
    FOREIGN KEY (idFilm) REFERENCES Films (id),
  	foreign key (idGenre) references Genres (id)
);

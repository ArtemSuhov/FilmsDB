# FilmsDB
The functionality of the film database includes the following features:

Storing films: the database allows users to store information about films such as title, director, year of release, genre, actors and other additional data.

Film Search: users can search for films by title and within genres.

Film Details: the database can contain detailed information about each film, including plot description, trailers, posters and other additional information.

Film Search Export: allows you to export films and actors from the Film Search service.

In this way, the film database functionality helps you manage information about films.

# Usage:
py run_web.py
The service runs on localhost:5000

Administration via file - admin.py

---

**Admin Tool for Managing Films and Actors**

This admin tool provides functionality to manage films and actors in the database. It interacts with the Kinopoisk API to fetch film and actor details.

**Usage:**

1. **Adding a Film:**
   - Command: `add_film <name> <description> <budget> <rating> <dateFound>`
   - Example: `add_film "The Shawshank Redemption" "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency." 25000000 9.3 "1994-10-14"`

2. **Adding a Film from Kinopoisk:**
   - Command: `add_film_kp <id_kp>`
   - Example: `add_film_kp 111`

3. **Deleting a Film:**
   - Command: `del_film <id>`
   - Example: `del_film 1`

4. **Editing Film Details:**
   - Command: `edit_film <id> [name=<new_name>] [description=<new_description>] [budget=<new_budget>] [rating=<new_rating>] [dateFound=<new_dateFound>]`
   - Example: `edit_film 1 name="New Title" rating=8.5`

5. **Adding an Actor:**
   - Command: `add_actor <surname> <name> <wikiLink> <genderId> <dateBirth>`
   - Example: `add_actor "Hanks" "Tom" "https://en.wikipedia.org/wiki/Tom_Hanks" 1 "1956-07-09"`

6. **Adding an Actor from Kinopoisk:**
   - Command: `add_actor_kp <id_kp>`
   - Example: `add_actor_kp 123`

7. **Deleting an Actor:**
   - Command: `del_actor <id>`
   - Example: `del_actor 1`

8. **Editing Actor Details:**
   - Command: `edit_actor <id> [surname=<new_surname>] [name=<new_name>] [wikiLink=<new_wikiLink>] [genderId=<new_genderId>] [dateBirth=<new_dateBirth>]`
   - Example: `edit_actor 1 name="Thomas"`

9. **Help:**
   - Command: `?`
   - Example: `?`

10. **Quitting the Admin Tool:**
    - Command: `quit`

**Note:** 
- For commands that involve adding or editing entities, use the appropriate parameters as specified. 
- GenderId: 1 for male, 2 for female.
- Date format: YYYY-MM-DD.

--- 


# ToDoList:
- Внедрить в UI (шаблоны) фильтр фильмов

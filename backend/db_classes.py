from init import db

#Rating filter - film
#genres filter - film
class Film:
    def __init__(self, id, name, description, budget, rating, dateFound):
        self.id = id
        self.name = name
        self.description = description
        self.budget = budget
        self.rating = rating
        self.dateFound = dateFound


    @staticmethod
    def get_by_id(id):
        query = "SELECT * FROM Films WHERE id = %s"
        user_data = db.db_select(query, id)
        if user_data:
            return Film(*user_data[0])

    @staticmethod
    def get_by_name(name):
        query = "SELECT * FROM Films WHERE name = %s"
        user_data = db.db_select(query, name)
        if user_data:
            return Film(*user_data[0])


class Studio:
    def __init__(self, id, name, wikiLink, dateFound):
        self.id = id
        self.name = name
        self.wikiLink = wikiLink
        self.dateFound = dateFound

    @staticmethod
    def get_by_id(id):
        query = "SELECT * FROM Studios WHERE id = %s"
        patient_data = db.db_select(query, id)
        if patient_data:
            return Studio(*patient_data[0])


class Actor:
    def __init__(self, id, surname, name, wikiLink, genderId, dateBirth):
        self.id = id
        self.surname = surname
        self.name = name
        self.wikiLink = wikiLink
        self.genderId = genderId
        self.dateBirth = dateBirth

    @staticmethod
    def get_by_id(id):
        query = "SELECT * FROM Actors WHERE id = %s"
        patient_data = db.db_select(query, id)
        if patient_data:
            return Studio(*patient_data[0])


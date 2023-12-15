from database import Database
import  logging

db = Database('filmoteka.db')
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

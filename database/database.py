"""
This module handles the communication with the applications database.

Product -- GGPT
https://github.com/Knaeckebrothero/Projekt-GGPT
App ID -- 616160
https://developer.riotgames.com/
"""
import logging
import pymongo
from pymongo.server_api import ServerApi
from dataclasses import asdict

from development.get_credentials import read_config


# Splits a list into smaller lists
def divide_chunks(mylist: list, chunksize: int):
    # Loops till length of mylist
    for i in range(0, len(mylist), chunksize):
        yield mylist[i:i + chunksize]


# Defines a custom logger, login into a log file.
def configure_custom_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler("./development/db.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(read_config('loggingLevel'))
    return logger


# Class containing all the attributes and methods used to communicate with the database.
class Database:
    def __init__(self, role: str, password: str):
        self._logger = configure_custom_logger()
        self._client = pymongo.MongoClient("mongodb+srv://{}:{}@projekt-analysistool.pfdmf3o."
                                           "mongodb.net/" "?retryWrites=true&w=majority"
                                           .format(role, password, server_api=ServerApi('1')))
        self._database = self._client['riotdata']
        self._logger.log(10, 'Connection established, class initiated')

    def retrieve_match_ids(self):
        pass

    # Inserts a list of dataclasses into the database.
    def insert_loldata(self, list_dataclasses: list[object], collection: str):
        # Variables
        dataclass_type = type(list_dataclasses[0])
        list_dicts = []

        self._logger.log(10, 'Converting objects to dictionarys...')
        # Converts the dataclasses to dictionaries before inserting them into the database.
        for match in list_dataclasses:
            # Checks if all objects are of the same type
            if not type(match) == dataclass_type:
                self._logger.log(30, 'Given list contains different objects')
                return
            # Converts object
            list_dicts.append(asdict(match))
        self._logger.log(10, 'Done converting')

        # Checks if the list needs to be chunked
        col = self._database[collection]
        if len(list_dicts) > 25:
            for chunk in divide_chunks(list_dicts, 25):
                self._logger.log(10, 'Inserting 25 objects...')
                col.insert_many(chunk)
                self._logger.log(10, 'Objects inserted')
        else:
            self._logger.log(10, 'Inserting objects...')
            col.insert_many(list_dicts)
        self._logger.log(10, 'Done inserting')

    # Retrieves a list of dataclasses from the database.
    def retrieve_objects(self, collection: str, size: int):
        pass

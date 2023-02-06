from sqlite3 import connect
from os.path import exists
from os import remove
from libs.jsonData import *

import string
import random

class Database:
    @staticmethod
    def dbpath():
        return "./database/bank.db"

    def __get_id(self, limit=10) -> str:
        if limit == 0:
            return None

        length = random.randint(4, 10)
        characters = string.ascii_letters + string.digits
        id = ''.join(random.choice(characters) for i in range(length))

        if not self.__is_unique(id):
            id = self.__get_id(limit-1)

        return id

    def __is_unique(self, id) -> bool:
        found = self.cursor.execute(f"""
        SELECT id FROM clients WHERE id='{id}'
        """).fetchone()

        if found is None:
            return True
        
        return False

    def __connect_database(self):
        self.db = connect(self.dbpath())
        self.cursor = self.db.cursor()

    def __init__(self):
        if not exists(self.dbpath()):
            self.__connect_database()
            self.cursor.execute("CREATE TABLE clients(client, money, id)")
            self.cursor.execute("CREATE TABLE logins(login, psk, id)")
        else:
            self.__connect_database()
        print(self.cursor.execute("SELECT * FROM clients").fetchall())

    def login(self, client: login_json) -> tuple[client_json, login_json] | tuple[None, None]:
        data = client.extract()
        login = data["login"]
        psk = data["psk"]

        if len(login) == 0 or len(psk) == 0:
            print("Empty Fields")
            return
        
        l_data = self.__get_from_logins(login, psk)

        if l_data is None:
            return None, None
        
        c_data = self.__get_from_clients(l_data['id'])

        return client_json(c_data), login_json(l_data)
    
    def add_client(self, l_json: login_json, c_json: client_json) -> tuple[client_json, login_data] | None:
        login = l_json.extract()
        client = c_json.extract()

        login_str = login["login"]
        psk_str = login["psk"]
        name_str = client["name"]
        money_str = client["money"]

        if self.__has_login(login_str):
            print('There is already an account with this login')
            return None

        send_c_data, send_l_data = self.__insert(name_str, login_str, psk_str, money_str)

        return client_json(send_c_data), login_json(send_l_data)

    def withdraw(self, client: login_json, amount: float) -> client_json | None:
        data = login_data(dictionary=client.extract())
        client = self.__get_from_clients(data['id'])

        if client is None:
            return None

        return self.__update_client(data['id'], float(client['money'])-amount)
    
    def deposit(self, client: login_json, amount: float) -> client_json | None:
        data = login_data(dictionary=client.extract())
        client = self.__get_from_clients(data['id'])

        if client is None:
            return None

        return self.__update_client(data['id'], float(client['money'])+amount)

    def delete_account(self, l_json: login_json) -> None:
        l_data = login_data(dictionary=l_json.extract())

        self.__remove(l_data['id'])

    def __get_from_clients(self, id: str) -> client_data | None:
        all_clients = self.cursor.execute(f"""
        SELECT * FROM clients
        """).fetchall()

        client = self.cursor.execute(f"SELECT * FROM clients WHERE id='{id}'").fetchone()

        return client_data(client[-3], client[-2])

    def __has_login(self, login: str) -> bool:
        client = self.cursor.execute(f"""SELECT * FROM logins WHERE login='{login}'""").fetchone()
        if client is None:
            return False
        
        return True

    def __get_from_logins(self, login:str, psk:str) -> login_data| None:
        client = self.cursor.execute(f"SELECT * FROM logins WHERE login='{login}' AND psk='{psk}'").fetchone()
        if client is None:
            return None

        return login_data(client[-3], client[-2], client[-1])

    def __insert(self, name: str, login: str, psk: str, money: float) -> tuple[client_data, login_data] | None:
        id = self.__get_id()

        if id is None:
            print("Couldn't get a unique id")
            return None

        self.cursor.execute(f"""
        INSERT INTO logins VALUES ('{login}', '{psk}', '{id}')
        """)
        val = self.cursor.execute(f"""
        INSERT INTO clients VALUES ('{name}', {money}, '{id}')
        """)
        self.db.commit()
        return client_data(name, money), login_data(login, psk, id)

    def __remove(self, id: str) -> None:
        self.cursor.execute(f"""
        DELETE FROM logins WHERE id='{id}'
        """)
        self.cursor.execute(f"""
        DELETE FROM clients WHERE id='{id}'
        """)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()
        return
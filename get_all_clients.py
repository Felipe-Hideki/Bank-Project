from sqlite3 import connect
from libs.DatabaseFuncs import Database

file_location = "./db.log"

if __name__ == '__main__':
    db = connect(Database.dbpath())
    cursor = db.cursor()

    clients = cursor.execute(f"""
    SELECT * FROM clients
    """).fetchall()

    logins = cursor.execute(f"""
    SELECT * FROM logins
    """).fetchall()

    try:
        file = open(file_location, 'w')

        file.write("clients { \n")
        
        for index in range(len(clients)):
            client, money, id = clients[index]
            login, psk, id = logins[index]
            file.write(f"    {client}(money: {money}, id: {id}) //// (login: {login}, psk: {psk}, id: {id})')\n")

        file.write("}")
        print("All clients registered at " + file_location)
    finally:
        file.close()
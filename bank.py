from libs.DatabaseFuncs import Database
from libs.jsonData import *
from libs.utils import clear

class App:
    def __init__(self):
        self.db = Database()
    
    def try_login(self, login: str, psk: str) -> tuple[client_data, login_data] | tuple[None, None]:
        send_data = login_json(login_data(login, psk))
        
        c_json, l_json = self.db.login(send_data)
        if c_json is None or l_json is None:
            return None, None

        c_data = client_data(dictionary=c_json.extract())
        l_data = login_data(dictionary=l_json.extract())
        
        return c_data, l_data

    def deposit(self):
        res = input("Enter 'cancel' if you want to cancel the operation\nValue to deposit: ")
        if res == 'cancel':
            return
        try:
            val = float(res)
        except:
            print('Inputted value isnt a number')
            return
        if val < 0:
            print('Trying to deposit a negative value\nOperation Failed')
            return
        returned = self.db.deposit(login_json(self.__l_data), val)
        if returned == None:
            print('Operation Failed')
            return
        self.__c_data = client_data(dictionary=returned.extract())

    def withdraw(self):
        res = input("Enter 'cancel' if you want to cancel the operation\nValue to withdraw: ")
        if res == 'cancel':
            return
        try:
            val = float(res)
        except:                    
            print('Inputted value isnt a number')
            return
        if self.__c_data['money'] - val < 0:
            print('Insuficient funds\nOperation Failed')
            return
        returned = self.db.withdraw(login_json(self.__l_data), val)
        if returned == None:
            print('Operation Failed')
            return
        self.__c_data = client_data(dictionary=returned.extract())

    def Delete_account(self):
        clear()

        print("Login again to confirm the deletion of the account")
        login = input("Login: ")
        psk = input("Password: ")

        send_l_json = login_json(login_data(login, psk))
        response_c_json, response_l_json = self.db.login(send_l_json)
        if response_l_json is None:
            print("Incorrect Credentials")
            input("Press enter to continue")
            return
        
        self.db.delete_account(response_l_json)

        self.logout()

    def logout(self):
        self.__c_data = None
        self.__l_data = None

    def parse_choice(self, choice: int) -> None:
        clear()
        try:
            choice = int(choice)
        except:
            print("Inputted value is not a number")
            return

        match(choice):
            case 1:
                self.deposit()
            case 2:
                self.withdraw()
            case 3:
                self.Delete_account()
            case 4:
                self.logout()
                return
            case _:
                return
        input("Press enter to continue")

    def loop(self):
        self.__continue = True
        self.__c_data = None
        self.__l_data = None

        while self.__continue:
            clear()
            print("Bank Bank")
            if self.__c_data is None:
                print("1 - Login\n2 - Register\n3 - Exit")
                res = input()
                
                try:
                    res = int(res)
                except:
                    print("Inputted value is not a number")
                    input('Press enter to try again')
                    continue

                clear()
                match(res):
                    case 1:
                        print("Please login into your account:")
                        login = input("Login: ")
                        psk = input("Password: ")
                        self.__c_data, self.__l_data = self.try_login(login, psk)

                        if self.__c_data is None:
                            print('Incorrect Login or Password')
                            input('Press enter to try again')
                            continue
                        print(f'you are logged in {self.__c_data["name"]}, you have a total of {"{:.2f}".format(self.__c_data["money"])} moneys')
                        input('Press enter to continue')
                        continue
                    case 2:
                        while(True):
                            clear()
                            print("Answer the questions below")
                            info = {}
                            info["login"] = input("Login: ")
                            info["psk"] = input("Password: ")
                            info["name"] = input("Your name: ")
                            print("Everything is correct?[y/n]")
                            if input() == "y":
                                break
                        returned = self.db.add_client(login_json(login_data(info["login"], info["psk"])), client_json(client_data(info["name"], 0)))
                        if returned is None:
                            print("Failed to register client\nOperation Failed")
                            input('press enter to continue')
                        else:
                            self.__c_data, self.__l_data = self.try_login(info["login"], info["psk"])
                            if self.__c_data is None or self.__l_data is None:
                                print("Login after register failed\nOperation Failed")
                                input('press enter to continue')
                        continue
                    case 3:
                        self.__continue = False
                        continue
                    case _:
                        continue


            print(f'you are logged in {self.__c_data["name"]}, you have a total of {self.__c_data["money"]} moneys')
            print("Select action:\n1 - Deposit\n2 - Withdraw\n3 - Delete account\n4 - Logout")
            res = input()
            self.parse_choice(res)

if __name__ == '__main__':
    app = App()

    try:
        app.loop()
    finally:
        app.db.close()
        pass
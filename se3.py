# Mozhdeh Shakerian
# 40025028
# I used ChatGPT in the final version of my code to fix bugs and improve the style.



import csv

class Person:
    def __init__(self, username, password, age, wallet=0.0, address=""):
        self.username = username
        self.password = password
        self.age = age
        self.wallet = wallet
        self.address = address

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "age": self.age,
            "wallet": self.wallet,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        return Person(
            username=data["username"],
            password=data["password"],
            age=data["age"],
            wallet=float(data["wallet"]),
            address=data["address"]
        )
class UserManager:
    def __init__(self, filename='users.csv'):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = Person.from_dict(row)
                    users[user.username] = user
        except FileNotFoundError:
            pass
        return users

    def save_users(self):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ["username", "password", "age", "wallet", "address"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.users.values():
                writer.writerow(user.to_dict())

    def sign_up(self, username, password, age, wallet, address):
        if username in self.users:
            print("Username already exists. Please choose another username.")
            return False

        person = Person(username, password, age, wallet, address)
        self.users[username] = person
        self.save_users()
        print(f"User {username} created successfully.")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            print(f"Welcome, {username}!")
            return self.users[username]
        else:
            print("Invalid username or password.")
            return None

    def recharge_wallet(self, user, amount):
        user.wallet += amount
        self.save_users()
        print(f"New wallet balance: {user.wallet}")

    def edit_address(self, user, new_address):
        if not new_address:
            print("Address cannot be empty.")
            return False

        if "city" not in new_address:
            print("City must be included in the address.")
            return False

        if "street" not in new_address:
            print("Street must be included in the address.")
            return False

        user.address = new_address
        self.save_users()
        print(f"New address: {user.address}")
        return True
class OnlineStore:
    def __init__(self):
        self.user_manager = UserManager()

    def main_menu(self):
        while True:
            print("\n1. Sign Up")
            print("2. Login")
            choice = input("Choose an option (1 or 2): ")

            if choice == '1':
                self.sign_up()
            elif choice == '2':
                user = self.login()
                if user:
                    self.user_menu(user)
            else:
                print("Invalid choice. Please select 1 or 2.")

    def sign_up(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        age = input("Enter your age: ")
        wallet = 0.0
        address = input("Enter your address (city, street, house number): ")
        self.user_manager.sign_up(username, password, age, wallet, address)

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        return self.user_manager.login(username, password)

    def user_menu(self, user):
        while True:
            print("\n1. Recharge Wallet")
            print("2. Edit Address")
            print("3. Logout")
            choice = input("Choose an option (1, 2, or 3): ")

            if choice == '1':
                amount = float(input("Enter amount to recharge: "))
                self.user_manager.recharge_wallet(user, amount)
            elif choice == '2':
                new_address = input("Enter new address (city, street, house number): ")
                self.user_manager.edit_address(user, new_address)
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
if __name__ == "__main__":
    store = OnlineStore()
    store.main_menu()

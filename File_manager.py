from cryptography.fernet import Fernet as fr #knihovna pro kodování a dekodování
import os #knihovna pro zjištění current direkrorii a přistup k souborům projektu v current direkrorii
#vytvoření classu
class My_pass_manager:
    def __init__(self): #konstrukter
        self.key = None # pro chování kliče
        self.pass_dickt = {} # pro chování webů a hesel k ním
        self.pass_web = None # pro chování jména souboru do ktérého se zapíše zakodováná hesla
    def create_key(self): #vytvoření kliče pro kodování a zapis jeho do souboru
        key = fr.generate_key()
        with open("key.key", 'wb') as f:
            f.write(key)
    def load_key(self): #nahrání kliče ze souboru (do proměnné classa self.key) pokud ten existuje
        try:
            with open('key.key', 'rb') as f:
                self.key = f.read()
        except FileNotFoundError:
            print('File with key was not created')
    def new_pass_file(self, file_name, password = None): #vytvoření souboru pro chování zakodováných hesel a předání tam už existujicí hesla
        self.pass_web = file_name #zápis argumentu do proměnné classu
        if self.pass_web is not None: #pokud dictionary není prazdný a obsahuje v sobě nějaká data s weby a hesly tak musíme ho vynulovat (udělat prázdným)
            self.pass_dickt = {}
        if password:
            for keys, values in password.items(): #iterace po existujicímu dictionary s hesly
                self.add_pass(keys, values)
    def add_pass(self, web, password): #přidání webu a hesla k němu do proměnné classu dictionary a zapis těch údajů do uvedeného souboru (pokud ten jěště neexistuje, vytvoří se) v zakodováné formě
        self.pass_dickt[web] = password
        with open(self.pass_web, 'a') as f: #a - append, ne přepsání celého souboru ale přidávaní tam nových údajů
            cod = fr(self.key).encrypt(password.encode()) #převědení hesla do binární proměnné (požaduje funkce encrypt()) a jeho kodování pomoce už vytvořeného kliče
            f.write(web + ':' + cod.decode() + '\n') #převedení z binární do normální formy
    def load_pass_file(self): #nahrávaní už existujicího souboru (bereme direction souboru z už zapsáného souboru do proměnné self.pass_web) do proměne classu dictionary v dekodováné formě
        if self.pass_web:
            with open(self.pass_web, 'r') as f:
                for line in f:
                    web, passw = line.split(':') #rozdelujeme web a heslo pomocí znaku ':'
                    self.pass_dickt[web] = fr(self.key).decrypt(passw.encode()).decode() #dekodování hesla ze souboru pomoci už vytvořeného klíče
        else:
            print('You have not created file to load')
    def load_ex_file(self, name): #nahrávání údajů ze složky name do proměmé classu dictionary v dekodováné formě a update promněnné self.pass_web
        try:
            self.pass_web = name
            with open(name, 'r') as ff:
                for line in ff:
                    web, passw = line.split(':')
                    self.pass_dickt[web] = fr(self.key).decrypt(passw.encode()).decode()
        except FileNotFoundError:
            print('No file in this directory')
    def get_pass(self, web): # ziskání hesla podle uvedeného kliče web (ziskání hesla uvedeného webu)
        return self.pass_dickt[web]
    def get_web(self): # přistup k proměnné self.pass_web
        return self.pass_web

person1 = My_pass_manager() # vytvoření objektu classu My_pass_manager
# vytvoření proměné typu dictionary s zakladnými weby a hesly k ním:
dict_of_pass = {
    'facebook':'mypass1',
    'mail':'mypass2',
    'twiter':'mypass3',
    'snapchat':'mypass4'
}
# Menu pro interakci s uživatelem:
print("""Chose the action
1. Create a new key
2. Load a key (do before any other action if you've already created a key)
3. Create new password file
4. Add new password into file
5. Load created password file
6. Load password from existing file
7. Get a password
8. Exit
""")
# Cyklus while a provedení činnosti podle volby uživatele zapsané do proměnné choice:
while True:
    choice = int(input('Enter your choice: '))
    if choice == 1:
        person1.create_key()
    elif choice == 2:
        person1.load_key()
    elif choice == 3:
        tem = input('Enter the name of file: ')
        person1.new_pass_file(tem, dict_of_pass) # předávaní do funkce parametrů tem, dict_of_pass
    elif choice == 4:
        web, pas = input('Enter the name of web and password: ').split()
        person1.add_pass(web, pas)
    elif choice == 5:
        person1.load_pass_file()
    elif choice == 6:
        try:
            curdir = os.getcwd() #getting current directory
            s = os.listdir(curdir) #all files in current directory
            dd = [i for i in s if '.txt' in i]
            for j in dd:
                print(j) #volíme který coubor otevřit pro práci s ním
            bufer = input('From which file would you like to load passwords? ')
            person1.load_ex_file(bufer)
        except TypeError:
            print('key was not loaded')
    elif choice == 7:
        if person1.get_web():
            buf = input('Enter password of which web you want to get: ')
            print(person1.get_pass(buf))
        else:
            print('No loaded file')
    elif choice == 8: # přikaz break uzavře cyklus
        break
    else:
        print('Error input')
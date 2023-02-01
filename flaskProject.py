from flask import Flask
from flask import request
import sys
import csv

#Création de notre application flask
app = Flask(__name__)


#classe Person qui prend en compte deux attributs name et balance. 2 methodes sont mises en place
#debit et credit
class Person:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        
    def __str__(self):
        return f"Person({self.name}, {self.balance})"
    
    def debit(self, amount):
        self.balance -= amount
        
    def credit(self, amount):
        self.balance += amount

#classe transaction qui a 3 attributs sender, recipent et amount 
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
    
    def __str__(self):
        return f"Transaction({self.sender}, {self.recipient}, {self.amount})"

   
#creation des deux tables persons et transactions qui seront remplies des infos recupérées du fichier csv fourni
persons = []
transactions = []

#recupérer les infos du fichiers csv
def load_data_from_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            sender, recipient, amount = row
            sender_person = next((p for p in persons if p.name == sender), None)
            if not sender_person:
                sender_person = Person(sender, 0)
                persons.append(sender_person)
            recipient_person = next((p for p in persons if p.name == recipient), None)
            if not recipient_person:
                recipient_person = Person(recipient, 0)
                persons.append(recipient_person)
            transaction = Transaction(sender, recipient, int(amount))
            transactions.append(transaction)
            sender_person.debit(int(amount))
            recipient_person.credit(int(amount))

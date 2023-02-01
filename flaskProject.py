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
            
            
#Création des comptes
p1=Person("Mouad",2000)
p2=Person("Mohammed",6000)
p3=Person("Sisi",2500)
p4=Person("Nic",3500)
p5=Person("yassine",8000)
p6=Person("simo",100)

#création des transactions
t1=Transaction(p1,p2,100)
t2=Transaction(p2,p5,200)
t3=Transaction(p4,p3,200)

#Création des listes : "personne" contenant des objets de type "Personne" et "transaction" contenant des objets de type "Transaction" 
personnes=[p1,p2,p3,p4,p5,p6]
_transactions=[t1,t2,t3]

#Définition de la route principale de l'application, uniquement accessible via une requête HTTP GET pour récupérer des données.
@app.route("/", methods=['GET'])
def printAll():
    if request.method == 'GET':
        res = "<h1>Liste des personnes :</h1><ul>"
        for person in personnes:
            res += "<li>NOM : " + person.name  + " / SOLDE COMPTE : " + '%.2f' % person.balance + "€</li>"
        res += "</ul><h1>Liste des transactions :</h1><ul>"
        #for transaction in _transactions:
        res += "<li>P1 : " + p1.name +  " / P2 : " + p2.name+  ":   Montant de la transaction : 100€  : " 
        res += "<li>P1 : " + p2.name +  " / P2 : " + p5.name+  ":   Montant de la transaction : 200€  : " 
        res += "<li>P1 : " + p4.name +  " / P2 : " + p3.name+  ":   Montant de la transaction : 200€  : " 

        return res+"</ul>"
    else:
        return "Invalid request method"

from datetime import datetime
from otp_verification import startOtpProcedure
from send_reservation_confirm import sendReservationConfirm

# Server connection
from argparse import _MutuallyExclusiveGroup
from multiprocessing.sharedctypes import Value
from sqlite3 import Cursor
from sre_compile import isstring
from sys import excepthook
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='sqluser',
    password='password',
    database='court_management'
)
mycursor = mydb.cursor()
opening_hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

class Reservations:
    def __int__(self, date, hour, court, email):
        self.date = date
        self.hour = hour
        self.court = court
        self.email = email

    def startChat():
        print(f"Chatbot: Welcome to the Tennis Court Reservation System")
        print(f"Chatbot: Please enter your personal data first")
        print(f"Chatbot: Fill in your name")
        name = input(f"You: ")
        print(f"Chatbot: Fill in your surname")
        surname = input(f"You: ")
        email = getEmailFromUser()
        if checkUserInDatabase(name, surname, email) == False:
            addUserToDatabase(name, surname, email) 
        searched_date = selectDate()
        selected_time= str(selectTime(searched_date))
        startOtpProcedure(email)
        court_number = addCourtNumber(selected_time, searched_date)
        if addReservationToDatabase(email, searched_date, selected_time, court_number) == True:
            sendReservationConfirm(name, surname, searched_date, selected_time, email, court_number)
            print(f"Chatbot: Reservation made successfully, check your email for details")

def checkUserInDatabase(name, surname, email):
    mycursor.execute(
        "SELECT client_email FROM Clients WHERE client_email = %s", (email, )
    )
    if len(mycursor.fetchall()) == 0:
        if addUserToDatabase(name, surname, email) == True:
            return True
    else:
        print(f"Chatbot: I see you are already our client please enter your password")
        if verifyPassword(email) == True:
            print(f"Chatbot: Password correct!")
            return True

def verifyPassword(email):
    mycursor.execute(
        "SELECT password FROM Clients WHERE client_email = %s", (email, )
    )
    password = mycursor.fetchone()[0]
    input_password = input(f"Password: ")
    while str(password) != str(input_password):
        print(f"Chatbot: Invalid password. Please try again")
        print(f"Chatbot: Enter password again")
        input_password == input('You: ')
    return True

def selectDate():
    print(f"Chatbot: Choose date of your interest")
    print(f"Chatbot: Type in YYYY-MM-DD format")
    date = input(f"You: ")
    try:
        searched_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print('Chatbot: Invalid format, please fill as required')
        selectDate()
    current_date = datetime.now().date()
    while current_date >= searched_date:
        print(f"Chatbot: Reservation cannot be made on past dates.Please choose different one.")
        return selectDate()
    if current_date < searched_date:
        return searched_date

def selectTime(choosen_date):
    mycursor.execute(
        "SELECT reservation_time FROM Reservations WHERE reservation_date = %s", (choosen_date, )
    )
    hours = [hour[0] for hour in mycursor.fetchall()]
    free_hours = []
    hours_choice = []
    if len(hours) == (len(opening_hours) * 5):
        print(f"Chatbot: We do not have any courts available for today please check different date")
        selectDate()
    else:
        for i in hours:
            occurance = hours.count(i)
            if occurance < 5:
                full_hour = str(i)
                free_hours.append(full_hour)
        for i in opening_hours:
            if i not in hours:
                for j in range(5):
                    free_hours.append(i)
        for i in free_hours:
            full_hour = str(i) + '.00'
            if full_hour not in hours_choice:
                hours_choice.append(full_hour)
        if len(hours_choice) != 0:
            print(f"Chatbot: Please choose preffered time. Type below choosen hour in format HH.MM")
            for t in hours_choice:
                print(t, end=", ")
            user_choice = input(f"\nYou: ")
            while user_choice not in hours_choice:
                user_choice = input(f"Chatbot: Please choose time from the list\n")
            if user_choice in hours_choice:
                return user_choice

def getEmailFromUser():
    print(f"Chatbot: Fill in your email")
    email = input(f"You: ")
    return email

def addCourtNumber(user_choice, searched_date):
    mycursor.execute(
        "SELECT reservation_time FROM Reservations WHERE reservation_date = %s", (searched_date, )
    )
    hours = [hour[0] for hour in mycursor.fetchall()]
    count_hour_occurance = 1
    for i in hours:
        if str(i) == str(user_choice):
            count_hour_occurance+= 1
    return count_hour_occurance

def addUserToDatabase(name, surname, email):
    print(f"Chatbot: I see you do not currently have account. Please set password for your account.")
    password = input(f"You: ")       
    mycursor.execute(
        "INSERT INTO Clients(username, surname, client_email, password) VALUES (%s, %s, %s, %s)", (str(name), str(surname), str(email), str(password))
    )
    mydb.commit()
    mycursor.execute(
        "SELECT client_email FROM Clients WHERE client_email = %s", (email, )
    )
    if str(mycursor.fetchone()[0]) == str(email):
        print(f"Chatbot: Account created. You are now registered user!")
        return True
    elif len(mycursor.fetchall()) == 0:
        print(f"Chatbot: Something went wrong. Please set your password again")
        return False

def addReservationToDatabase(email, date, time, court):
    mycursor.execute(
        "INSERT INTO Reservations(reservation_date, reservation_time, court_number, client_email) VALUES (%s, %s, %s, %s)", (date, time, court, str(email))
    )
    mydb.commit()
    return True

def main():
    start = Reservations
    start.startChat()

if __name__ == "__main__":
    main()
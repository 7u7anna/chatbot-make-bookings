from email.message import EmailMessage
import os
import smtplib
def sendReservationConfirm(name, surname, date, time, email, court_number):
    EMAIL_ADDRESS = os.environ.get(EMAIL_ADDRESS)
    EMAIL_PASSWORD = os.environ.get(EMAIL_PASSWORD)

    name = name.capitalize()
    surname = surname.capitalize()

    confirm = EmailMessage()
    confirm['From'] = EMAIL_ADDRESS
    confirm['To'] = str(email)
    confirm['Subject'] = f'{name}, your reservation details'
    confirm.set_content(
        f'Your reservation made by {name} {surname} for {date} at {time} have been registered.\nYour court number is {court_number}\n\nThank you for choosing our services.'
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(confirm)

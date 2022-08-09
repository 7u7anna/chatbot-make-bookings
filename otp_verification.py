from email.message import EmailMessage
import os
import smtplib
import random
from random import randint

def startOtpProcedure(user_mail):
    while sendingProcedure(user_mail) != True:
        sendingProcedure(user_mail)
    return True  

def sendingProcedure(user_mail):
    code = generatingSending(user_mail)
    if checkCodeCorrect(code) != True:
        print(f"Chatbot: Invalid code, we will need to verify again because of the safety reasons we use two-step verification so you will receive two different codes in separate emails.")
        return False
    return True

def checkCodeCorrect(code):
    print(f'Chatbot: Type in code you received in email ')
    code_from_mail = input('You: ')
    if len(str(code_from_mail)) == len(str(code)):
        for i in range(len(code_from_mail)):
            if str(code_from_mail[i]) != str(code[i]):
                return False
        return True
    return False

def generatingSending(user_mail):
    code = randomNumber()
    sendOtpCode(code, user_mail)
    return code
         
def randomNumber():
    code = ''
    for i in range(4):
        elem = random.randint(0, 9)
        code+= str(elem)
    return code

def sendOtpCode(code, user_mail):
    EMAIL_ADDRESS = os.environ.get(EMAIL_ADDRESS)
    EMAIL_PASSWORD = os.environ.get(EMAIL_PASSWORD)

    otp = EmailMessage()
    otp['From'] = EMAIL_ADDRESS
    otp['To'] = str(user_mail)
    otp['Subject'] = 'Here is your pin'
    otp.set_content(
        f'Please use this number to complete your court reservation here is the code: {code}\n\nPlease not that code is active only once. After all we will send you an email with reservation confirm.'
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(otp)



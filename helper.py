from random import randint
import requests
# import env

env = {}
def randomGen(n):
    return ''.join([str(randint(0, 9)) for i in range(0, n)])


def sendOTP(email, otp):
    url = env.OTP_URL
    print(url)
    formdata = {
        "email": email,
        "body": otp
    }
    response = requests.post(url, data=formdata)
    response.raise_for_status()
    print(f"OTP: {otp} is sent to {email}")


def remindStakeholder(json):
    url = 'https://script.google.com/macros/s/AKfycbz-6CsoX7wt1WXtADgqpmq6aTzNgcI5vzRnB6lEF9aAQn6DU-dKeODScqdX-X_ybCu2hw/exec'
    response = requests.post(url, data=json)
    print(response.content)
    response.raise_for_status()
    
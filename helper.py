from random import randint
import requests
import env
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


import json
import time
import requests
from webapp import apis
from mailjet_rest import Client


def valid_password(paswd):
    digit = upper = lower = False

    for each_char in paswd:
        if each_char.isupper():
            upper = True
        elif each_char.islower():
            lower = True
        elif each_char.isdigit():
            digit = True
        if digit and upper and lower:
            return True

    return 'Password must contain one digit, upper, lower character'


def isdeliverable(mail_addr):
    api = apis.Abstract()

    response = requests.get(
        f'https://emailvalidation.abstractapi.com/v1/?api_key={api.key}&email={mail_addr}')

    if (response.status_code != 200):
        return f'[{response.status_code}]: please contact HOD'

    else:
        data = json.loads(response.text)
        if data['deliverability'] == 'UNDELIVERABLE':
            return 'Email is undeliverable, please change!'

        return True


def generate_otp():
    return str(time.time()).split('.')[1]


class Main:

    def __init__(self, request):
        self.request = request

    def isvalid(self):
        if len(self.request.POST['first_name']) < 3:
            return 'First name must contain 3 characters'
        elif len(self.request.POST['last_name']) < 3:
            return 'Last name must contain 3 characters'
        elif len(self.request.POST['username']) < 5:
            return 'Username must contain 5 characters'
        elif len(self.request.POST['module']) == 0:
            return 'Please select student or faculty'
        elif len(self.request.POST['new_password']) < 8:
            return 'Password must contain 8 and one digit, upper, lower character'
        else:
            if (error := valid_password(self.request.POST['new_password'])) != True:
                return error
            elif self.request.POST['new_password'] != self.request.POST['conf_new_paswd']:
                return 'Confirm password did not match'

        return isdeliverable(self.request.POST['mail'])

    def send_otp(self, mail_addr, name, account):
        api = apis.Mailjet()
        otp = generate_otp()
        mail = Client(auth=(api.key, api.secret), version='v3.1')

        data = {
            'Messages': [{

                "From": {
                    "Email": "codecol.services@gmail.com",
                    "Name": "Codecol"},

                "To": [{
                    "Email": mail_addr,
                    "Name": name}],

                "Subject": "Your verification code",
                "TextPart": "OTP verification",
                "HTMLPart":
                f"<div style='font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;'><h3>Hi {name}!</h3>We just need to<span style='color: #99e265'> verify </span>your email address<br />before you can<span style='color: #ffbd4a'> access </span>{account} account.<br /><br />Your verification code is<span style='color: #ff5c5c'> {otp}</span><br /><br />Enter this code in our website to<span style='color: #2eb2ff'> activate </span><br />your {account} account.<br /><br />Kind Regards, <br /><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>D</span><span style='color: #2eb2ff'>E</span><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>L</span></div>",
                "CustomID": "AppGettingStartedTest"}]
        }

        response = mail.send.create(data=data)
        if (response.status_code != 200):
            return f'[{response.status_code}]: please contact HOD'

        return True

    def verification(self):
        pass

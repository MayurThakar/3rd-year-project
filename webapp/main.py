import json
import requests
from webapp import apis
from webapp.models import OTP, Faculty, Student
from random import randint
from mailjet_rest import Client


def isdeliverable(mail_addr):
    api = apis.Abstract()

    response = requests.get(
        f'https://emailvalidation.abstractapi.com/v1/?api_key={api.key}&email={mail_addr}')

    if (response.status_code != 200):
        return f'[{response.status_code}]: please contact HOD'

    data = json.loads(response.text)
    if data['deliverability'] == 'UNDELIVERABLE':
        return 'Email is undeliverable, please change!'

    return True


def isduplicate(new_data):
    fetched_username = Faculty.objects.filter(
        username=new_data['username']).first()
    if fetched_username:
        return 'This username is already taken'

    fetched_mail = Faculty.objects.filter(
        mail=new_data['mail']).first()
    if fetched_mail:
        return 'This email is already taken'

    fetched_username = Student.objects.filter(
        username=new_data['username']).first()
    if fetched_username:
        return 'This username is already taken'

    fetched_mail = Student.objects.filter(
        mail=new_data['mail']).first()
    if fetched_mail:
        return 'This email is already taken'

    return isdeliverable(new_data['mail'])


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


def generate_otp():
    return str(randint(1000, 10000))


def add_otp(mail_addr, genr_otp):
    reference = OTP()
    reference.mail = mail_addr
    reference.otp = genr_otp
    reference.save()


def encrypt_password(password):
    encr_paswd = ''

    for each_char in password:
        if each_char.isupper():
            encr_paswd = "".join([encr_paswd, str(ord(each_char.lower()))])
        elif each_char.islower():
            encr_paswd = "".join([encr_paswd, str(ord(each_char.upper()))])
        elif each_char.isdigit():
            encr_paswd = "".join([encr_paswd, chr(int(each_char)+33)])

    return ''.join(reversed(encr_paswd))


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
        elif len(self.request.POST['account']) == 0:
            return 'Please select student or faculty account'
        elif (error := isduplicate(self.request.POST)) != True:
            return error
        elif len(self.request.POST['new_password']) < 8:
            return 'Password must contain 8 and one digit, upper, lower character'
        elif (error := valid_password(self.request.POST['new_password'])) != True:
            return error
        elif self.request.POST['new_password'] != self.request.POST['conf_new_paswd']:
            return 'Confirm password did not match'

        return True

    def send_otp(self, mail_addr, name, account):
        api = apis.Mailjet()
        genr_otp = generate_otp()
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
                f"<div style='font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;'><h3>Hi {name}!</h3>We just need to<span style='color: #99e265'> verify </span>your email address<br />before you can<span style='color: #ffbd4a'> access </span>{account} account.<br /><br />Your verification code is<span style='color: #ff5c5c'> {genr_otp}</span><br /><br />Enter this code in our website to<span style='color: #2eb2ff'> activate </span><br />your {account} account.<br /><br />Kind Regards, <br /><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>D</span><span style='color: #2eb2ff'>E</span><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>L</span></div>",
                "CustomID": "AppGettingStartedTest"}]
        }

        response = mail.send.create(data=data)
        if (response.status_code != 200):
            return f'[{response.status_code}]: please contact HOD'

        add_otp(mail_addr, genr_otp)
        return True

    def verification(self, obtd_otp, mail_addr):
        if not obtd_otp.isdigit():
            return 'Please provide only digits'

        otp_mail = OTP.objects.filter(otp=obtd_otp).values('mail').first()

        if otp_mail:
            if mail_addr == otp_mail['mail']:

                OTP.objects.filter(otp=obtd_otp).delete()
                return True

        return 'Sorry, invalid OTP!'

    def create_account(self, data):
        if data['account'] == 'faculty':
            reference = Faculty()
        else:
            reference = Student()

        reference.full_name = f"{data['first_name']} {data['last_name']}"
        reference.username = data['username']
        reference.mail = data['mail']
        reference.password = encrypt_password(data['new_password'])
        reference.save()

# username_mail = Faculty.objects.filter(username=new_data['username'], mail=new_data['mail']).first()

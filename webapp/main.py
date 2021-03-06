import json
import requests
import pandas as panda
from webapp import apis
from webapp import models
from random import randint
from webapp import credentials
from mailjet_rest import Client
from datetime import datetime, timedelta


def isdeliverable(mail_addr):
    api = apis.Abstract()
    response = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key={api.key}&email={mail_addr}')
    
    if (response.status_code != 200):
        return f'[{response.status_code}]: Please contact principal', 0

    data = json.loads(response.text)
    if data['deliverability'] == 'UNDELIVERABLE':
        return 'Email is undeliverable, please change!', 4

    return True


def isduplicate(new_data):

    model = [models.Faculty, models.Student]

    for mdl in model:

        uname = mdl.objects.filter(
            username=new_data['new_username']).first()
        if uname:
            return 'This username is already taken', 3

        mail_addr = mdl.objects.filter(
            mail=new_data['mail']).first()
        if mail_addr:
            return 'This email is already taken', 4

    return isdeliverable(new_data['mail'])


def valid_password(password):
    digit = upper = lower = False

    for each_char in password:
        if each_char.isupper():
            upper = True
        elif each_char.islower():
            lower = True
        elif each_char.isdigit():
            digit = True
        if digit and upper and lower:
            return True

    return 'Password must contain one digit, upper, lower character', 5


def generate_otp():
    return str(randint(1000, 10000))


def add_otp(mail_addr, genr_otp):
    reference = models.OTP()
    reference.mail = mail_addr
    reference.otp = genr_otp
    reference.save()


def send_otp(data):
    mail_addr = data['mail']
    fname = data['first_name']
    account = data['new_account']
    api = apis.Mailjet()
    genr_otp = generate_otp()
    creds = Client(auth=(api.key, api.secret), version='v3.1')

    body = {
        'Messages': [{

            "From": {
                "Email": "codecol.services@gmail.com",
                "Name": "Codecol"},

            "To": [{
                "Email": mail_addr,
                "Name": fname}],

            "Subject": "Your verification code",
            "TextPart": "OTP verification",
            "HTMLPart":
            f"<div style='font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;'><h3>Hi {fname}!</h3>We just need to<span style='color: #99e265'> verify </span>your email address<br />before you can<span style='color: #ffbd4a'> access </span>{account} account.<br /><br />Your verification code is<span style='color: #ff5c5c'> {genr_otp}</span><br /><br />Enter this code in our website to<span style='color: #2eb2ff'> activate </span><br />your {account} account.<br /><br />Kind Regards, <br /><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>D</span><span style='color: #2eb2ff'>E</span><span style='color: #99e265'>C</span><span style='color: #ffbd4a'>O</span><span style='color: #ff5c5c'>L</span></div>",
            "CustomID": "AppGettingStartedTest"}]
    }

    response = creds.send.create(data=body)
    if (response.status_code != 200):
        return f'[{response.status_code}]: Please contact principal'

    otp = models.OTP.objects.filter(mail=mail_addr).first()
    if otp == None:
        add_otp(mail_addr, genr_otp)

    return True


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


def account_status(username):
    acct_sts = models.Faculty.objects.filter(username=username).first()

    if acct_sts.account_status == 'pending':
        return 'Your account is not active, Please contact principal', 0
    elif acct_sts.account_status == 'deactive':
        return 'Sorry, your account been deactivated', 0

    return True


def get_credentials():
    id_name = models.Gsheet.objects.all().first()
    return id_name.sheetID, id_name.sheetNAME


def read_Gsheet():
    SPREADSHEET_ID, SPREADSHEET_NAME = get_credentials()
    creds = credentials.Credentials(SPREADSHEET_ID, SPREADSHEET_NAME)
    dataframe = panda.read_csv(creds.SPREADSHEET_URL)
    sheet = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    return sheet


def get_current_day():
    response = requests.get('http://worldclockapi.com/api/json/gmt/now')
    data = json.loads(response.text)
    return data['dayOfTheWeek']


def column_in(sheet, day):
    if not day in sheet.columns:
        return False

    return True


def get_full_name(username):
    uname = models.Faculty.objects.filter(username=username).first()
    return uname.full_name


def fetch_periods(sheet, day):
    cols = panda.DataFrame(sheet, columns=[day, 'Time'])
    periods = {}

    for _, row in cols.iterrows():
        if len(str(row[day]).split('|')) > 1:
            periods[row['Time']] = {
                'username': str(row[day]).split('|')[0],
                'teacher': get_full_name(str(row[day]).split('|')[0]),
                'subject': str(row[day]).split('|')[1].title()}

    return periods


def user_period(username, periods):

    for time, tch_sub in periods.items():
        if username == tch_sub['username']:
            return [time, tch_sub['subject']]

    return None


def get_current_time():
    response = requests.get(
        'http://worldtimeapi.org/api/timezone/Indian/Cocos')
    data = json.loads(response.text)
    date_time = datetime.fromisoformat(str(data['datetime']).split('.')[0])
    date_time = date_time - timedelta(minutes=60)
    return str(date_time).split(' ')[1]


class Main:

    def __init__(self, request):
        self.request = request

    def isexist(self):
        username = self.request.POST['username']
        password = encrypt_password(self.request.POST['password'])

        if self.request.POST['account'] == 'faculty':
            model = models.Faculty
        else:
            model = models.Student

        uname = model.objects.filter(username=username).first()

        if uname == None:
            return 'User does not exist', 1
        elif uname.password != password:
            return 'Incorrect password', 2

        return account_status(username) if self.request.POST['account'] == 'faculty' else True

    def isvalid(self):
        if len(self.request.POST['first_name']) < 3:
            return 'First name must contain 3 characters', 1
        elif len(self.request.POST['last_name']) < 3:
            return 'Last name must contain 3 characters', 2
        elif len(self.request.POST['new_username']) < 5:
            return 'Username must contain 5 characters', 3
        elif len(self.request.POST['new_account']) == 0:
            return 'Please select student or faculty account', 0
        elif (error := isduplicate(self.request.POST)) != True:
            return error
        elif len(self.request.POST['new_password']) < 8:
            return 'Password must contain 8 and one digit, upper, lower character', 5
        elif (error := valid_password(self.request.POST['new_password'])) != True:
            return error
        elif self.request.POST['new_password'] != self.request.POST['conf_new_paswd']:
            return 'Confirm password did not match', 6

        return send_otp(self.request.POST)

    def verification(self):
        obtd_otp = self.request.POST['otp']
        mail_addr = self.request.session['data']['mail']

        if obtd_otp.isdigit() == False:
            return 'Please provide only digits'

        otp_mail = models.OTP.objects.filter(
            otp=obtd_otp).values('mail').first()

        if otp_mail:
            if mail_addr == otp_mail['mail']:

                models.OTP.objects.filter(otp=obtd_otp).delete()
                return True

        return 'Sorry, invalid OTP!'

    def create_account(self, data):
        if data['new_account'] == 'faculty':
            reference = models.Faculty()
        else:
            reference = models.Student()

        full_name = f"{data['first_name'].title()} {data['last_name'].title()}"
        reference.full_name = full_name
        reference.username = data['new_username']
        reference.mail = data['mail']
        reference.password = encrypt_password(data['new_password'])
        reference.save()

    def has_periods(self, username=None):
        sheet = read_Gsheet()
        DAY = get_current_day()

        if column_in(sheet, DAY):
            periods = fetch_periods(sheet, DAY)

            if username != None:
                return user_period(username, periods)

            return periods

        else:
            return None

    def fetch_announces(self):
        announcements = list(
            set(models.Announce.objects.all().values_list()))
        announces = {}

        for content in announcements:
            announces[content[2].title()] = {
                'date': content[1],
                'description': content[3]}

        return announces

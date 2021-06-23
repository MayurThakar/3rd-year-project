import time


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

        return True

    def send_otp(self):
        print(generate_otp())

    def verification(self):
        pass

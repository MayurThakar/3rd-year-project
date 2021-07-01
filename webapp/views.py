from webapp import main
from django.shortcuts import render

# Create your views here.


def index(request):

    if request.method == 'POST' and 'signin-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.isexist()) == True:

            if request.POST['account'] == 'faculty':
                return render(request, 'faculty.html')

            else:
                periods = reference.fetch_periods()
                announces = reference.fetch_announces()
                return render(request, 'student.html', {
                    'periods': periods,
                    'announces': announces})

        else:
            return render(request, 'index.html', {
                'has_error': error[0],
                'err_id': error[1],
                'input_data': request.POST})

    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST' and 'signup-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.isvalid()) == True:
            request.session['data'] = request.POST
            return render(request, 'signup.html', {
                'otp_verif': True,
                'has_message': 'OTP has been sent to your email'})

        else:
            return render(request, 'signup.html', {
                'has_error': error[0],
                'err_id': error[1],
                'input_data': request.POST})

    elif request.method == 'POST' and 'verif-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.verification()) == True:

            reference.create_account(request.session['data'])
            del request.session['data']
            return render(request, 'index.html')

        else:
            return render(request, 'signup.html', {
                'otp_verif': True,
                'has_message': 'OTP has been sent to your email',
                'obtd_otp': request.POST['otp'],
                'has_error': error})

    return render(request, 'signup.html')

from webapp import main
from django.shortcuts import render

# Create your views here.


def signup(request):
    if request.method == 'POST' and 'signup-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.isvalid()) == True:
            if (error := reference.send_otp(
                request.POST['mail'], request.POST['first_name'],
                    request.POST['account'])) == True:

                request.session['data'] = request.POST
                return render(request, 'signup.html', {
                    'otp_verif': True,
                    'has_message': 'OTP has been sent to your email'})

        return render(request, 'signup.html', {'has_error': error, 'input_data': request.POST})

    elif request.method == 'POST' and 'verif-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.verification(
            request.POST['otp'],
                request.session['data']['mail'])) == True:

            reference.create_account(request.session['data'])
            del request.session['data']
            return render(request, 'index.html')

        return render(request, 'signup.html', {
            'otp_verif': True,
            'has_message': 'OTP has been sent to your email',
            'obtd_otp': request.POST['otp'],
            'has_error': error})

    return render(request, 'signup.html')

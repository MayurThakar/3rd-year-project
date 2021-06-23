from django.shortcuts import render
from webapp import main

# Create your views here.


def signup(request):
    if request.method == 'POST' and 'signup-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.isvalid()) == True:
            reference.send_otp()
            return render(request, 'signup.html', {
                'has_message': 'OTP has been sent to your gmail',
                'otp_verif': True})
        return render(request, 'signup.html', {'has_error': error, 'input_data': request.POST})

    elif request.method == 'POST' and 'otp-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.verification()) == True:
            return render(request, 'index.html')
        return render(request, 'signup.html', {'has_error': error, 'otp_verif': True})

    return render(request, 'signup.html')

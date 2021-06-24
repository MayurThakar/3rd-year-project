from webapp import main
from django.shortcuts import render

# Create your views here.


def signup(request):
    if request.method == 'POST' and 'signup-button' in request.POST:
        reference = main.Main(request)

        if (error := reference.isvalid()) == True:

            if (error := reference.send_otp(
                request.POST['mail'],
                request.POST['first_name'],
                    request.POST['module'])) == True:

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

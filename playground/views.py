from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Validation
from django.contrib.sessions.models import Session
import random
import os
import sendgrid

#TO DO: Declare validation_code variable
#TO DO: Create definition called validate_code
#TO DO: Get the value the user is submitting and compare
# Create your views here.
def say_hello(request):
    return render(request, 'hello.html')

def generate_code():
    return (random.randint(0, 899999)+100000)

def verifyemail(request):
    #TO DO: Generate 6 digit code
    #TO DO: Return 6 digit code to user
    #TO DO: Return a verify.html which has a text box to type 6 digit code and a submit button
    code = generate_code()
    request.session['generated_code'] = code
    email = request.POST.get('sender_email')
    fname = request.POST.get('first_name')
    lname = request.POST.get('last_name')
    person_instance = Person.objects.create(email=email, fname=fname, lname=lname)
    person_instance.save()
    #TO DO: Create validation code object
    validation_instance = Validation.objects.create(person = person_instance, validation_code=code)
    validation_instance.save()
    validation_id = validation_instance.id
    send_email(email, code)
    print(request.path)
    return render(request, 'verifyemail.html', {'code': code, 'validation_id': validation_id})

def validate_code(request):
    if request.method == 'POST':
        submitted_code = int(request.POST.get('given_digit'))  # Assuming your form field name is 'given_digit'
        valid_id = int(request.POST.get('valid_id'))
        # Retrieve the validation_instance using the generated_code
        validation_instance = Validation.objects.get(id=valid_id)
        print(submitted_code, validation_instance.validation_code)
        if submitted_code == validation_instance.validation_code:
            # Code is correct
            return render(request, 'success.html')  # Render success.html
        else:
            # Code is incorrect
            return render(request, 'error.html')  # Render error.html
    else:
        # Handle GET request or other cases
        # Redirect the user back to the form page or display an error message
        return render(request, 'verifyemail.html')
    
def send_email(to_address, code):
    message = sendgrid.mail.Mail(
    from_email='sidharthpodury@gmail.com',
    to_emails=to_address,
    subject='Here is your secret code',
    html_content= f'Your code is : <strong>{code}</strong>')
    try:
        sgclient = sendgrid.SendGridAPIClient('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')
        response = sgclient.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
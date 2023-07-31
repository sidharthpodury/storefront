from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Validation, Invitation, Timeslot
from django.contrib.sessions.models import Session
import random
import os
import sendgrid
from playground import secret

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
    send_validation(email, code)
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
    
def send_validation(to_address, code):
    message = sendgrid.mail.Mail(
    from_email='sidharthpodury@gmail.com',
    to_emails=to_address,
    subject='Here is your secret code',
    html_content= f'Your code is : <strong>{code}</strong>')
    try:
        sgclient = sendgrid.SendGridAPIClient(secret.my_api_key)
        response = sgclient.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
        
def send_invite(request):
    if request.method == 'POST':
        # Get the selected invitees and meeting times from the form data
        #TODO: Figure out how to read more than one item from form
        selected_invitees = request.POST.getlist('invitees')
        selected_meeting_times = request.POST.getlist('meeting_times')
        sender_email = "sidharth.podury@gmail.com"
        invitees = ['kmpodury@gmail.com', 'koswati@gmail.com']
        available_times = ['3/3/2023 8AM', '1/03/2023 10AM']
        sender_person = Person.objects.create(email=sender_email)
        sender_person.save()
        invitation = Invitation.objects.create(sender = sender_person)
        invitation.save()
        print(f"invitation is {invitation}")
        for email in invitees:
            invited = Person.objects.create(email=email)
            invited.save()
            for selected_time in available_times:
                timeslot = Timeslot.objects.create(invitee=invited, invitation=invitation, selected_dt=selected_time)
                timeslot.save()
                print(f"timeslot is {timeslot}")
        # After saving the data, you may redirect to a success page or render a success template
        return render(request, 'invitation_sent.html')

    # If it's not a POST request, simply render the formf
    return render(request, 'success.html')
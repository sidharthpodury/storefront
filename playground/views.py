"""
Django Project - Sending emails with python.

:Author Sidharth Podury
:Version 7-31-23
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person, Validation, Invitation, Timeslot
from django.contrib.sessions.models import Session
import random
import os
import sendgrid
from playground import secret


def say_hello(request):
    """Return a render request to a hello.html.

    Args:
        request (HttpRequest): request received from browser

    Return:
        Hello.html (render): prompt user to enter email and name
    """
    return render(request, "hello.html")


def generate_code():
    """Return a random 6 digit number.

    Args:
        None

    Returns:
        int
    """
    return random.randint(0, 899999) + 100000


def verify_email(request):
    """Return a render request indicating a verified email.

    Args:
        request

    Returns:
        verifyemail.html (render): an html page prompting you to enter code
    """
    # TO DO: Generate 6 digit code
    # TO DO: Return 6 digit code to user
    code = generate_code()
    email = request.POST.get("sender_email")
    fname = request.POST.get("first_name")
    lname = request.POST.get("last_name")
    person_instance = Person.objects.create(email=email,
                                            fname=fname,
                                            lname=lname)
    person_instance.save()
    # TO DO: Create validation code object
    validation_instance = Validation.objects.create(
        person=person_instance, validation_code=code
    )
    validation_instance.save()
    validation_id = validation_instance.id
    send_validation(email, code)
    print(request.path)
    return render(
        request, "verifyemail.html", {"validation_id": validation_id}
    )


def validate_code(request, validation_id):
    """Return a render stating whether verification was successful.

    Args:
        request

    Returns:
        success.html (render): Prompts user to enter receiver info and times
    """
    if request.method == "POST":
        submitted_code = int(
            request.POST.get("given_digit")
        )  # Assuming your form field name is 'given_digit'
        # Retrieve the validation_instance using the generated_code
        validation_instance = Validation.objects.get(id=validation_id)
        person_key = validation_instance.person.id
        print(submitted_code, validation_instance.validation_code)
        if submitted_code == validation_instance.validation_code:
            # Code is correct
            return render(request, "success.html", {'person_key': person_key})  # Render success.html
        else:
            # Code is incorrect
            return render(request, "error.html")  # Render error.html
    else:
        # Handle GET request or other cases
        # Redirect the user back to the form page or display an error message
        return render(request, "verifyemail.html")


def send_validation(to_address, code):
    message = sendgrid.mail.Mail(
        from_email="sidharthpodury@gmail.com",
        to_emails=to_address,
        subject="Here is your secret code",
        html_content=f"Your code is : <strong>{code}</strong>",
    )
    try:
        sgclient = sendgrid.SendGridAPIClient(secret.my_api_key)
        response = sgclient.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def get_invite(request, person_key):
    if request.method == "POST":
        selected_invitees = request.POST.get("selected_invitees")
        selected_meeting_times = request.POST.getlist("meeting_times")
        person_instance = Person.objects.get(id=person_key)
        sender_email = person_instance.email
        selected_invitees = selected_invitees.split(',')
        selected_invitees.pop()
        sender_person = Person.objects.create(email=sender_email)
        print("Sender person is", sender_email)

        invitation = Invitation.objects.create(sender=sender_person)
        invitation_key = invitation.id
    
        for email in selected_invitees:
            invitee = Person.objects.create(email=email)
            invitee_key = invitee.id
            send_invite(email, sender_email)
            for selected_time in selected_meeting_times:
                timeslot = Timeslot.objects.create(
                    invitation=invitation,
                    invitee=invitee,
                    selected_dt=selected_time
                )
        return render(request, "invitation_sent.html", {'invitee_key': invitee_key, 'invitation_key': invitation_key})
    return render(request, "success.html")

def send_invite(invitee, sender_person):
    print(invitee, sender_person)
    message = sendgrid.mail.Mail(
    from_email=sender_person,
    to_emails=invitee,
    subject="Here is your invitation",
    html_content=f"Invitation",
    )
    try:
        sgclient = sendgrid.SendGridAPIClient(secret.my_api_key)
        response = sgclient.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def show_invite(request, invitee_key, invitation_key):
    #timeslot_instance = Timeslot.objects.get(invitee=invitee_key, invitation=invitation_key)
    timeslots = Timeslot.objects.filter(invitee=invitee_key, invitation=invitation_key)
    print(timeslots)
    selected_ts = []
    for timeslot in timeslots:
        selected_ts.append(timeslot.selected_dt)
    return render(request, 'show_invite.html', {'selected_ts':selected_ts})
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
    request.session["generated_code"] = code
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
        request, "verifyemail.html", {"code": code,
                                      "validation_id": validation_id}
    )


def validate_code(request):
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
        valid_id = int(request.POST.get("valid_id"))
        # Retrieve the validation_instance using the generated_code
        validation_instance = Validation.objects.get(id=valid_id)
        print(submitted_code, validation_instance.validation_code)
        if submitted_code == validation_instance.validation_code:
            # Code is correct
            return render(request, "success.html")  # Render success.html
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


def send_invite(request):
    if request.method == "POST":
        selected_invitees = request.POST.getlist("invitees")
        selected_meeting_times = request.POST.getlist("meeting_times")
        sender_email = "sid.podury@gmail.com"

        sender_person, _ = Person.objects.get_or_create(email=sender_email)

        invitation = Invitation.objects.create(sender=sender_person)

        for email in selected_invitees:
            invited, _ = Person.objects.get_or_create(email=email)
            for selected_time in selected_meeting_times:
                timeslot = Timeslot.objects.create(
                    invitee=invited,
                    invitation=invitation,
                    selected_dt=selected_time
                )
        return render(request, "invitation_sent.html")
    return render(request, "success.html")
from communication.models import EmailMessage, EmailAddress

def send_email(recipients: list, subject: str, message: str) -> int:
    email_addresses = [EmailAddress.objects.get_or_create(email=recipient)[0] for recipient in recipients]

    email_message = EmailMessage.objects.create(
        subject=subject,
        message=message,
    )

    for recipient in email_addresses:
        email_message.recipients.add(recipient)

    response = email_message.send()

    return response.status_code

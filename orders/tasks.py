from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_email(title: str, tpl_name: str, ctx: dict, recipients):
    if type(recipients) == str:
        recipients = [recipients]
    tpl = render_to_string(tpl_name,ctx)
    for recipient in recipients:
        email = EmailMessage(subject=title, body=tpl, from_email=settings.DEFAULT_FROM_EMAIL, to=[recipient])
        email.content_subtype = "html"  
        email.send(fail_silently=False)
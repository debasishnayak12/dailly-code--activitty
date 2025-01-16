from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.core.mail import EmailMultiAlternatives

@api_view(['POST'])
def send_email(request):
    subject = request.data.get('subject', 'Default Subject')
    message = request.data.get('message', 'Default Message')
    recipient = request.data.get('recipient', '')

    if not recipient:
        return Response({'error': 'Recipient email is required.'}, status=400)

    try:
        #sending only text content to mail 
        # send_mail(
        #     subject,
        #     message,
        #         'nayakdebasish7126@gmail.com',  # From email
        #     [recipient],            # To email
        #     fail_silently=False,
        # )
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='nayakdebasish7205@gmail.com',
            to=[recipient],
        )
        email.content_subtype = 'html'  # Set the email content type to HTML
        email.send(fail_silently=False)
        
        return Response({'success': 'Email sent successfully.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def send_html_text(request):
    subject = request.data.get('subject', 'Default Subject')
    plain_message = request.data.get('plain_message', 'Default plain text message.')
    html_message = request.data.get('html_message', '<p>Default <b>HTML</b> Message</p>')
    recipients = request.data.get('recipients', [])

    if not recipients or not isinstance(recipients, list):
        return Response({'error': 'A valid recipient list is required.'}, status=400)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,  # Plain text content
            from_email='nayakdebasish7205@gmail.com',
            to=recipients,
        )
        email.attach_alternative(html_message, "text/html")  # Attach HTML version
        email.send(fail_silently=False)
        return Response({'success': f'Email sent to {len(recipients)} recipients.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
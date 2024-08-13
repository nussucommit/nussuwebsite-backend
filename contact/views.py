from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from dotenv import load_dotenv
from pathlib import Path
import os
import requests
from notionConnection.parser import parse


dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('NOTION_API_KEY')
version = '2021-08-16'

NOTION_PAGE_URL = 'https://api.notion.com/v1/blocks/{blockid}/children'
NOTION_HEADER = {'Notion-Version': version, 'Authorization': token}



@api_view(['POST'])
def submit_feedback(request):
    # Extract data from the request
    sheet1 = request.data.get('sheet1', {})
    full_name = sheet1.get('fullName')
    email = sheet1.get('email')
    subject = sheet1.get('subject')
    question = sheet1.get('question')

    # Validate the input
    if not (full_name and email and subject and question):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    # Email configuration
    SENDER_EMAIL = os.getenv('EMAIL_HOST_USER')
    RECEIVER_EMAIL = SENDER_EMAIL  # Feedback goes to the company email

    # Send the feedback email
    try:
        send_mail(
            subject=f"Feedback: {subject} from {full_name}",
            message=f"Name: {full_name}\nEmail: {email}\nSubject: {subject}\nQuestion: {question}",
            from_email=SENDER_EMAIL,
            recipient_list=[RECEIVER_EMAIL],
        )
    except Exception as e:
        return Response({"error": "Failed to send feedback email", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Send auto-reply to the user
    try:
        send_mail(
            subject='Auto Reply From Protechs Nutrition',
            message='Thank you for your message. We will get back to you soon.',
            from_email=SENDER_EMAIL,
            recipient_list=[email],
        )
    except Exception as e:
        return Response({"error": "Failed to send auto reply", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"success": "Feedback submitted successfully"}, status=status.HTTP_200_OK)


@api_view(['Get'])
def contact(request):
    CONTACT_URL = '80fc40185db84c88bd30824a10add0de'
    data = get_parsed_data(CONTACT_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

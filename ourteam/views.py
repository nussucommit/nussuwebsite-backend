from rest_framework.decorators import api_view
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
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

@api_view(['Get'])
def presidential(request):
    PRESIDENTIAL_URL = '775fe303392d498293f9102feb96ac35'
    data = get_parsed_data(PRESIDENTIAL_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def relations(request):
    RELATIONS_URL = 'dc34de1f9d7f405e982517689b429bce'
    data = get_parsed_data(RELATIONS_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def secretariat(request):
    SECRETARIAT_URL = '8871dfe66ad2448c8e7740059a4f83cc'
    data = get_parsed_data(SECRETARIAT_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def finance(request):
    FINANCE_URL = 'b840c269648e4d5c8d1934e7251d4595'
    data = get_parsed_data(FINANCE_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def communications(request):
    COMMUNICATIONS_URL = '70e6bf12c8154340bf06e0f888618866'
    data = get_parsed_data(COMMUNICATIONS_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def studentlife(request):
    STUDENT_LIFE_URL = 'f48aefac261446f8918d94816a0b7327'
    data = get_parsed_data(STUDENT_LIFE_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def studentwelfare(request):
    STUDENT_WELFARE_URL = '5e75012fc8da47cd9a5948108a27e735'
    data = get_parsed_data(STUDENT_WELFARE_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

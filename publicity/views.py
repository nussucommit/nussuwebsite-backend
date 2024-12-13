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
def pageOne(request):
    PAGE_ONE_URL = 'a439ca165b8f466cbbe6235e4614a5a0'
    data = get_parsed_data(PAGE_ONE_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def pageTwo(request):
    PAGE_TWO_URL = '988df5f0e0c04496966c0d318e3a2a87'
    data = get_parsed_data(PAGE_TWO_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

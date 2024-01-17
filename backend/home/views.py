from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
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
@cache_page(timeout=60 * 30)
def home(request):
    HOME_URL = 'df0fa3fd940b46399b33e6462d964d5c'
    data = get_parsed_data(HOME_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    if response.status_code != 200:
        return {'status_code': response.status_code, 'data': response.json()['message']}
    data = response.json()
    return parse(data)

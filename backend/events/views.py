from rest_framework.decorators import api_view
from django.core.cache import cache
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
def events(request):
    EVENTS_URL = '60ed78155c1d4e858f0800ad226f8d4d'

    cache_key = 'events'
    data = cache.get(cache_key)

    if data is None:
        data = get_parsed_data(EVENTS_URL)
        cache.set(key=cache_key, value=data, timeout=60 * 30)

    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

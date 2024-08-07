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
def aboutus(request):
    ABOUT_US_URL = '4c7b695537044ccfa186d85ecfff7c3a'
    data = get_parsed_data(ABOUT_US_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def history(request):
    HISTORY_URL = '7ec11fc1167e4bdebb61527c654982fd'
    data = get_parsed_data(HISTORY_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def governance(request):
    GOVERNANCE_URL = '7611e94d7fa9415db1d2453253ecce4e'
    data = get_parsed_data(GOVERNANCE_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def ourteam(request):
    OUR_TEAM_URL = 'd64ee576792d48a4a3bbca2153795348'
    data = get_parsed_data(OUR_TEAM_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def president(request):
    PRESIDENT_URL = '44bcb9c8dbd542bfb24d967e4c95de26'
    data = get_parsed_data(PRESIDENT_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    return parse(data)

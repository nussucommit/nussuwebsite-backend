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
def studentFunds(request):
    STUDENT_FUNDS_URL = '74d4fd3396a24c83bdde43513cd08b27'
    data = get_parsed_data(STUDENT_FUNDS_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def councilFunding(request):
    COUNCIL_FUNDING_URL = '599dff9ddd534ffa8bee1b3261939dbe'
    data = get_parsed_data(COUNCIL_FUNDING_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def resilienceFund(request):
    RESILIENCE_FUND_URL = '4cd1136a50f14885821be91b3790505a'
    data = get_parsed_data(RESILIENCE_FUND_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def logisticsRental(request):
    LOGISTICS_RENTAL_URL = 'b9cd2bef52954fc58569b3bf1c5679d9'
    data = get_parsed_data(LOGISTICS_RENTAL_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def zoomLicense(request):
    ZOOM_LICENSE_URL = '32acb975db9f4fec811b77181ce7983a'
    data = get_parsed_data(ZOOM_LICENSE_URL)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['Get'])
def publicityManagement(request):
    PUBLICITY_MANAGEMENT_URL = '270cba9c9f9b4fb79660e525039acaa8'
    data = get_parsed_data(PUBLICITY_MANAGEMENT_URL)
    return Response(data, status=status.HTTP_200_OK)

def get_parsed_data(id):
    url = NOTION_PAGE_URL.format(blockid=id)
    response = requests.get(url, headers=NOTION_HEADER)
    data = response.json()
    # return data
    return parse(data)

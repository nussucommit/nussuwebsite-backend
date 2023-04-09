from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import NotionClient

class ContactUsAPIView(APIView):
    def get(self, request):
        resp = {'message': "Hola, amigos"}
        pageId = '6475f7cb6a544e8dbed905191c627553'
        client = NotionClient()
        try:
        
            data = client.getAllChildrenAsync(pageId)
        except Exception as e:
            return Response({"error": str(e)}, status="404")
        
        return Response(data)


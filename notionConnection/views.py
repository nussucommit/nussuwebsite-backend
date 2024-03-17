from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import NotionClient

class TestAPIView(APIView):
    def get(self, request):
        resp = {'message': "Hola, amigos"}
        pageId = 'd363532b2d1b48f391a9d1dafaa2a351'
        client = NotionClient()
        try:
            data = client.getAllChildren(pageId)

        except Exception as e:
            return Response({"error": str(e)}, status="404")
        
        return Response(data)
# Create your views here.

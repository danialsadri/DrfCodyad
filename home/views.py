from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


class MessageView(APIView):
    def get(self, request: Request):
        name = request.query_params.get('name')
        return Response(data={'message': f"hello {name}"})

    def post(self, request: Request):
        name = request.data.get('name')
        return Response(data={'message': f"hello {name}"})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
import requests


class MessageView(APIView):
    def get(self, request: Request):
        name = request.query_params.get('name')
        return Response(data={'message': f"hello {name}"})

    def post(self, request: Request):
        name = request.data.get('name')
        return Response(data={'message': f"hello {name}"})


class GetCryptoPrice(APIView):
    def get(self, request: Request):
        coin = request.query_params.get('coin')
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}")
        data = response.json()
        result = {
            'price': data['price'],
            'symbol': data['symbol']
        }
        return Response(data=result)

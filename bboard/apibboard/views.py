from django.shortcuts import render
from rest_framework.response import Response
from  rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from mainapp.models import Bb
from .serializers import BbSerializers, BbDetailSerializers
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST

#Главная страница - api с выводом списка объявлений
@api_view(['GET'])
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_avtive = True)[:10]
        serializer = BbSerializers(bbs, many=True)
        return Response(serializer.data)

#Страница - api детальный вывод объявления
class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_avtive = True)
    serializer_class = BbDetailSerializers
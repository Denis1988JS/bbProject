from rest_framework import serializers

from mainapp.models import Bb

#Сериализация - список объявлений
class BbSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id','title','content','price','create_date')

#Сериализация - вывод отдельного объявления
class BbDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id','title','content','price','create_date','contacts','image')

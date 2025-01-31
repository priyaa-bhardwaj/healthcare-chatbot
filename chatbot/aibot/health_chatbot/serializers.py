from rest_framework import serializers
from .models import CustomUser, Appointment, Question

class UserSerializer(serializers.ModelSerializer):
    chat=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model=CustomUser
        fields='__all__'
    
class QuestionSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),many=False)
    # user_details=UserSerializer()
    class Meta:
        model=Question
        fields='__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),many=False)
    class Meta:
        model=Appointment
        fields='__all__'

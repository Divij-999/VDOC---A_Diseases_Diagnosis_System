from rest_framework import serializers
from .models import *


class DescriptionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Description
        fields = ['Description_id','Disease','Disease_description']

class PrecautionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Precaution
        fields = ['Precaution_id','Disease','Precaution_1','Precaution_2','Precaution_3','Precaution_4']

class MedicationSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Medication
        fields = ['Medication_id','Disease','Disease_medication']

class DietSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Diet
        fields = ['Diet_id','Disease','Disease_Diet']

class DiseaseSerializer(serializers.ModelSerializer) :

    Description_id = DescriptionSerializer()
    Precaution_id = PrecautionSerializer()
    Medication_id = MedicationSerializer()
    Diet_id = DietSerializer()

    class Meta :
        model = Diseases
        fields = ['Disease_id','Disease','Symptom_1','Symptom_2','Symptom_3','Symptom_4','Description_id','Precaution_id','Medication_id','Diet_id','Disease_severity']
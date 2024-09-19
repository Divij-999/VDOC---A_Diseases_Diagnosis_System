from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin


class Description(models.Model) :
    Description_id = models.AutoField(primary_key=True)
    Disease = models.CharField(max_length=100)
    Disease_description = models.TextField(blank=True)

    def __str__(self) :
        return self.Disease

class Precaution(models.Model) :
    Precaution_id = models.AutoField(primary_key=True)
    Disease = models.CharField(max_length=100)
    Precaution_1 = models.CharField(max_length=100,null=True)
    Precaution_2 = models.CharField(max_length=100,null=True)
    Precaution_3 = models.CharField(max_length=100,null=True)
    Precaution_4 = models.CharField(max_length=100,null=True)

    def __str__(self) :
        return self.Disease

class Medication(models.Model) :
    Medication_id = models.AutoField(primary_key=True)
    Disease = models.CharField(max_length=100)
    Disease_medication = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    def __str__(self) :
        return self.Disease

class Diet(models.Model) :
    Diet_id = models.AutoField(primary_key=True)
    Disease = models.CharField(max_length=100)
    Disease_Diet = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    def __str__(self) :
        return self.Disease

class Diseases(models.Model) :
    Disease_id = models.AutoField(primary_key=True)
    Disease = models.CharField(max_length=100)
    Symptom_1 = models.CharField(max_length=100,null=True)
    Symptom_2 = models.CharField(max_length=100,null=True)
    Symptom_3 = models.CharField(max_length=100,null=True)
    Symptom_4 = models.CharField(max_length=100,null=True)
    Description_id = models.ForeignKey(Description, on_delete=models.CASCADE,blank=True,null=True)
    Precaution_id = models.ForeignKey(Precaution, on_delete=models.CASCADE,blank=True,null=True)
    Medication_id = models.ForeignKey(Medication, on_delete=models.CASCADE,blank=True,null=True)
    Diet_id = models.ForeignKey(Diet, on_delete=models.CASCADE,blank=True,null=True)
    Disease_severity = models.FloatField(null=True)
    
    def __str__(self) :
        return self.Disease
    
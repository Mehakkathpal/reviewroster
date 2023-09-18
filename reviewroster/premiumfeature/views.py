from django.shortcuts import render
from rest_framework.views import APIView
from premiumfeature.serializer import companySerializer
from premiumfeature.models import Companies
from rest_framework.response import Response
# Create your views here.


class companyAPIView(APIView):
    def get(self,request,pk=None):
        company_id=pk
        if pk is None:
            companies = Companies.objects.all()
            serializer = companySerializer(companies,many=True)
            return Response(serializer.data)
        else:
            company = Companies.objects.filter(company_id=company_id)
            serializer = companySerializer(company)
            return serializer.data
            

            


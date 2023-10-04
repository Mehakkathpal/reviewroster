from django.shortcuts import render
from rest_framework.views import APIView
from feemanagement.serializer import feestatusserializer
from feemanagement.models import feestatus
from rest_framework.response import Response
from rest_framework.decorators import api_view


class feestatusAPIView(APIView):
    def get(self,request,pk=None):
        student_email=pk
        if pk is None:
            fee_status = feestatus.objects.all()
            serializer = feestatusserializer(fee_status,many=True)
            return Response(serializer.data)
        else:
            fee_status = feestatus.objects.filter(student_email=student_email)
            serializer = feestatusserializer(fee_status)
            return Response(serializer.data)

    def put(self, request):
        data = request.data
        email = data.get("email")
        try:
            fee_object = feestatus.objects.get(student_email=email)
        except feestatus.DoesNotExist:
            return Response({"message": "User with email ID doesn't exist."}, status=status.HTTP_404_NOT_FOUND)

        fee_object.fee_paid = True
        fee_object.save()
        return Response({"message": "Fee Paid"})

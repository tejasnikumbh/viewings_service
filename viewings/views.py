from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from . import models
from . import serializers

class Viewings(APIView):
	def get(self, request, format=None):
		params = request.query_params
		# TODO:- Validate Request Params else return Bad Request
		user_id = params['user_id']
		user_type = params['user_type']
		status = params['status']
		viewings = []
		if user_type == "tenant":
			viewings = models.Viewing.objects.filter(tenant=user_id, status=status)
		else: # The user is a host
			offices = models.Office.objects.filter(owner=user_id)
			for office in offices:
				viewings += models.Viewing.objects.filter(office=office.id, status=status)
		serializer = serializers.ViewingSerializer(viewings, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		print request.data['name']
		return Response("")
	def put(self, request, format=None):
		print request.data['name']
		return Response("")

class Conversations(APIView):
	def get(self, request, format=None):
		print request.query_params
		return Response("")



from rest_framework import serializers
from . import models

from django.utils import timezone

class ViewingSerializer(serializers.ModelSerializer):

	class Meta:

		fields = (
			'id',
			'created_at',
			'scheduled_time',
			'company_name',
			'number_of_desks',
			'phone_number',
			'description_of_company',
			'move_in_date',
			'hubble_discovery_info',
			'tenant',
			'office',
			'status'
		)
		model = models.Viewing


	def validate_tenant(self, value):
		if not(models.User.objects.filter(id=value.id).exists()) or \
		not(models.User.objects.filter(id=value.id).first().is_tenant):
			print "Tenant not found"
			raise serializers.ValidationError("Tenant Not Found")
		return value
	
	def validate_office(self, value):
		if not(models.Office.objects.filter(id=value.id).exists()):
			print "Office not found"
			raise serializers.ValidationError("Office Not Found")
		return value

	def validate(self, data):
		# Viewings possible only in future
		if not(data['scheduled_time'] > timezone.now()):
			print "Scheduled time has to be in the future"
			raise serializers.ValidationError("Scheduled time has to be in future")
		# Move in date has to be in future
		if not(data['move_in_date'] > timezone.now().date()):
			print "Move in date has to be in future"
			raise serializers.ValidationError("Move in date has to be in future")
		# User cannot schedule viewing at own place
		if data['tenant'].id == data['office'].owner.id:
			print "Cannot schedule viewing at own place"
			raise serializers.ValidationError("User cannot schedule viewing at own place")
		return data
		

class ConversationSerializer(serializers.ModelSerializer):

	class Meta:
		extra_kwargs = {
            'tenant': {'write_only': True},
            'host': {'write_only': True},
        }
		fields = (
			'tenant',
			'host',
			'message',
			'time_stamp'
		)
		model = models.Conversation
	
	def validate_tenant(self, value):
		if not(models.User.objects.filter(id=value.id).exists()) or \
		not(models.User.objects.filter(id=value.id).first().is_tenant):
			print "Tenant not found"
			raise serializers.ValidationError("Tenant Not found")
		return value

	def validate_host(self, value):
		if not(models.User.objects.filter(id=value.id).exists()) or \
		not(models.User.objects.filter(id=value.id).first().is_host):
			print "Host not found"
			raise serializers.ValidationError("Host not found")	
		return value

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		fields = (
			'id',
			'name',
			'is_host',
			'is_tenant'
		)
		model = models.User

	def validate(self, data):
		if not(data['is_host']) and not(data['is_tenant']):
			raise serializers.ValidationError(
				"User needs to be either tenant or host")
		return value

class OfficeSerializer(serializers.ModelSerializer):

	class Meta:
		fields = (
			'id',
			'owner',
			'description'
		)
		model = models.Office

	def validate_owner(self, value):
		if not(models.User.objects.filter(id=value.id).exists()) or \
		not(models.User.objects.filter(id=value.id).first().is_host):
			print "Host not found"
			raise serializers.ValidationError("Host not found")
		return value
	
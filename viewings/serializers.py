from rest_framework import serializers
from . import models

class ViewingSerializer(serializers.ModelSerializer):
	class Meta:
		fields = (
			'id',
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

class ConversationSerializer(serializers.ModelSerializer):
	class Meta:
		fields = (
			'id',
			'tenant',
			'host',
			'message',
			'time_stamp'
		)
		model = models.Conversation
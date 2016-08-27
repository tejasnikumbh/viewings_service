from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from . import models
from . import serializers

from datetime import datetime
import json

class Viewings(APIView):
	def get(self, request, format=None):
		'''

			Useful for viewing all viewings
			Useful for viewing confirmed viewings
			Useful for viewing requested viewings
			Useful for viewing declined viewings
			
			Needs: - User ID as well as User Type

			* URL <server>/api/v1/viewings?user_id=1&user_type=host&status=R
			* Status is optional parameter
		'''
		params = request.query_params
		# Validating if the request parameters are correct
		if not(self._validate_get(params)):
			content = {
				"message": "The page you are looking for cannot be found",
				"detail" : "Refer the API Docs for correct URL Params"
			}
			return Response(content, status = status.HTTP_404_NOT_FOUND)
		# Exist and are correct	
		user_id = params['user_id']
		user_type = params['user_type']
		request_status = "ALL"
		if 'status' in params.keys():
			request_status = params['status']
		
		# Validate if User exists in Database
		if not(models.User.objects.filter(id=user_id).exists()):
			content = {
				"message": "The page you are looking for cannot be found",
				"detail" : "There was no user by that id in the database"
				}
			return Response(content, status = status.HTTP_404_NOT_FOUND)

		# Validate if user_type is correct for user
		user = models.User.objects.filter(id=user_id).first()
		if not((user_type == 'tenant' and user.is_tenant) or \
			(user_type == 'host' and user.is_host)):
			content = {
				"message": "The page you are looking for cannot be found",
				"detail" : "The user_type is not correct for the given user"
			}
			return Response(content, status = status.HTTP_404_NOT_FOUND)
		
		viewings = []
		if user_type == 'tenant':
			if request_status == "ALL": # Fetch all viewings
				viewings = models.Viewing.objects.filter(tenant=user_id)
			else: # Fetch viewings of particular request status
				viewings = models.Viewing.objects.filter(tenant=user_id,
				 status=request_status)
		else: # Fetch offices for user, and viewings for offices
			offices = models.Office.objects.filter(owner=user_id)
			if request_status == "ALL":
				for office in offices:
					viewings += models.Viewing.objects.filter(office=office.id)
			else:
				for office in offices:
					viewings += models.Viewing.objects.filter(office=office.id,
					 status=request_status)
		serializer = serializers.ViewingSerializer(viewings, many=True)
		return Response(serializer.data)		

	def post(self, request, format=None):
		'''
			Useful for requesting a viewing
		'''
		params = request.data
		# Checking if all parameters exist
		if not(self._validate_post(params)):
			content = {
				"message": "Bad Request",
				"detail" : "One or more parameters is missing"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		# Checking if tenant exists
		if not(self._validate_tenant(params['tenant'])):
			content = {
				"message": "Bad Request",
				"detail" : "Tenant not found"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		# Checking if office exists
		if not(self._validate_office(params['office'])):
			content = {
				"message": "Bad Request",
				"detail" : "Office not found"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		tenant = models.User.objects.filter(id=params['tenant']).first()
		office = models.Office.objects.filter(id=params['office']).first()
		viewing = None
		# Checking if viewing exists at office by tenant. 
		# Decline it in that case
		if models.Viewing.objects.filter(office=office, tenant=tenant).exists():
			viewing = models.Viewing.objects.filter(office=office, tenant=tenant)
			viewing.status = 'D'
			self._save_conversation(viewing=viewing, status='D')
			viewing.save()

		try: # Will return bad format if any value not according to format
			viewing = models.Viewing(
				scheduled_time=params['scheduled_time'],
				company_name=params['company_name'],
				number_of_desks=params['number_of_desks'],
				phone_number=params['phone_number'],
				description_of_company=params['description_of_company'],
				move_in_date=params['move_in_date'],
				tenant=tenant,
				office=office,
				status='R')
			viewing.save()
		except:
			content = {
				"message": "Bad Request",
				"detail" : "One or more parameter value not according to format"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)

		self._save_conversation(viewing=viewing, status='R')
		serializer = serializers.ViewingSerializer(viewing)
		return Response(serializer.data)
	
	def put(self, request, format=None):
		'''
			Useful for confirming or declining a viewing
		'''
		params = request.data
		# Checking if all params exist
		if not(self._validate_put(params)):
			content = {
				"message": "Bad Request",
				"detail" : "One or more parameters is missing"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		# Checking if viewing exists
		if not(self._validate_viewing(params['viewing_id'])):
			content = {
				"message": "Bad Request",
				"detail" : "Viewing you are trying to update cannot be found"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		# Checking if host exists
		if not(self._validate_host(params['host_id'])):
			content = {
				"message": "Bad Request",
				"detail" : "Host not found"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		# Checking ig status is of update 
		if not(self._validate_status(params['status'], is_update=True)):
			content = {
				"message": "Bad Request",
				"detail" : "Only updates - Confirmation of Decline allowed"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		
		host = models.User.objects.filter(id=params['host_id']).first()
		viewing = models.Viewing.objects.filter(id=params['viewing_id']).first()
		
		# Checking if viewing has already been processed
		if viewing.status != 'R':
			content = {
				"message": "Bad Request",
				"detail" : "Viewing has already been Processed"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)

		# Checking if viewing is allowed to be modified by host	
		if viewing.office.owner != host:
			content = {
				"message": "Bad Request",
				"detail" : "Host does not own office for which update is being performed"
			}
			return Response(content, status = status.HTTP_400_BAD_REQUEST)
		
		viewing.status = params['status']
		viewing.save()

		self._save_conversation(viewing=viewing, status=params['status'])
		serializer = serializers.ViewingSerializer(viewing)
		return Response(serializer.data)
		
	def _save_conversation(self, viewing, status):
		tenant_name = viewing.tenant.name
		host_name = viewing.office.owner.name
		processed_at_date_time = datetime.now()
		requested_for_date_time = viewing.scheduled_time
		message_start = ""
		if status == 'R':
			message_start = tenant_name + " requested a viewing on "
			message_end = " with " + host_name
		elif status == 'D':
			message_start = host_name + " declined a viewing on "
			message_end = " with " + tenant_name		
		else:
			message_start = host_name + " confirmed a viewing on "
			message_end = " with " + tenant_name
		message_core = str(processed_at_date_time) + \
						" for " + \
						str(requested_for_date_time)
		message = message_start + message_core + message_end
		conversation = models.Conversation(
			tenant=viewing.tenant,
			host=viewing.office.owner,
			message=message)
		conversation.save()


	def _validate_get(self, params):
		'''
			Doesn't fail if there are extra params, which at 
			this point seems unnecessary.

			* Checks for all required fields being present
			* Checks for all required fields having correct data
		'''
		if not('user_id' in params.keys() and \
			'user_type' in params.keys()):
			return False
		user_id_valid = self._validate_int(params['user_id'])
		user_type_valid = self._validate_user_type(params['user_type'])
		result = user_id_valid and user_id_valid
		print result
		if 'status' in params.keys():
			status_valid = self._validate_status(params['status'])
			result = result and status_valid
		print result
		return result

	def _validate_post(self, params):
		'''
			Checks if post params are according to the spec, else 
			returns False
		'''
		keys = params.keys()
		if not('scheduled_time' in keys and \
			'company_name' in keys and \
			'number_of_desks' in keys and \
			'phone_number' in keys and \
			'description_of_company' in keys and \
			'move_in_date' in keys and \
			'hubble_discovery_info' in keys and \
			'tenant' in keys and \
			'office' in keys):
			return False	
		return True

	def _validate_put(self, params):
		'''
			Checks if put params are according to the spec, else
			returns False
		'''
		keys = params.keys()
		if not('viewing_id' in keys and \
			'host_id' in keys and \
			'status' in keys):
			return False
		return True

	def _validate_int(self, string):
		try: int(string)
		except: return False
		return True

	def _validate_user_type(self, user_type):
		return user_type == 'tenant' or user_type == 'host'

	def _validate_status(self, status, is_update=False):
		if is_update: return status == 'C' or status == 'D'
		else: return status == 'R' or status == 'C' or status == 'D'

	def _validate_tenant(self, tenant_id):
		return models.User.objects.filter(id=tenant_id).exists() and \
		models.User.objects.filter(id=tenant_id).first().is_tenant

	def _validate_host(self, host_id):
		return models.User.objects.filter(id=host_id).exists() and \
		models.User.objects.filter(id=host_id).first().is_host
	
	def _validate_office(self, office_id):
		return models.Office.objects.filter(id=office_id).exists()

	def _validate_viewing(self, viewing_id):
		return models.Viewing.objects.filter(id=viewing_id).exists()
	

class Conversations(APIView):
	def get(self, request, format=None):
		'''
			Returns conversations for a given user
		'''
		params = request.query_params
		# Checking if request valid
		if not(self._validate_get(params)):
			content = {
				"message": "The page you are looking for cannot be found",
				"detail" : "Refer the API Docs for correct URL Params"
			}
			return Response(content, status = status.HTTP_404_NOT_FOUND)
		# Checking if user is in db	
		if not(self._validate_user(params['user_id'])):
			content = {
				"message": "The page you are looking for cannot be found",
				"detail" : "User not found"
			}
			return Response(content, status = status.HTTP_404_NOT_FOUND)
		
		user_id = int(params['user_id'])
		#print tenant
			
		as_tenant = models.Conversation.objects.filter(tenant=user_id)
		hosts = set()
		host_vals = as_tenant.values('host')
		for host in host_vals:
			host_id = host['host']
			hosts.add(host_id)
		as_tenant_threads = {}
		for host_id in hosts:
			host = models.User.objects.filter(id=host_id).first()
			as_tenant_threads["host_name"] = host.name
			serializer = serializers.ConversationSerializer(
				as_tenant.filter(host=host).order_by('time_stamp').only('message', 'time_stamp'),
				many=True)
			as_tenant_threads["messages"] = serializer.data
			

		as_host = models.Conversation.objects.filter(host=user_id)
		tenants = set()
		tenant_vals = as_host.values('tenant')
		for tenant in tenant_vals:
			tenant_id = tenant['tenant']
			tenants.add(tenant_id)
		as_host_threads = {}
		for tenant_id in tenants:
			tenant = models.User.objects.filter(id=tenant_id).first()
			as_host_threads["tenant_name"] = tenant.name
			serializer = serializers.ConversationSerializer(
				as_host.filter(tenant=tenant).order_by('time_stamp').only('message', 'time_stamp'),
				many=True)
			as_host_threads["messages"] = serializer.data

		conversation = { 
			"as_host": as_host_threads, 
			"as_tenant": as_tenant_threads
		}
		response = json.dumps(conversation)
		response = json.JSONDecoder().decode(response)
		return Response(response)

	def _validate_int(self, string):
		try: int(string)
		except: return False
		return True

	def _validate_get(self, params):
		if 'user_id' not in params.keys():
			return False
		return self._validate_int(params['user_id'])
		
	def _validate_user(self, id):
		return models.User.objects.filter(id=id).exists()
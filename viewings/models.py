from __future__ import unicode_literals

from django.db import models

REQUEST_STATUS = (
    ('R', 'Requested'),
    ('C', 'Confirmed'),
    ('D', 'Declined'),
)

class Viewing(models.Model):
	scheduled_time = models.DateTimeField()
	company_name = models.CharField(max_length=255)
	number_of_desks = models.IntegerField()
	phone_number = models.CharField(max_length=255)
	description_of_company = models.TextField()
	move_in_date = models.DateField()
	hubble_discovery_info = models.TextField(blank=True, default="")
	tenant = models.ForeignKey('User', related_name='tenant_user')
	office = models.ForeignKey('Office', related_name='office')
	status = models.CharField(max_length=1, choices = REQUEST_STATUS)
	

class Conversation(models.Model):
	tenant = models.ForeignKey('User', related_name='tenant')
	host = models.ForeignKey('User', related_name='host')
	message = models.TextField()
	time_stamp = models.DateTimeField()


# Dummy Models for simulating functionality
class User(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class Office(models.Model):
	owner = models.ForeignKey(User, related_name='owner')
	description = models.CharField(max_length=255)
	def __str__(self):
		return self.description
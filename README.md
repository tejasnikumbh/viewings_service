Hubble Microservice
==============================

Hubble Microservice for Managing Viewings and Conversations

Running the Project
--------------------
* To run the project, simply type in the following command while in the root of the project

	```python manage.py runserver 0.0.0.0:8000```

  	- This will run the project on the 8000 port of 0.0.0.0 of your machine

* If you'd like creating and destroying projects, make a super user using the following 

	```python manage.py createsuperuser```

  	- And use the credentials you enter to log into the admin


API Endpoints
--------------

Viewings


* URL:- <servername>/api/v1/viewings(/ for POST/PUT)

  - GET
  	
  	Parameters are necessary. Validators for them are in place
  	
  	params => ``` user_id=<some_id>&user_type=<tenant or host> ```

  	params => ``` user_id=<some_id>&user_type=<tenant or host>&status=<R or C or D>```

    - Functionality 
    	- Can be used to retrieve all confirmed viewings for tenant [user_id, tenant, C]
    	- Can be used to retrieve all confirmed viewings for hosts [user_id, host, C]
    - Example

        ``` 0.0.0.0:8000/api/v1/viewings/user_id=1&user_type=tenant&status=C ```
        ``` 0.0.0.0:8000/api/v1/viewings/user_id=1&user_type=host&status=C ```
    - Additional functionality
    	- Can be used to retrieve all viewings for a particular user & type
    	- Can be used to retrieve Requested Viewings for a particular user & type    
    	- Can be used to retrieve Declined Viewings for a particular user & type
    - Sample Response

    ```javascript
    [
    	{
    	 "id": 1,
    	 "scheduled_time": "2016-08-08T06:00:00Z",
    	 "company_name": "Hubble",
    	 "number_of_desks": 3,
    	 "phone_number": "7766666666",
    	 "description_of_company": "Hubble is a Office Rental Space Company in London",
    	 "move_in_date": "2016-08-16",
    	 "hubble_discovery_info": "Through friends",
    	 "tenant": 1,
    	 "office": 2,
    	 "status": "R"
    	 }
     ]
    ```

  - POST
  	No parameters necessary, Can directly send a POST request to URL with a JSON body as follows
  	
  	* Stretch Goal - Check if the viewing time clashes with another booked viewing at same place *
  	
  	- Functionality
     	- Can be used to request a viewing by a tenant
     	- Value of status field can be 'R' only. Validators in place
    - Example 

    ```javascript
    [
    	{
         "scheduled_time": "2016-08-08T06:00:00Z",
         "company_name": "Hubble",
         "number_of_desks": 3,
         "phone_number": "7766666666",
         "description_of_company": "Hubble is a Office Rental Space Company in London",
         "move_in_date": "2016-08-16",
         "hubble_discovery_info": "Through friends",
         "tenant": 1,    	     
         "office": 2,
    	}
     ]
   	``` 
   - PUT
   	No parameters required, Can directly send a PUT request to URL with a JSON body as follows
	Note that accepted value in status field is C or D only, since the endpoint is intended for 
  	updating old viewings only. Validators are in place. Also returns 404 if the viewing_id is not 
  	found in database.
  	Another point is host has to own the place of the viewing, else error is raised
  	- Functionality
  		- Can be used to accept or decline a viewing by a host
  	- Example

  	```javascript
     [
     	{
         "viewing_id": 1,
         "host_id": 1,
         "status": "C"
     	}
     ]
    ```
    

Conversations
=============

* URL:- <server_name>/api/v1/conversations
    - GET
	- Parameters are necessary. Validators are in place.
	- params => ``` user_id=<some_id> ```
    - Functionality 
    	- Can be used to retrieve all conversations for user [tenant or host]
    - Example
        ``` 0.0.0.0:8000/api/v1/conversations/user_id=1 ```
    	- The conversations are grouped by user_id of the conversing partner.
    	- Sample Response:-  Note tenant id is same for as_tenant, same with as_host

	```javascript
	{
	    "as_host": {
		    "tenant_name": "Abhishek Gupta",
		    "messages": [
            		{
                		"time_stamp": "2016-08-27T14:40:17.801918Z",
                		"message": "Need an office space at somepoint"
            		},
		        {
                		"time_stamp": "2016-08-27T14:40:39.311452Z",
                		"message": "Sorry man can't do it"
            		}]
            },
	    "as_tenant": {
	    
	    }
	}
    	```
    	

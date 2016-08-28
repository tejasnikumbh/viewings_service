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
=========

* URL:- <servername>/api/v1/viewings(/ for POST/PUT)
* Request Type:- GET
    - Parameters are necessary. Validators for them are in place
    	- params =>  ``` user_id=<some_id>&user_type=<tenant or host> ```
    	- params =>  ``` user_id=<some_id>&user_type=<tenant or host>&status=<R or C or D> ```
    - Functionality 
    	- Can be used to retrieve all confirmed viewings for tenant [user_id, tenant, C]
    	- Can be used to retrieve all confirmed viewings for hosts [user_id, host, C]
    - Validations
    	- Checks if all parameters exist and are in proper format
    	- Checks if user exists
    	- Checks if user is of the specified type [tenant or host]
    - Example
        - ``` 0.0.0.0:8000/api/v1/viewings/user_id=1&user_type=tenant&status=C ```
        - ``` 0.0.0.0:8000/api/v1/viewings/user_id=1&user_type=host&status=C ```
    - Additional functionality
    	- Can be used to retrieve all viewings for a particular user & type
    	- Can be used to retrieve Requested Viewings for a particular user & type    
    	- Can be used to retrieve Declined Viewings for a particular user & type
    - Sample Response
    ``` javascript
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

* Request Type:- POST
    - No parameters necessary, Can directly send a POST request to URL with a JSON body as follows
    - * Stretch Goal - Check if the viewing time clashes with another booked viewing at same place *
    - Functionality
     	- Can be used to request a viewing by a tenant
    - Validations
     	- Checks if all parameters are present and in proper format
     	- Checks if tenant exists
     	- Checks if office exists
     	- If same tenant has scheduled a viewing previously, declines it and adds new viewing
     	- Checks if scheduled time is in future {In Serializer}
     	- Checks if move in date is in future {In Serializer}
     	- Checks if tenant is not scheduling viewing at his own place[when he is a host as well] {In Serializer}
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
* Request Type:- PUT
    - No parameters required, Can directly send a PUT request to URL with a JSON body as follows
    - Note that accepted value in status field is C or D only, since the endpoint is intended for updating old viewing only. Validators are in place. Also returns 404 if the viewing_id is not found in database.
    - Another point is host has to own the place of the viewing, else error is raised
    - Functionality
    	- Can be used to accept or decline a viewing by a host
    - Validations
     	- Checks if all parameters exist and are in proper format
     	- Checks if viewing exists
     	- Checks if host exists
     	- Checks if update is performed [R is not Allowed in status field]
     	- Checks if viewing has already been processed
     	- Checks if office at viewing is owned by host
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
* Request Type:- GET
	- Parameters are necessary. Validators are in place.
	- params => ``` user_id=<some_id> ```
    - Functionality 
    	- Can be used to retrieve all conversations for user [tenant or host]
    	- Since a user can be both a tenant and a host, the fields both types of conversations
    	- Also, keeping in mind that host and tenant dashboards for conversations will be different, they have been grouped differently as such
    - Validations
    	- Checks for request parameter structure
    	- Checks if user_id is in proper format
    	- Checks if user_id exists
    	- Checks if user is not talking to himself {In Serializer}
    - Example
        ``` 0.0.0.0:8000/api/v1/conversations/user_id=1 ```
    	- The conversations are grouped by user_id of the conversing partner.
    - Sample Response:-  Note tenant id is same for as_tenant, same with as_host

```javascript
 {
    "user_name": "Tejas Nikumbh",
    "messages": {
        "as_host": [
            {
                "partner_name": "Paul Golding",
                "messages": [
                    {
                        "time_stamp": "2016-08-28T07:51:56.618565Z",
                        "message": "Paul Golding requested a viewing on 2016-08-28 07:51:56.611504 for 2016-08-30T18:00:00Z with Tejas Nikumbh at Office in Bermondsey"
                    },
                    {
                        "time_stamp": "2016-08-28T08:09:37.821563Z",
                        "message": "Tejas Nikumbh declined a viewing on 2016-08-28 08:09:37.814651 for 2016-08-30 18:00:00+00:00 with Paul Golding at Office in Bermondsey"
                    },
                    {
                        "time_stamp": "2016-08-28T08:09:37.836511Z",
                        "message": "Paul Golding requested a viewing on 2016-08-28 08:09:37.830209 for 2016-08-29T18:00:00Z with Tejas Nikumbh at Office in Bermondsey"
                    },
                    {
                        "time_stamp": "2016-08-28T08:10:46.350935Z",
                        "message": "Tejas Nikumbh confirmed a viewing on 2016-08-28 08:10:46.341277 for 2016-08-29 18:00:00+00:00 with Paul Golding at Office in Bermondsey"
                    }
                ]
            },
            {
                "partner_name": "Kasia Streich",
                "messages": [
                    {
                        "time_stamp": "2016-08-28T07:51:09.051529Z",
                        "message": "Kasia Streich requested a viewing on 2016-08-28 07:51:09.042243 for 2016-08-30T18:00:00Z with Tejas Nikumbh at Office in USA"
                    },
                    {
                        "time_stamp": "2016-08-28T07:57:03.784420Z",
                        "message": "Tejas Nikumbh confirmed a viewing on 2016-08-28 07:57:03.778114 for 2016-08-30 18:00:00+00:00 with Kasia Streich at Office in USA"
                    }
                ]
            },
            {
                "partner_name": "Abhishek Gupta",
                "messages": [
                    {
                        "time_stamp": "2016-08-28T07:50:54.671956Z",
                        "message": "Abhishek Gupta requested a viewing on 2016-08-28 07:50:54.664798 for 2016-08-30T18:00:00Z with Tejas Nikumbh at Office in Waterloo"
                    },
                    {
                        "time_stamp": "2016-08-28T07:50:57.958699Z",
                        "message": "Abhishek Gupta requested a viewing on 2016-08-28 07:50:57.950520 for 2016-08-30T18:00:00Z with Tejas Nikumbh at Office in USA"
                    },
                    {
                        "time_stamp": "2016-08-28T07:57:10.536128Z",
                        "message": "Tejas Nikumbh confirmed a viewing on 2016-08-28 07:57:10.529209 for 2016-08-30 18:00:00+00:00 with Abhishek Gupta at Office in USA"
                    },
                    {
                        "time_stamp": "2016-08-28T07:57:15.559649Z",
                        "message": "Tejas Nikumbh confirmed a viewing on 2016-08-28 07:57:15.552640 for 2016-08-30 18:00:00+00:00 with Abhishek Gupta at Office in Waterloo"
                    }
                ]
            }
        ],
        "as_tenant": [
            {
                "partner_name": "Steph Pau",
                "messages": [
                    {
                        "time_stamp": "2016-08-28T07:53:53.962725Z",
                        "message": "Tejas Nikumbh requested a viewing on 2016-08-28 07:53:53.956227 for 2016-08-30T18:00:00Z with Steph Pau at Office in Shoreditch"
                    },
                    {
                        "time_stamp": "2016-08-28T08:02:03.259660Z",
                        "message": "Steph Pau confirmed a viewing on 2016-08-28 08:02:03.253584 for 2016-08-30 18:00:00+00:00 with Tejas Nikumbh at Office in Shoreditch"
                    }
                ]
            },
            {
                "partner_name": "Mahtab Ghamsari",
                "messages": [
                    {
                        "time_stamp": "2016-08-28T07:54:01.181889Z",
                        "message": "Tejas Nikumbh requested a viewing on 2016-08-28 07:54:01.168367 for 2016-08-30T18:00:00Z with Mahtab Ghamsari at Office in Westminster"
                    },
                    {
                        "time_stamp": "2016-08-28T08:03:06.827695Z",
                        "message": "Mahtab Ghamsari confirmed a viewing on 2016-08-28 08:03:06.820990 for 2016-08-30 18:00:00+00:00 with Tejas Nikumbh at Office in Westminster"
                    }
                ]
            }
        ]
    }
}
```
    	

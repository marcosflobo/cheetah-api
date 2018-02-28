# API versions
**Table of Contents**
<!--ts-->
* [V1](#v1)
  * [Struncture](#structure)
    * [Examples](#examples)
  * [Headers](#headers)
  * [Common responses](#common-responses)
  * [Definition](#definition)
    * [Actions](#actions)
    * [Countries](#countries)
    * [Bank Holidays](#bank-holidays)
    * [Holidays](#holidays)
    * [Login](#login)
    * [Profiles](#profiles)
    * [Projects](#projects)
    * [Releases](#releases)
    * [Sprints](#sprints)
    * [Stories](#stories)
    * [Teams](#teams)
    * [Users](#users)
       * [List users](#list-users)
       * [Get user](#get-user)
       * [Create user](#create-user)
       * [Update user](#update-user)
       * [Delete user](#delete-user)
<!--ts-->
# V1
This is Cheetah API V1 definition
## Structure
`HTTP_METHOD /v1/<entity>/(action|parameter)*/(param/)*`
### Examples
Get team list
`GET /v1/team/`

Get a user information
`GET /v1/user/user_id`

Login
`POST /v1/login`

Add user to team
`GET /v1/team/adduser/team_id/user_id`

## Headers
TODO

## Common responses
### 401 Unauthorized
All API calls, except POST /v1/login, can return this response
```javascript
{
	"response": {
		"status": 401,
		"message": "Unauthorized action"
	}
}
```
### 403 Forbidden
All API calls, except POST /v1/login, can return this response
```javascript
{
	"response": {
		"status": 401,
		"message": "Forbidden action"
	}
}
```

# Definition
## Actions
### Request
TODO
### Response
TODO
## Countries
### Request
TODO
### Response
TODO
## Bank Holidays
### Request
TODO
### Response
TODO
## Holidays
### Request
TODO
### Response
TODO
## Login
### Request
TODO
### Response
TODO
## Profiles
Here we are talking about user roles
### Request
TODO
### Response
TODO
## Projects
### Request
TODO
### Response
TODO
## Releases
### Request
TODO
### Response
TODO
## Sprints
### Request
TODO
### Response
TODO
## Stories
### Request
TODO
### Response
TODO
## Teams
### Request
TODO
### Response
TODO

## Users
### List Users
List users
### Role
Admin
#### Request
`GET /v1/users/`
#### Response
```javascript
{
    "users": [
        {
        	"id": 0,
        	"login": "",
        	"name": "",
        	"profile_id": 0,
        	"country_id": 0
        }
    ]
}
```
#### Request
`GET /v1/users/extended/`
#### Response
```javascript
{
    "users": [
        {
        	"id": 0,
        	"login": "",
        	"name": "",
        	"profile": {...},
        	"country": {...},
        }
    ]
}
```
### Get user
Get user information from the user id
#### Request
`GET /v1/users/{id}`
#### Response
```javascript
{
    "user": {
    	"id": 0,
        "login": "",
        "name": "",
        "profile_id": 0,
        "country_id": 0
    }
}
```
#### Response ERROR User not found
The user id is not found
```javascript
{
	"response": {
		"status": 404,
		"message": "User not found"
	}
}
```
#### Request
`GET /v1/users/{id}/extended/`
#### Response
```javascript
{
    "user": {
    	"id": 0,
        "login": "",
        "name": "",
        "profile": {...},
        "country": {...}
    }
}
```
#### Response ERROR User not found
The user id is not found
```javascript
{
	"response": {
		"status": 404,
		"message": "User not found"
	}
}
```
### Create user
Create a new user
#### Request
`POST /v1/users/`
##### Body
```javascript
{
    "user": {
        "login": "",
        "pw": "",
        "name": "",
        "profile_id": 0,
        "country_id": 0
    }
}
```
#### Response OK
```javascript
{
	"response": {
		"status": 201,
		"message": "User created",
		"id": 0
	}
}
```
#### Response ERROR Bad Request
The request body is wrong
```javascript
{
	"response": {
		"status": 400,
		"message": "The request is invalid"
	}
}
```
#### Response ERROR Forbidden
The user does not have permissions to perform this action
```javascript
{
	"response": {
		"status": 403,
		"message": "User creation forbidden"
	}
}
```
### Update user
Update an existing user
#### Request
`PUT /v1/users/{id}/`
##### Body
```javascript
{
    "user": {
        "login": "",
        "pw": "",
        "name": "",
        "profile_id": 0,
        "country_id": 0
    }
}
```
#### Response OK
```javascript
{
	"response": {
		"status": 204,
		"message": "User updated",
		"id": 0,
		"login": "",
		"name": "",
		"profile_id": 0,
		"country_id": 0
	}
}
```
#### Response ERROR Bad Request
The request body is wrong. Possible reasons:
- The login cannot be duplicated
```javascript
{
	"response": {
		"status": 400,
		"message": "The request is invalid"
	}
}
```
#### Response ERROR User not found
The user id is not found
```javascript
{
	"response": {
		"status": 404,
		"message": "User not found"
	}
}
```
### Delete user
Delete an existing user
#### Request
`DELETE /v1/users/{id}/`
##### Body
EMPTY
#### Response OK
```javascript
{
	"response": {
		"status": 202,
		"message": "User deleted"
	}
}
```
#### Response ERROR Bad Request
The request body is wrong.
```javascript
{
	"response": {
		"status": 400,
		"message": "The request is invalid"
	}
}
```
#### Response ERROR User not found
The user id is not found
```javascript
{
	"response": {
		"status": 404,
		"message": "User not found"
	}
}
```
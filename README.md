# It is a program for writing and reading news.
I wrote tests for this program. For this I used pytest and unittest.

# This programm is API for service named "Yatube". This API uses next models: Post, Comment, Follow, Group, User. 

You can create posts, change it and delete. You can write comments, follow by someone and have groups with this API.
## How to launch a project:
Clone the repository and go to it on the command line:

`git clone https://github.com/Antochino/api_final_yatube.git`

`cd yatube_api/`

## Create and activate a virtual environment:

`python3 -m venv env`

`source env/bin/activate`

## Install dependencies from a file requirements.txt:

`python3 -m pip install --upgrade pip`

`pip install -r requirements.txt`

## Perform migrations:

`python3 manage.py migrate`

## Launch a project:

`python3 manage.py runserver`

## Request examples

Request: `http://127.0.0.1:8000/api/v1/posts/`

Response: `{
  "text": "string",
  "image": "string",
  "group": 0
}`

Request: `http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/`

Response:`[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]`

### Techonologies: 

REST API, Viewsets, routers, JWT, serializers, permissions, limits, pagination, sorting.

### Author: 
Elizaveta Ilicheva

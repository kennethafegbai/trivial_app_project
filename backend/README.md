# API DOCUMENTAION

### Introduction
This API allows you manage a pool of questions and categories for a Trivia app.

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "message": "Bad request",
    "error": 400,
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method not allowed
- 500: Server error

### Endpoints 

### categories

### GET /categories

### Query parameters
This endpoint does not require query parameter

### Request body
This endpoint does not require request body

### Sample request

- `curl -X GET http://127.0.0.1:5000/categories`

### Sample response

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### GET '/categories/question_id/questions
- return questions based on category id

### Query parameters
This endpoint does not require query parameter

### Request body
This endpoint does not require request body

### Sample request

- `curl -X GET http://127.0.0.1:5000/categories/4/questions`

### Sample response

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    },

     {
      "id": 6,
      "question": "This is a question6",
      "answer": "This is an answer6",
      "difficulty": 3,
      "category": 4
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History"
}
```

#### questions

### GET /questions
Returns 10 questions per page

### Query parameters
`page` : int(optional) - page number starting from 1

### Request body
This endpoit does not require request body

### Sample request

- `curl -X GET http://127.0.0.1:5000/questions`

### Sample response

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History"
}
```

### POST /questions
add a new question to database

### Query parameters
No query parameter

### Request body
accepts `question`, `answer`, `difficulty`, and `category` as request body in json format.
`question` - `text`
`answer` - `string`
`category` - `integer`
`difficulty` - `integer`

```json
{
  "question": "What is my name",
  "answer": "Kenneth Afegbai",
  "difficulty": 4,
  "category": 3
}
```

### Sample request

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is my name?", "answer":"Kenneth Afegbai", "category":5, "difficulty":3}'`

### Sample response

```json
{
  "success": true,
  "added": 24,
}
```

#### POST /questions (search for questions)
- search the database with a search term and return questions if any match otherwise returns not found

### Query parameters
No query parameter

### Request body
accepts `searchTerm` as request body in json format
`searchTerm` - `string`

```json
{
  "searchTerm": "title"
}
```
### Sample request

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm:"title"}'`

### Sample response

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History"
}
```

#### POST /quizzes
- Randomly pick a question from database at a time using a specified `quiz_category` and `previous_questions` array. The `previous_questions` makes it possible not to pick an already choosen question

### Query parameters
No query parameter

### Request body
accepts `quiz_category` and `previous_questions` as response body in json format
`quiz_category` - `integer`
`previous_questions` - `array`

```json
{
  "quiz_category": 4,
  "previous_questions":[1, 6, 10]
}
```
### Sample request

- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":"4","previous_questions":[1, 6, 10]}'`


### Sample response

```json
{
   "question": {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
    }
}
```

### DELETE '/questions/question_id

### Query parameters
No query parameter

### Request body
No request body is required

### Sample request

- `curl -X DELETE http://127.0.0.1:5000/questions/2`

### Sample response

```json
  {
      "success":true,
      "deleted": 2,
      "message": "delete successful"
  }
```

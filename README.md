# FastAPI Application: MySQL and MongoDB Integration  
   
This repository contains a FastAPI application that integrates with MySQL and MongoDB to provide APIs for managing and querying datasets, comments, ratings, and evaluators.  
   
## Features  
   
- **MySQL Integration**: Store ratings, datasets, and evaluator information.  
- **MongoDB Integration**: Store and retrieve comments.  
- **RESTful APIs**: Endpoints for adding, querying, and managing data.  
- **Async Support**: Fully asynchronous implementation using `FastAPI`, `SQLAlchemy`, and `Motor`.  
   
---  
   
## Table of Contents  
   
- [Setup](#setup)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Environment Variables](#environment-variables)  
- [API Endpoints](#api-endpoints)  
  - [Rate a Comment](#rate-a-comment)  
  - [Get Comments](#get-comments)  
  - [Add Comments](#add-comments)  
  - [Add Dataset](#add-dataset)  
  - [Get All Evaluators](#get-all-evaluators)  
  - [Check Evaluator](#check-evaluator)  
- [Running the Application](#running-the-application)  
- [Project Structure](#project-structure)  
- [Technologies Used](#technologies-used)  
- [License](#license)  
   
---  
   
## Setup  
   
### Prerequisites  
   
Before you begin, ensure you have the following installed:  
   
- Python 3.8 or higher  
- MySQL database  
- MongoDB database  
- `pip` for managing Python packages  
   
---  
   
### Installation  
   
1. **Clone the repository**:  
  
    ```bash  
    git clone https://github.com/yourusername/yourrepository.git  
    cd yourrepository  
    ```  
   
2. **Install dependencies**:  
  
    ```bash  
    pip install -r requirements.txt  
    ```  
   
3. **Set up the database**:  
   - Create the necessary tables in your MySQL database using the schema defined in the `ratings_table`, `comments_table`, and `evaluators_table`.  
   - Ensure MongoDB is running and accessible.  
   
---  
   
### Environment Variables  
   
Create a `.env` file in the root directory to store environment variables. Example:  
   
```dotenv  
# MySQL Configuration  
MYSQL_USER=user  
MYSQL_PASSWORD=password  
MYSQL_HOST=localhost  
MYSQL_PORT=3306  
MYSQL_DB=dbname  
   
# MongoDB Configuration  
MONGODB_USER=user  
MONGODB_PASSWORD=password  
MONGODB_HOST=localhost  
MONGODB_PORT=27017  
MONGODB_DB=mydatabase  
```  
   
---  
   
## API Endpoints  
   
### 1. **Rate a Comment**  
   
- **Endpoint**: `/ratecomment`  
- **Method**: `POST`  
- **Description**: Adds a rating for a comment.  
   
#### Request Body:  
   
```json  
{  
  "d_id": 1,  
  "c_id": 101,  
  "u_id": 1001,  
  "rating": 5,  
  "flag": true,  
  "other": "Great comment!"  
}  
```  
   
#### Response:  
   
```json  
{  
  "message": "Rating submitted successfully"  
}  
```  
   
---  
   
### 2. **Get Comments**  
   
- **Endpoint**: `/getcomments`  
- **Method**: `GET`  
- **Description**: Retrieves comments for a specific dataset.  
   
#### Query Parameters:  
   
- `d_id` (int): Dataset ID.  
   
#### Response:  
   
```json  
{  
  "comments": [  
    {"c_id": 101, "text": "This is a great dataset!"},  
    {"c_id": 102, "text": "Interesting findings."}  
  ]  
}  
```  
   
---  
   
### 3. **Add Comments**  
   
- **Endpoint**: `/addcomments`  
- **Method**: `POST`  
- **Description**: Adds a list of comments to MongoDB.  
   
#### Request Body:  
   
```json  
[  
  {"c_id": 101, "text": "This is a great dataset!"},  
  {"c_id": 102, "text": "Interesting findings."}  
]  
```  
   
#### Response:  
   
```json  
{  
  "message": "Comments added successfully"  
}  
```  
   
---  
   
### 4. **Add Dataset**  
   
- **Endpoint**: `/adddataset`  
- **Method**: `POST`  
- **Description**: Adds a dataset with a list of comment IDs to MySQL.  
   
#### Request Body:  
   
```json  
{  
  "d_id": 1,  
  "c_id_list": [101, 102, 103]  
}  
```  
   
#### Response:  
   
```json  
{  
  "message": "Dataset added successfully"  
}  
```  
   
---  
   
### 5. **Get All Evaluators**  
   
- **Endpoint**: `/allevaluators`  
- **Method**: `GET`  
- **Description**: Retrieves all evaluators from the MySQL database.  
   
#### Response:  
   
```text  
1, John Doe  
2, Jane Smith  
```  
   
---  
   
### 6. **Check Evaluator**  
   
- **Endpoint**: `/checkevaluator`  
- **Method**: `POST`  
- **Description**: Checks if an evaluator exists by name. If not, adds a new evaluator.  
   
#### Request Body:  
   
```json  
{  
  "name": "John Doe"  
}  
```  
   
#### Response (if evaluator exists):  
   
```json  
{  
  "u_id": 1  
}  
```  
   
#### Response (if evaluator is added):  
   
```json  
{  
  "message": "Evaluator added",  
  "u_id": 3  
}  
```  
   
---  
   
## Running the Application  
   
1. **Start the FastAPI server**:  
  
   Run the following command to start the development server:  
  
   ```bash  
   uvicorn main:app --reload  
   ```  
  
   Replace `main` with the filename containing your FastAPI app if it's named differently.  
   
2. **Access the API documentation**:  
  
   Open your browser and navigate to:  
  
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  
   
---  
   
## Project Structure  
   
```  
.  
├── main.py                # Main application file  
├── requirements.txt       # Dependencies  
├── .env                   # Environment variables (not included in the repo for security)  
└── README.md              # Documentation  
```  
   
---  
   
## Technologies Used  
   
- **[FastAPI](https://fastapi.tiangolo.com/)**: A modern, fast web framework for Python.  
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM for interacting with MySQL.  
- **[Motor](https://motor.readthedocs.io/)**: Asynchronous MongoDB driver for Python.  
- **[MySQL](https://www.mysql.com/)**: Relational database for structured data.  
- **[MongoDB](https://www.mongodb.com/)**: NoSQL database for unstructured data.  
   
---  
   
## License  
   
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
   
---  
   
Feel free to contribute to the project by submitting issues or pull requests. If you have any questions, don't hesitate to reach out!  
   
Happy coding! 🚀


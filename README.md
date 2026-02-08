Metadata Management API – FastAPI Assignment

1. Overview

This project implements a Metadata Management System using FastAPI and SQLAlchemy.
The system manages:
•	Datasets – logical collections of data
•	Data Elements – columns/fields belonging to a dataset
The API supports CRUD operations and enforces key business rules such as dataset uniqueness and referential integrity.
This project focuses on metadata only, not actual data storage.

2. Tech Stack

•	Framework: FastAPI
•	ORM: SQLAlchemy
•	Validation: Pydantic
•	Database: SQLite
•	Testing: Pytest
•	Server: Uvicorn

3. Data Model

Dataset (1) ─────── (N) DataElement (One to many relationship)

One dataset can have multiple data elements
Each data element belongs to exactly one dataset

3.2 Dataset Table (datasets)

Column	       Type	           Description
id	          Integer	   Primary Key (auto-increment)
name	      String	   Unique dataset name
description	  String	   Dataset description
created_at	  DateTime	   Auto-generated timestamp


3.3 DataElement Table (data_elements)

Column	        Type	     Description
id	           Integer	      Primary Key
dataset_id	   Integer	      Foreign Key → datasets.id
name	       String	      Column name
data_type	   String	      Data type (string, int, etc.)
nullable	   Boolean	      Whether column allows NULL
created_at	   DateTime	      Auto-generated timestamp

4. Key Design Decisions

4.1 Metadata-Only Design

The application stores metadata, not actual data.
This aligns with real-world data catalog and data governance systems.

4.2 RESTful API Design

•	GET → Read metadata
•	POST → Create metadata
•	DELETE → Remove metadata

4.3 ORM + Pydantic Separation

•	SQLAlchemy handles persistence
•	Pydantic handles request/response validation
•	Prevents leaking database internals to API users

4.4 Relationship Handling

•	SQLAlchemy relationships with cascade delete
•	Deleting a dataset removes its data elements automatically

5. Business Rules Enforced
•	Dataset name must be unique
•	Cannot delete a dataset that does not exist
•	Data elements must reference a valid dataset
•	Proper HTTP errors are returned for invalid operations

6. Assumptions
•	SQLite is sufficient for assignment scope
•	Authentication and authorization are out of scope
•	Hard delete is used (no soft delete)
•	Data types are stored as strings (no enum validation)

7. Project Structure

api_assignment/
│
├── main.py
├── database.py
├── models.py
├── schema.py
│
├── routers/
│   └── manage.py        # API routes
│
├── tests/
│   └── test_dataset.py
│
├── requirements.txt
└── README.md

8. API Endpoints

Dataset APIs

Method	      Endpoint	                       Description
GET	       /list_datasets	                List all datasets
GET	       /read_all_datasets	            Datasets with data elements
GET	       /read_specific_dataset/{id}	    Data elements of a dataset
POST	   /add_dataset	                    Create a new dataset
DELETE	   /delete_dataset/{dataset_name}	Delete dataset by name
________________________________________
Data Element APIs

Method	   Endpoint	          Description
GET	    /list_data_element	List all data elements
POST	/add_dataelement	Create a data element

9. How to Run the Application

9.1 Create Virtual Environment

python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows

9.2 Install Dependencies
pip install -r requirements.txt

9.3 Run the Server (RUN the TEST First)
uvicorn main:app –reload

For Swagger UI
just add “/docs” in the URL

10. How to Run Tests
python -m pytest

Test Coverage
•	Verifies dataset creation
•	Validates HTTP status codes
•	Confirms response structure
•	Ensures business rules are enforced (One one dataset of a particular name)


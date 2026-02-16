# Metadata Management API – FastAPI Assignment

## Overview
This project implements a Metadata Management System using FastAPI and SQLAlchemy. The system manages:
- **Datasets** – logical collections of data
- **Data Elements** – columns/fields belonging to a dataset

The API supports CRUD operations and enforces key business rules such as dataset uniqueness and referential integrity. This project focuses on metadata only, not actual data storage.

---

## Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: SQLite
- **Testing**: Pytest
- **Server**: Uvicorn

---

## Data Model
**Relationship**: **Dataset (1) ─────── (N) DataElement** *(One to many relationship)*  
- One dataset can have multiple data elements.  
- Each data element belongs to exactly one dataset.

### Dataset Table (datasets)
| Column      | Type      | Description                                      |
|-------------|-----------|--------------------------------------------------|
| **id**      | Integer   | Primary Key (auto-increment)                     |
| **name**    | String    | Unique dataset name                              |
| **description** | String | Dataset description                             |
| **created_at** | DateTime | Auto-generated timestamp                       |

### DataElement Table (data_elements)
| Column      | Type      | Description                                      |
|-------------|-----------|--------------------------------------------------|
| **id**      | Integer   | Primary Key                                      |
| **dataset_id** | Integer | Foreign Key → datasets.id                       |
| **name**    | String    | Column name                                      |
| **data_type** | String   | Data type (string, int, etc.)                   |
| **nullable** | Boolean   | Whether column allows NULL                      |
| **created_at** | DateTime | Auto-generated timestamp                       |

---

## Key Design Decisions
### 1. Metadata-Only Design
The application stores metadata, not actual data. This aligns with real-world data catalog and data governance systems.

### 2. RESTful API Design
- **GET** → Read metadata  
- **POST** → Create metadata
- **UPDATE** -> Update metadata
- **DELETE** → Remove metadata  

### 3. ORM + Pydantic Separation
- SQLAlchemy handles persistence.  
- Pydantic handles request/response validation.  
- This prevents leaking database internals to API users.

### 4. Relationship Handling
- SQLAlchemy relationships with cascade delete.  
- Deleting a dataset removes its data elements automatically.

---

## Business Rules Enforced
- Dataset name must be unique.  
- Cannot delete a dataset that does not exist.  
- Data elements must reference a valid dataset.
- Authorisation and jwt token for update and delete endpoint
- Proper HTTP errors are returned for invalid operations.

---

## API Endpoints
### Dataset APIs
| Method  | Endpoint                     | Description                           |
|---------|------------------------------|---------------------------------------|
| **GET** | /list_datasets               | List all datasets                     |
| **PUT** | /update_dataset              | update dataset                        |
| **POST**| /add_dataset                 | Create a new dataset                  |
| **DELETE** | /delete_dataset/{dataset_id} | Delete dataset by id               |

### Data Element APIs
| Method  | Endpoint                     | Description                           |
|---------|------------------------------|---------------------------------------|
| **GET** | /list_data_element           | List all data elements                |
| **POST**| /add_dataelement             | Create a data element                 |
| **GET** | /read_specific_dataset/{id}  | Data elements of a dataset            |

---

## How to Run the Application

### 1. Create Virtual Environment
```bash
python -m venv venv source venv/bin/activate # Linux / Mac venv\Scripts\activate # Windows
```
---
## 2. Install Dependency
```bash
pip install -r requirements.txt
```
---
## 3. Create a .env file
Inside the env file there should be 2 variable SECRET_KEY=your secret key and ALGORITHM='HS256'

---
## 4. TESTS
```bash
python -m pytest
```
---
## 5. Run the application
```bash
uvicorn main:app
```
---
## 6. open swaggerUI
add /docs in the given URL

 


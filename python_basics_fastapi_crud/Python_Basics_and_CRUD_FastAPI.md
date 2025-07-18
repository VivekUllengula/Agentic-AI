# Understanding Decorators, Lambdas, Generators, Dictionary, List & File Handling in Python and FastAPI CRUD

## Overview
➡️ In this guide, you'll explore core Python concepts and how to apply them in a practical way by building a CRUD API using **FastAPI**.We'll start with  foundatational Python topics such as decorators, lambda functions, generators, data structures, and file handling.Then, we'll use that knowledge to build a complete FastAPI application with CRUD operations and Pydantic models.

### This guide includes:
- Python basics(functions, decorators, lambdas, etc.)
- Data structures like dictionaries and lists
- File handling and JSON I/O
- Building a FastAPI app from scratch
- CRUD operations using an in-memory store
- Interview prep questions

## 1.1 Decorators
➡️ A decorator is function thet wraps another function to modify or enhance its behaviour without changing it's code.

### Example: A program that takes the name as an argument and prints the name of the function using a decorator
```python
#A simple decorator
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs) 
    return wrapper

@logger
def greet(name):
    print(f"Hello, {name}")
greet("Alice")
Output: Calling function: greet
        Hello, Alice
```
### 💡 Use cases include logging and authenticaton.

## 1.2 Lambda Functions
➡️ A lambda function is an anonymous, one-liner fucntion. Which doesn't have a name. A lambda function can take any number of arguments, but can only have one expression. 

### Example: A program that takes a integer as an argument and prints the square of that integer using lambdas.
```python
sqaure = lambda x: x * x
print(square(5)) #Output: 25
```
### 💡 Lambda functions are often used with map(), filter() and sorted().

### Example:
```python
nums = [1, 2, 3, 4, 5, 6]
even = list(filter(lambda x: x % 2 == 0, nums))
print(even) #Output: [2, 4, 6]
```

## 1.3 Generators
➡️ Generators allow you to iterate over data in a lazy manner using the yield keyword, it is best for saving memeory.

### Example: A program that prints the countdown using the yeild function. 
```python
def countdown(n):
    while n > 0:
    yield n 
    n -= 1

for num in countdown(5):
    print(num) #Output: 5, 4, 3, 2, 1
```

### 💡 Generators are useful for reading large files, streaming data, or infinite sequences.


## 1.4 Dictionaries and Lists
### Dictionary: 
➡️ This is a data structure available in Python, which stores the data in the form of key and value pairs.This is a mutable data structure and this doesn't allow duplicate keys.

### Example: 
```python
student = {"name": "Veerappan", 
            "age": 35
          }
print(student["name"]) #Output: Veerappan 

car = {
    "brand": "Tata",
    "model": "Nano",
    "year": 2014
}
print(car["brand"]) #Output: Ford 

```
### Lists: 
➡️ This is another data storage similat to that of a array but these can store various types of data in single list.This is mutable data type and lists allow duplicates.

### Example: 
```python
numbers = [1, 2, 3, 4, 5]
print(numbers) #Output: [1, 2, 3, 4, 5]

names = ["Ram", "Seetha", "Ravana" ]
print(names[0]) #Output: Ram 

multiple_data_types = ["abc", 34, True, 40, "male"] #A list can contain multiple types of data 

```
### 💡 We can also write operations inside of lists, which is called as List Comprehension.
### Example: A program that prints the squares on numbers ranging from 0 to upto 5
```python
squares = [x * x for x in range(5)]
print(squares) #Output: [0, 1, 4, 9, 16]
```
### Nested Structures: 
```python
#A list of dictionaries 
students = [{"name": "Alice"},{"name": "Bob"} ]
names = [s["name"] for s in students]
print(names) #Output: ['Alice', 'Bob']

#A list inside of a dictionary
car = {
  "brand": "Tata",
  "model": "Curvv",
  "electric": True,
  "year": 2025,
  "colors": ["red", "white", "blue"]
}
```

## 1.5 File Handling
➡️ In python we have inbuilt file handling functionality, we can operate on files usin the 'with' opeartion and 'open'
keyword. We have different operations we can perform on files like read, write, etc.

### Example:
### 1.Writing to a text file:
```python
with open("example.txt", "w") as f: #Here 'w' indicates that we ar opening a file with 'write' permission only.
    f.write("Hello!")
```
### 2.Reading from a text file:
```python
with open("example.txt", "r") as f: #Here 'r' indicates that we ar opening a file with 'read' permission only.
    print(f.read())
```
### 3.Writing to a JSON file:
```python
def write_json(data):
    with open("data.json", "w") as f: 
        json.dump(data, f, indent=4) 
```
### 4.Reading from a JSON file:
```python
def read_json():
    with open("data.json", "r") as f: 
        data = json.load(f)
```
## Important File access modes
  
**r**  -> 	        Read-only mode.	            Opens the file for reading. File must exist; otherwise, it raises an error.  
**rb** ->	        Read-only in binary mode.	Opens the file for reading binary data. File must exist; otherwise, it raises an error.  
  
**w**  ->	        Write mode.	                Opens the file for writing. Creates a new file or truncates the existing file.  
**wb** ->	        Write in binary mode.	    Opens the file for writing binary data. Creates a new file or truncates the existing file.  
  
**a**	->        Append mode.	            Opens the file for appending data. Creates a new file if it doesn't exist.  

### 💡 File Hnadling is used for logs, configuration, or persistent data storage (Eg: JSON files)
--- 

# 2. CRUD Application with FastAPI

## 2.1 What is FastAPI?
➡️ FastAPI is a high performance web framework for building APIs in Python. It supports async programming and uses 
Pydantic for data validation.

## 2.2 What are CRUD Operations?
➡️ CRUD opeartios are the HTTP methods that modifies the data.

**C** -> Create (HTTP method - **POST**)  
**R** -> Read  (HTTP method - **GET**)  
**U** -> Update (HTTP method - **PUT**)  
**D** -> Delete (HTTP method - **DELETE**)  

## 2.3 Project Structure
➡️fastapi_crud/  
->main.py  
->model.py  
->services.py  
->data.py  
->requirements.txt  

## 2.4 Setup
Install FastAPI and Uvicorn:
```bash
pip install fastapi and uvicorn
```
Run the server:
```bash
uvicorn main:app -- reload
```
## 2.5 What is Pydantic?
Pydantic is a data validation and parsing library in FastAPI. It lets you define classes with type annotations and validates incoming data to ensure it matches those types. If the input is invalid, FastAPI automatically returns a `422` error with a helpful message.

### Example:
```python 
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str = ""
```
This defines a model for input and output that ensures the `id` is always an integer, `name` is a string, etc.

### CRUD Operations with FastAPI - *`Code Explanation`* 

### `main.py` - Application Entry Point
This is the heart of your FastAPI app. It defines the API (routes) and connects each endpoint to a function from the `services.py` module.

#### What it does:
- `FastAPI()`: Initilizes the app.
- `@app.get`, `@app.post`,etc.: Define HTTP methods and their respective URLs.
- `HTTPException`: Hanles error responses clearly.

#### Example Explained:
```python 
@app.get("/items/{item_id}")
def read(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```
- `item_id: int`: Path parameter.
- Calls a service (`get_item`) to retrieve data.
- If item doesn't exist, throws a `404` with a message.

This is the **API controller layer**, keeping your app modular by passing logic to `services.py`.

### `model.py` - Data Validation with Pydantic
This file defines the **schema** for your data using Pydantic's `BaseModel`.

#### What it does:
- Ensures incoming data matches expected types.
- Validates inputs automatically.
- Is used in both request adn respnse bodies.

#### Example Explained:
```python 
class Item(BaseModel):
    id: int
    name: str
    description: str = ""
```
When a request is made to POST or PUT an item, FastAPI,
- Validates the request JSON against the model.
- Automatically converts it into an `Item`object.
- Returns a 422 error if invalid (e.g.,`name` is missing or not a string).

### `services.py` - Business Logic Layer
This is where all your data-handling logic goes. Think of it like a **mini service layer**.

#### Why separate logic into services:
- Keeps `main.py` clean.
- Makes code reusable, testable, and maintainable.

#### Example Explained:
```python 
def get_item(item_id: int):
    data = read_data()
    return data.get(str(item_id))
```
- Returns a specific ite based on the `id`.

###Another function
```python 
def update_item(item_id: int, item: Item):
    data = read_data()
    if str(item_id) not in data:
        return None
    data[str(item_id)] = item.dict()
    write_data(data)
    return item
```
- Finds the index of the item to update
- Replaces the item with the new data.
- Returns the updated item if successful, else `None`.

## In summary:

| File Name    | Role     | Key Purpose    |
| ------- | ------------ | ------- |
| `main.py` | API routes/controller | Handles HTTP requests/responses |
| `model.py` | Schema definition(Pydantic) | Validates and parses request/response data |
| `services.py` | Business logic layer | Implements core logic like CRUD operations |

##### Each files plays a specific role in making your FastAPI app clean, scalable, and professional.

### ✅ Conclusion:
This guide introduced key Python concepts including decorators, lambda functions, generators, data structures and file handling. You have also learned how to build simple CRUD API using FastAPI.

## Interview questions

1. What is a decorator in Python and how is it used?  
2. Can you write a simple example of a Python decorator?  
3. What are lambda functions in Python? How are they different from regular functions?  
4. Give an example where a lambda function is used with **filter()**.  
5. What are generators in Python? How do they differ from regular functions?  
6. What is the use of the **yield** keyword?  
7. What are the advantages of using generators?  
8. What is the difference betweena list and a dictionary in Pyhton?  
9. Can you explain list comprehension with an example?  
10. How do you read and write files in Python?  
11. What are different file access modes in Python?  
12. How do you handle file not found errors in Python?  
13. What is FastAPI and why would you use it?  
14. How does FastAPI comapre to Flask?  
15. What is Pydantic used for in FastAPI?  
16. What HTTP methods are used for CRUD operations?  
17. Can you descrie the project structure of a FastAPI?  
18. How do you define a model in FastAPI using Pydantic?
19. How do you handle errors in FastAPI routes?  
20. How would you persist data in FastAPI app without using a database?  



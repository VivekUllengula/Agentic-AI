# Introduction
➡️ Python is a versatile programming language known for its ease of use and power. This article will cover the topics for python basics such as decorators, lambda functions, generators, dictionaries, lists, file handling. Then we will also build a simple CRUD application using FastAPI.


# 1.Understanding Decorators, Lambdas, Generators Dictionary, List &  File Handling in Python

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
## Important File Operations
  
**r**  -> 	        Read-only mode.	            Opens the file for reading. File must exist; otherwise, it raises an error.  
**rb** ->	        Read-only in binary mode.	Opens the file for reading binary data. File must exist; otherwise, it raises an error.  
  
**w**  ->	        Write mode.	                Opens the file for writing. Creates a new file or truncates the existing file.  
**wb** ->	        Write in binary mode.	    Opens the file for writing binary data. Creates a new file or truncates the existing file.  
  
**a**	->        Append mode.	            Opens the file for appending data. Creates a new file if it doesn't exist.  
**----------------------------------------------------------------------------------------------------------------------------------**  


### 💡 File Hnadling is used for logs, configuration, or persistent data storage (Eg: JSON files)

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
### ➡️ Please go through the attached project to get a clear understanding of FastAPI and CRUD operations

### ✅ Conclusion:
This guide introduced key Python concepts including decorators, lambda functions, generators, data structures and file handling. You have also learned how to build simple CRUD API using FastAPI.




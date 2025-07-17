# Introduction
➡️ Python is a versatile programming language known for its ease of use and power. This article will cover the topics for python basics such as decorators, lambda functions, generators, dictionaries, lists, file handling. Then we will also build a simple CRUD application using FastAPI.


# 1.Python Concepts

## 1.1 Decorators
➡️ A decorator is function thet wraps another function to modify or enhance its behaviour without changing it's code.

### Example:
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
➡️ A lambda function is an anonymous, one-liner fucntion. Which doesn't have a name. This is similar to that of
anonymous arrow functions in JavaScript.

### Example:
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

### Example:
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
➡️ This is a data structure available in Python, which stores the data in the form of key and value pairs, 
similar to a HashMap in Java.This is a mutable.

### Example: 
```python
student = {"name": "Alice", 
            "age": 22
          }
print(student["name"]) #Output: Alice 
```
### Lists: 
➡️ This is another data storage similat to that of a array in Java, bu unlike java lists in python can store various types of data in single list.This is mutable.

### Example: 
```python
numbers = [1, 2, 3, 4, 5]
print(numbers) #Output [1, 2, 3, 4, 5]
```
### 💡 We can also write operations inside of lists, which is called as List Comprehension.
```python
squares = [x * x for x in range(5)]
print(squares) #Output: [0, 1, 4, 9, 16]
```
### Nested Structures: 
```python
students = [{"name": "Alice"},{"name": "Bob"} ]
names = [s["name"] for s in students]
print(names) #Output: ['Alice', 'Bob']
```

## 1.5 File Handling
➡️ In python we have inbuilt file handling functionality, we can operate on files usin the 'with' opeartion and 'open'
keyword. We have different operations we can perform on files like read, write, etc.

### Example:
### 1.Writing to a file:
```python
with open("example.txt", "w") as f: #Here 'w' indicates that we ar opening a file with 'write' permission only.
    f.write("Hello!")
```
### 2.Reading from a file:
```python
with open("example.txt", "r") as f: #Here 'r' indicates that we ar opening a file with 'read' permission only.
    print(f.read())
```
### 💡 File Hnadling is used for logs, configuration, or persistent data storage (Eg: JSON files)

# 2. CRUD Application with FastAPI

## 2.1 What is FastAPI?
➡️ FastAPI is a high performance web framework for building APIs in Python. It supports async programming and uses 
Pydantic for data validation.

## 2.2 Project Structure
➡️fastapi_crud/  
->main.py  
->model.py  
->services.py  
->data.py  
->requirements.txt  

## 2.3 Setup
Install FastAPI and Uvicorn:
```bash
pip install fastapi and uvicorn
```
Run the server:
```bash
uvicorn main:app -- reload
```
### ✅ Conclusion:
This guide introduced key Python concepts including decorators, lambda functions, generators, data structures and file handling. You have also learned how to build simple CRUD API using FastAPI.




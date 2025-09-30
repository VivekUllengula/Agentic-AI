"""
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin12345@zp.lca6he2.mongodb.net/")

db = client["users-collection"]

users = db["users"]

def find_users(username: str):

    user = users.find_one({"username": username})
    user["_id"] = str(user["_id"])
    return user

print(find_users("zennialpro@gmail.com"))

from datetime import datetime, timezone

def just_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Function - {func.__name__} started running now at {datetime.now(timezone.utc)}")
        result = func(*args, **kwargs)
        print(f"Function - {func.__name__} finished running now at {datetime.now(timezone.utc)}")
        return result
    return wrapper

@just_decorator
def name(n: str):
    print(f"My name is {n}")
name("Baji")



def squares(n):
    for i in range(n):
        yield i ** 2

print (list(squares(100000)))


squares = [i ** 2 for i in range(100000)]
print(squares)


import numpy as np

arr = np.array([2,4,6])
print(arr)

b = 10
print(arr + b)

arr2 = np.array([[2,4,6], [2,4,6]])

print(arr2.T)


""
import pandas as pd

data = {
    "name": ["Manish", "Baji", "Siva"],
    "age": [32, 22, 27],
    "salary": [44000, 15000, 15000]
}

df = pd.DataFrame(data)

print(df)

print(df["age"].mean())

print(df[df["name"] == "Baji"]["salary"])

print(df.groupby("age")["salary"].mean())

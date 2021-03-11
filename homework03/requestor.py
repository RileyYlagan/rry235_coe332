import requests

response1 = requests.get(url="http://localhost:5039/animals")

print(response1.status_code)
print(response1.json())
print(response1.headers)

#remove the quotations for sections you want to run

"""
response2 = requests.get(url="http://localhost:5039/animals/head/bull")

print(response2.status_code)
print(response2.json())
print(response2.headers)

"""

"""
response3 = requests.get(url="http://localhost:5039/animals/legs/6")

print(response3.status_code)
print(response3.json())
print(response3.headers)
"""


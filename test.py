import requests

url = "https://bigserver688user.alwaysdata.net/anime/animes/1/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcwODc4MjI0LCJpYXQiOjE3NzA4NzczMjQsImp0aSI6IjdiYmJhYjIyYzVlYjQzYWI4YWQ3MTkxYWU0ZTgwYTExIiwidXNlcl9pZCI6IjEifQ.RYJhqf6dNEXB4Fl9vfHiMjQ7lmj-5zTwy0deM-fPAwo"

r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
print(r.status_code)
print(r.text)

# CS6200 PROJECT  by Zihao Zhang

## Instruction on running

### 1. clone

Use git clone or download the master branch to your local system.

### 2. pipenv

Use local terminal locate to the path

```
CS6200-project/insta_zzh-master/ 
```

run:
```
pipenv install
```
It will automatically install all the requirements inside **pipfile**.

### 3. elasticsearch

Download elasticsearch 7.1.0 and run the local server on your system.

### 4.dataset:

Download flickr dataset https://www.kaggle.com/hsankesara/flickr-image-dataset and put the top folder into static/

### 5. run

Make sure the elasticsearch server is running. do
```
python manage.py runserver
```
Then type ``` localhost:8000/Insta/ ``` or any urls you can find in Insta/urls.py for testing.

### 6. test account

try
```
username: test10 | password 123456
```
to get access into the project.

try

```
localhost:8000/admin | username:root ; password 123456 
```
for admin operations.

try
```
localhost:8000/Insta/init_dataset/
```
to add all pictures in dataset as post 

Notice: This process would take long. Please change parameters in views.py -> init_dataset. (try Insta/init_reset to delete all posts)

try
```
localhost:8000/Insta/search/
```
for the search engine.






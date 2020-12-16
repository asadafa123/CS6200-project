# CS6200 PROJECT  by Zihao Zhang

## Instruction on running

### 1. clone

Use git clone or download the master branch to your local system.

### 2. pipenv

Use local terminal locate to the path
'''
CS6200-project/insta_zzh-master/ 
'''
run:
'''
<p>pipenv install</p>
'''
It will automatically install all the requirements inside **pipfile**.

### 3. elasticsearch

Download elasticsearch 7.1.0 and run the local server on your system.

### 4.dataset:

Download flickr dataset https://www.kaggle.com/hsankesara/flickr-image-dataset and put the top folder into static/

### 5. run

Make sure the elasticsearch server is running. do
'''
<p>python manage.py runserver</p>
'''
Then type <p> localhost:8000/Insta/ </p> or any urls you can find in Insta/urls.py for testing.

### 6. test account

try
'''
<p>username: test10 | password 123456</p>
'''
to get access into the project.

try
'''
<p>localhost:8000/Insta/init_dataset/</p>
'''
to add all pictures in dataset as post 

try
'''
<p>localhost:8000/Insta/search/</p>
'''
for the search engine.






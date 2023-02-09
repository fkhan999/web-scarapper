
# Youtube-searchapi

This is django project which will scrap music videos details asynchronous every hour from youtube using selenium to avoid api limit of google


## Run Locally

Clone the project

```bash
git clone https://link-to-project
```

Go to the project directory

```
cd Youtube-API
```
Create Virtual env
```
python -m venv .venv
```
Activate virtual environment

Install dependencies
```
pip install -r requrements.txt

```
makemigrations and migrate
```
python manage.py makemigrations
python manage.py migrate
```
Start the server

```
python manage.py runserver
```


## API Reference

#### Create a new user

```http
  POST /api/createUser/
```


### Request JWT token
```
POST /api/token/
```
### Request JWT access token
```
POST /api/token/refresh/
```





## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)


## Authors

- [@fkhan999](https://www.github.com/fkhan999)


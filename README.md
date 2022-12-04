
![img.png](img.png)

## Introduction
**This is a Crawler written in pure python.**

It can Crawl all categories and link of the all article in the specific category

Also it can crawl all article in Zoomit.ir Website with these details:
- Title
- Body
- Author
- Posted DateTime


##Installation instructions:

### Create your virtual environment:
```
python3 -m venv venv
```

### Install pip packages:
```
pip install -r requirements.txt
```

### Create a MySQL Database:

```
CREATE DATABASE dbname;
```

### Grant all permissions to the database:

```
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;
```

### Add your local config to ```config.py```:
```bash
SQL_USERNAME = ""
SQL_PASSWORD = ""
SQL_HOST = ""
SQL_PORT = 0
```

## Run the Crawler:

### To see all the categories
```
python start.py show_categories
```

### To start crawling:
```
python start.py crawl CATEGORY_NAME
```

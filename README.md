# Bit68 Task

## installation

### install dependencies
```bash
pip install -r requirements.txt
```
### spinning up database
```bash
docker-compose up
```
### create postgres database
```bash
docker-compose exec -i db psql -U admin
```
```bash
CREATE DATABASE postgres
```

### migrate database & running testserver
```bash
python manage.py migrate
python manage.py runserver
```

## run test 
```bash
pytest
```

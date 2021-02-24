#!/bin/bash


python manage.py loaddata common/fixtures/news.json 

python manage.py loaddata quiz/fixtures/exam_types.json 
python manage.py loaddata quiz/fixtures/category.json
python manage.py loaddata quiz/fixtures/questions.json


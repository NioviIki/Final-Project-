# Final-Project-
```bash
 cd warehouse/
 ./manage.py runserver 8001
 ```

```bash
 cd eshop/
 ./manage.py runserver 8000
 ```

```bash
cd eshop/
 celery -A core.celery worker --loglevel=INFO
```

```bash
cd eshop/
celery -A core.celery beat -l INFO
```
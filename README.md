# AutarizationApi

## install requirements
```commandline
pip install -r requirements

```

## start project
```commandline
python main.py

```

## Api requests

```commandline
http://127.0.0.1:5000
```
### login body

```json lines
{"username": "your_username", "password": "ypur_password"}
```

### register body
```json lines
{"username": "your_username", "password": "ypur_password"}
```

### save body
```json lines
{
    "task_name": "My Task 1",
    "status": "Pending",
    "config": {
        "test": "Українська"
    },
    "selectors": ["selector1", "selector2"]
}
```
# Математический калькулятор на Flet

## Локальный запуск

```bash
pip install -r requirements.txt
flet run --web main.py
```

## Публикация на Render

Build Command:
```bash
pip install -r requirements.txt
```

Start Command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

# Shouty

Minimal and pythonic wrapper to libshout2.


## Examples

```python
import shouty

params = {
    'host': 'localhost',
    'port': 8000,
    'user': 'source',
    'password': 'hackme',
    'format': shouty.Format.MP3,
    'mount': '/shouty'
}

with shouty.connect(**params) as connection:
    connection.send_file('file.mp3')
```

To send a file manually:

```python
with shouty.connect(**params) as connection:
    with open('file.mp3', 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break

            connection.send(chunk)
            connection.sync()
```

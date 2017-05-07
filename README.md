# Shouty

Minimal and pythonic wrapper to libshout2.


## Example

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

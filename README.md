# Shouty

Minimal and pythonic wrapper to libshout2.


## Example

```python
import shouty

params = {
    'user': 'source',
    'password': 'hackme',
    'format': shouty.Format.MP3,
    'mount': '/shouty'
}

with shouty.connect('localhost', 8000, **params) as connection:
    connection.send_file('file.mp3')
```

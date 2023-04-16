# dotenv

Loads environment variables from `.env` file. Inspired by [dotenv](https://github.com/motdotla/dotenv).

## Example

```text
# .env
API_KEY=1234567890
```

From Python:

```python
# myscript.py
import os

from dotenv import config

config()

print(os.environ['API_KEY'])  # 1234567890
```

From the command line:

```bash
dotenv python myscript.py  # 1234567890
```

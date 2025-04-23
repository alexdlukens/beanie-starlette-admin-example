# Beanie Starlette Admin Example

## Setup

* This project uses poetry for dependency management. First install poetry
```bash
# optionally setup poetry to put virtualenvs in the project dir
poetry config virtualenvs.in-project true

# install project dependencies
poetry install
```


```bash
# first setup MONGO_URI to point to your MongoDB instance
export MONGO_URI="mongodb://localhost:27017"

# then run the script
scripts/run.sh
```

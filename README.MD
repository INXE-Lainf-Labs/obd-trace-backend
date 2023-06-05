[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

FastAPI starter

# Requirements

- Python (3.10.\*) [Installation](https://www.python.org/downloads/ "Installation")
- docker-compose [Installation](https://docs.docker.com/compose/install/ "Installation")
- Docker [Installation](https://docs.docker.com/desktop/mac/install/ "Installation")

## How to run

1. Clone this repository on a folder of your preference
2. Rename the file located in `src/config/example.env` to `src/config/.env`
3. On a terminal, go to the root project folder and execute `make docker-up`

The application will be available at  [http://localhost:8000/](http://localhost:8000/)

## Tests and lint

First, start the containers:
```bash
$ make docker-up
```

Test the application:
```bash
make test
```

Show lint errors:
```bash
make lint
```

Try to fix lint errors:
```bash
make lint-fix
```

## Install Black code formatter to your environment

```bash
$ make install-code-formatter
```

## Documentation

By default, fast API automatically documents all our routes and models at [http://localhost:8000/docs](http://localhost:8000/docs).

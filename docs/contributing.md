---
hide:
  - navigation
---
# Contributing

## Contributing guide

* [Fork the project](https://github.com/AgileTestApp/agiletest-cli/fork)
* Make changes
* Test your changes via local Python & via Docker
* Create PR to `main`

## Development setup

* Python with minimum version in `requires-python` key of `pyproject.toml`. Refer `Dockerfile` to know which version is used officially.
* [Activate your virtual environment](https://docs.python.org/3/library/venv.html)
* `pip install '.[dev]'` or `make install-dev`

### Build & test Docker image

To build for local testing:

```shell
docker build --rm -t ghcr.io/agiletestapp/agiletest-cli .
```

Test your build.

### Bump version

To bump the version of the project to `1.0.1`: `tbump 1.0.1`

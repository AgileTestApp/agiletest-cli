---
hide:
  - navigation
---

# AgileTest CLI

AgileTest CLI is a command line interface for [AgileTest](https://agiletest.app) - a test case management tool for agile teams.

For other documentations, visit [AgileTest Documentation](https://docs.devsamurai.com/agiletest).

## Quick Start

AgileTest CLI is available as:

* [Docker Image](https://github.com/AgileTestApp/agiletest-cli/pkgs/container/agiletest-cli) `ghcr.io/agiletestapp/agiletest-cli:latest`
* Python Package (coming soon). For now you can [install from source](#install-from-source).

For full CLI documentation, visit [AgileTest CLI Documentation](cli.md).

### CI/CD Integration

See [CI/CD Integration](ci-cd.md) for examples of how to integrate AgileTest CLI with popular CI/CD tools.

### Authentication

To use the CLI, you need to [generate a pair of client ID and client secret from AgileTest](https://docs.devsamurai.com/agiletest/access-api-documentation).

You can pass the client ID and client secret as command line arguments:

```shell
agiletest --client-id your_client_id --client-secret your_client_secret [COMMANDS]
```

Or set them as environment variables:

```shell
export AGILETEST_CLIENT_ID=your_client_id
export AGILETEST_CLIENT_SECRET=your_client_secret
```

### Import Test Execution Results

Example: Import test execution results from a JUnit XML file `tests/junit-test-data.xml`
to a Test Execution issue in AgileTest.

```shell
# with python CLI
agiletest --client-id your_client_id --client-secret your_client_secret \
    test-execution import \
    --framework-type junit --project-key TC \
    --test-execution-key TC-202 tests/junit-test-data.xml

# or with docker
docker run --rm -i \
    -e AGILETEST_CLIENT_ID=your_client_id \
    -e AGILETEST_CLIENT_SECRET=your_client_secret \
    ghcr.io/agiletestapp/agiletest-cli \
    test-execution import \
    --framework-type junit --project-key TC \
    --test-execution-key TC-202 <tests/junit-test-data.xml
```

## Install from source

The CLI requires Python 3.10 or later.

```shell
# Clone the repo
git clone https://github.com/AgileTestApp/agiletest-cli.git

cd agiletest-cli

# Install the package
pip install .
```

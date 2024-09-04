import logging
import sys

import click
from cli_commands import test_execution
from config import (
    AGILETEST_BASE_URL,
    AGILETEST_CLIENT_ID,
    AGILETEST_CLIENT_SECRET,
    DEBUG_LOG_FORMAT,
    DEFAULT_TIMEOUT,
    LOG_FORMAT,
    LOG_LEVEL,
    TRACEBACK_LIMIT,
)

sys.tracebacklimit = TRACEBACK_LIMIT

is_debug_mode = LOG_LEVEL.upper() == "DEBUG"
logging.basicConfig(
    level=LOG_LEVEL,
    format=DEBUG_LOG_FORMAT if is_debug_mode else LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
if not is_debug_mode:
    logging.getLogger("httpx").setLevel(logging.WARNING)


@click.group()
@click.option("--client-id", help="Agiletest client id", default="")
@click.option("--client-secret", help="Agiletest client secret", default="")
@click.option("--base-url", help="Agiletest base url", default="")
@click.option("--timeout", help="Agiletest request timeout", default=DEFAULT_TIMEOUT)
@click.pass_context
def cli(
    ctx: click.Context,
    client_id: str,
    client_secret: str,
    base_url: str,
    timeout: int,
):
    """AgileTest.app CLI tool. See https://AgileTestApp.github.io/agiletest-cli for documentation."""
    if not client_id:
        client_id = AGILETEST_CLIENT_ID
    if not client_secret:
        client_secret = AGILETEST_CLIENT_SECRET
    if not base_url:
        base_url = AGILETEST_BASE_URL
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj["AGILETEST_CLIENT_ID"] = client_id
    ctx.obj["AGILETEST_CLIENT_SECRET"] = client_secret
    ctx.obj["AGILETEST_BASE_URL"] = base_url
    ctx.obj["TIMEOUT"] = timeout
    ctx.obj["LOGGER"] = logging.getLogger(__name__)


cli.add_command(test_execution)


if __name__ == "__main__":
    cli()

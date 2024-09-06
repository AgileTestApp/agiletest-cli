import logging
import sys

import click
from agiletest_client import AgiletestHelper
from cli_commands import test_execution
from config import (
    AGILETEST_AUTH_BASE_URL,
    AGILETEST_BASE_URL,
    AGILETEST_CLIENT_ID,
    AGILETEST_CLIENT_SECRET,
    DEBUG_LOG_FORMAT,
    DEFAULT_TIMEOUT,
    LOG_FORMAT,
    LOG_LEVEL,
    TRACEBACK_LIMIT,
)
from utils import ClickContextConst

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
@click.option("--client-id", help="Agiletest client id", default=AGILETEST_CLIENT_ID)
@click.option(
    "--client-secret", help="Agiletest client secret", default=AGILETEST_CLIENT_SECRET
)
@click.option("--base-url", help="Agiletest base url", default=AGILETEST_BASE_URL)
@click.option(
    "--base-auth-url",
    help="Agiletest base authentication url",
    default=AGILETEST_AUTH_BASE_URL,
)
@click.option("--timeout", help="Agiletest request timeout", default=DEFAULT_TIMEOUT)
@click.pass_context
def cli(
    ctx: click.Context,
    client_id: str,
    client_secret: str,
    base_url: str,
    base_auth_url: str,
    timeout: int,
):
    """AgileTest.app CLI tool. See https://AgileTestApp.github.io/agiletest-cli for documentation."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj[ClickContextConst.AGILETEST_HELPER] = AgiletestHelper(
        client_id=client_id,
        client_secret=client_secret,
        base_url=base_url,
        base_auth_url=base_auth_url,
        timeout=timeout,
    )
    ctx.obj[ClickContextConst.LOGGER] = logging.getLogger(__name__)


cli.add_command(test_execution)


if __name__ == "__main__":
    cli()

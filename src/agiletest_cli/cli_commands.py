import sys
import typing

import click
from agiletest_client import AgiletestHelper
from config import TEST_EXECUTION_TYPES
from utils import get_logger_from_click_ctx


@click.group("test-execution")
@click.pass_context
def test_execution(ctx: click.Context):
    """Test Execution commands."""
    pass


@test_execution.command("import")
@click.option(
    "-t",
    "--framework-type",
    required=True,
    type=click.Choice(TEST_EXECUTION_TYPES),
)
@click.option("-p", "--project-key", type=click.STRING, required=True)
@click.option(
    "-te",
    "--test-execution-key",
    type=click.STRING,
    required=False,
    default="",
)
@click.argument("input_file", type=click.File(mode="r"), default=sys.stdin)
@click.pass_context
def import_test_execution(
    ctx: click.Context,
    framework_type: str,
    project_key: str,
    test_execution_key: str,
    input_file: typing.TextIO,
):
    """Import a test execution result."""
    logger = get_logger_from_click_ctx(ctx)
    msg = f"Importing test execution for '{framework_type}' framework to project '{project_key}'"
    if test_execution_key:
        msg += f" - Test Execution '{test_execution_key}'"
    logger.info(msg)

    input_text = input_file.read()
    helper = AgiletestHelper(
        client_id=ctx.obj["AGILETEST_CLIENT_ID"],
        client_secret=ctx.obj["AGILETEST_CLIENT_SECRET"],
        base_url=ctx.obj["AGILETEST_BASE_URL"],
        timeout=ctx.obj["TIMEOUT"],
    )
    result = helper.upload_test_execution_text_xml(
        framework_type=framework_type,
        project_key=project_key,
        data_xml=input_text,
        test_execution_key=test_execution_key,
    )
    if not result:
        logger.error("Failed to import test execution")
        ctx.exit(1)
    logger.info("Successfully imported Test Execution result!")

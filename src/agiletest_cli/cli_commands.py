import sys
import typing

import click
import utils
from config import TEST_EXECUTION_TYPES


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
    logger = utils.get_logger_from_click_ctx(ctx)
    msg = f"Importing test execution for '{framework_type}' framework to project '{project_key}'"
    if test_execution_key:
        msg += f" - Test Execution '{test_execution_key}'"
    logger.info(msg)

    input_text = input_file.read()
    helper = utils.get_agiletest_helper_from_click_ctx(ctx)
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


@test_execution.command("import-multipart")
@click.option(
    "-t", "--framework-type", required=True, type=click.Choice(TEST_EXECUTION_TYPES)
)
@click.option(
    "-i", "--test-info", type=click.File(mode="r"), default=sys.stdin, required=True
)
@click.argument("test_result", type=click.File(mode="r"), default=sys.stdin)
@click.pass_context
def import_test_execution_multipart(
    ctx: click.Context,
    framework_type: str,
    test_info: typing.TextIO,
    test_result: typing.TextIO,
):
    """Import a test execution result in multipart format."""
    logger = utils.get_logger_from_click_ctx(ctx)
    logger.info(
        f"Importing test execution for '{framework_type}' framework in multipart"
    )

    test_result_text = test_result.read()
    test_info_text = test_info.read()
    helper = utils.get_agiletest_helper_from_click_ctx(ctx)
    result = helper.upload_test_execution_multipart(
        framework_type=framework_type,
        test_results=test_result_text,
        test_execution_info=test_info_text,
    )
    if not result:
        logger.error("Failed to import test execution multipart")
        ctx.exit(1)
    logger.info("Successfully imported Test Execution result!")

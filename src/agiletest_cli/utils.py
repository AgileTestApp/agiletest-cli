import logging

import click

from agiletest_cli.agiletest_client import AgiletestHelper


class ClickContextConst:
    LOGGER = "LOGGER"
    AGILETEST_HELPER = "AGILETEST_HELPER"


def get_logger_from_click_ctx(ctx: click.Context) -> logging.Logger:
    return ctx.obj[ClickContextConst.LOGGER]


def get_agiletest_helper_from_click_ctx(ctx: click.Context) -> AgiletestHelper:
    return ctx.obj[ClickContextConst.AGILETEST_HELPER]

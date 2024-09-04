import logging

import click


def get_logger_from_click_ctx(ctx: click.Context) -> logging.Logger:
    return ctx.obj["LOGGER"]

import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.agiletest.app"
DEFAULT_AUTH_BASE_URL = "https://jira.agiletest.app"

TEST_EXECUTION_TYPES = [
    "junit",
    "nunit",
    "testng",
    "cucumber",
    "behave",
    "xunit",
    "robot",
]

AGILETEST_CLIENT_ID = os.getenv("AGILETEST_CLIENT_ID", "")
AGILETEST_CLIENT_SECRET = os.getenv("AGILETEST_CLIENT_SECRET", "")
AGILETEST_BASE_URL = os.getenv("AGILETEST_BASE_URL", DEFAULT_BASE_URL).strip("/")
AGILETEST_AUTH_BASE_URL = os.getenv(
    "AGILETEST_AUTH_BASE_URL", DEFAULT_AUTH_BASE_URL
).strip("/")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DEBUG_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s - %(message)s"
TRACEBACK_LIMIT = 5
DEFAULT_TIMEOUT = 30

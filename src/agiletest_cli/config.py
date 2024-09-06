import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.agiletest.app"
DEFAULT_AUTH_BASE_URL = "https://jira.agiletest.app"

FRAMEWORK_RESULT_FILETYPE_MAPPING = {
    "junit": "xml",
    "nunit": "xml",
    "testng": "xml",
    "xunit": "xml",
    "robot": "xml",
    "cucumber": "json",
    "behave": "json",
}
TEST_EXECUTION_TYPES = list(FRAMEWORK_RESULT_FILETYPE_MAPPING.keys())
MIME_TYPE_MAPPING = {
    "xml": "application/xml",
    "json": "application/json",
}

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

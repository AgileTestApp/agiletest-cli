import json
import logging
import os
import time
from typing import Generator

import httpx
import jwt
from config import (
    AGILETEST_AUTH_BASE_URL,
    AGILETEST_BASE_URL,
    DEFAULT_TIMEOUT,
    TEST_EXECUTION_TYPES,
)
from httpx import Request, Response

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.INFO)


class AgiletestAuth(httpx.Auth):
    requires_response_body = True

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        auth_base_url: str = AGILETEST_AUTH_BASE_URL,
    ):
        self.logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = auth_base_url
        self.token = ""

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and Client Secret are required")

    def _check_valid_token(self) -> bool:
        if not self.token:
            return False
        try:
            claims = jwt.decode(self.token, verify=False)
        except jwt.DecodeError:
            return False
        expiration_timestamp = claims.get("exp", 0)
        return expiration_timestamp > int(time.time())

    def build_refresh_request(self) -> Request:
        self.logger.debug(f"Building refresh request for client id {self.client_id}")
        return httpx.Request(
            method="POST",
            url=f"{self.base_url}/api/apikeys/authenticate",
            json={"clientId": self.client_id, "clientSecret": self.client_secret},
        )

    def update_token(self, response: Response) -> None:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            self.logger.error(
                f"Failed to refresh token: {response.status_code} - {response.text}"
            )
            raise err
        self.logger.debug(f"New token: {response.text}")
        self.token = str(response.text).strip()

    def auth_flow(self, request: httpx.Request) -> Generator[Request, Response, None]:
        if not self._check_valid_token():
            self.logger.debug("Refreshing token")
            refresh_res = yield self.build_refresh_request()
            self.update_token(refresh_res)

        request.headers["Authorization"] = f"JWT {self.token}"
        response = yield request

        if response.status_code == 401:
            refresh_res = yield self.build_refresh_request()
            self.update_token(refresh_res)
            request.headers["Authorization"] = f"JWT {self.token}"
            yield request


class AgiletestHelper:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = AGILETEST_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(LOG_LEVEL)
        self.base_url = base_url
        self.timeout = timeout
        self.auth = AgiletestAuth(
            client_id=client_id,
            client_secret=client_secret,
        )
        self.client = self._get_client()

    def _get_client(self) -> httpx.Client:
        return httpx.Client(
            auth=self.auth, base_url=self.base_url, timeout=self.timeout
        )

    def _check_response(self, response: Response, json_check: bool = True) -> bool:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            self.logger.error(
                f"Request Error: {err} - {response.status_code} - {response.text}"
            )
            return False
        if json_check:
            try:
                response.json()
            except json.decoder.JSONDecodeError as err:
                self.logger.error(
                    f"Response invalid JSON response: {err} - {response.text}"
                )
                return False
        return True

    def upload_test_execution_text_xml(
        self,
        framework_type: str,
        project_key: str,
        data_xml: str,
        test_execution_key: str = "",
    ) -> bool | dict:
        """Upload test execution to Agiletest.

        Args:
            framework_type (str): framework type
            project_key (str): project key
            data_xml (str): test execution data in xml format
            test_execution_key (str, optional): test execution jira issue key to import to. Defaults to "".

        Raises:
            ValueError: framework type not supported

        Returns:
            bool | dict: false if failed, dict with response if success
        """
        framework_type = framework_type.lower()
        if framework_type not in TEST_EXECUTION_TYPES:
            raise ValueError(
                f"Invalid test execution type: {framework_type}. Supported frameworks: {TEST_EXECUTION_TYPES}"
            )
        params = {"projectKey": project_key}
        if test_execution_key:
            params["testExecutionKey"] = test_execution_key

        headers = {"Content-Type": "text/xml"}
        res = self.client.post(
            f"/ds/test-executions/{framework_type}",
            params=params,
            headers=headers,
            content=data_xml,
        )
        result = self._check_response(res)
        if not result:
            return result
        self.logger.info(f"Test execution uploaded successfully: '{res.text}'")
        res_json: dict = res.json()
        test_execution_key = res_json.get("key", "")
        test_execution_url = res_json.get("url", "")
        missed_cases = res_json.get("missedCases", [])
        if missed_cases:
            self.logger.warning(
                f"Test execution {test_execution_key} with missed test cases: {missed_cases}"
            )
        self.logger.info(
            f"Test Execution issue updated: {test_execution_key} {test_execution_url}"
        )
        return res_json

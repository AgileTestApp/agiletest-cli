# CI CD Integration

## GitHub Actions

Test & import test execution to AgileTest with GitHub Actions.

A working sample repo is available at [AgileTestApp/sample-automation-test-import](https://github.com/AgileTestApp/sample-automation-test-import). See [test-and-upload-report.yml](https://github.com/AgileTestApp/sample-automation-test-import/blob/main/.github/workflows/test-and-upload-report.yml) for a sample GitHub Actions workflow that runs tests and uploads test results to AgileTest.

```yaml
# Sample step to upload Robot Framework test results to AgileTest
# Assuming you have a Robot Framework test suite that generates a report file to `./reports/robot-report.xml`
      - name: Upload report to AgileTest.App
        env:
          AGILETEST_CLIENT_ID: ${{ secrets.AGILETEST_CLIENT_ID }}
          AGILETEST_CLIENT_SECRET: ${{ secrets.AGILETEST_CLIENT_SECRET }}
        run: |
          docker run --rm \
          -e AGILETEST_CLIENT_ID=$AGILETEST_CLIENT_ID \
          -e AGILETEST_CLIENT_SECRET=$AGILETEST_CLIENT_SECRET \
          -v ${{ github.workspace }}/reports:/reports \
          ghcr.io/agiletestapp/agiletest-cli:latest \
          test-execution import --framework-type robot --project-key TC \
          /reports/robot-report.xml
```

## Bitbucket Pipelines

A working sample repo is available at [agiletestapp/bitbucket-sample-automation-test-import](https://bitbucket.org/agiletestapp/bitbucket-sample-automation-test-import/). See [bitbucket-pipelines.yml](https://bitbucket.org/agiletestapp/bitbucket-sample-automation-test-import/src/main/bitbucket-pipelines.yml) for a sample Bitbucket Pipelines configuration that runs tests and uploads test results to AgileTest.

```yaml
# Sample step to test & upload Behave test results to AgileTest
      - step:
          image: python
          name: Behave Test & Upload Report
          script:
            - pip install -r requirements.txt
            - behave behave/features -f json -o reports/behave-report.json
            - |
              docker run --rm \
              -e AGILETEST_CLIENT_ID=$AGILETEST_CLIENT_ID \
              -e AGILETEST_CLIENT_SECRET=$AGILETEST_CLIENT_SECRET \
              -v $BITBUCKET_CLONE_DIR/sample-automation-test-import/reports:/reports \
              ghcr.io/agiletestapp/agiletest-cli:latest \
              test-execution import --framework-type behave --project-key TC \
              /reports/behave-report.json
```

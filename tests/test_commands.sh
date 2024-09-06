# agiletest cli
agiletest test-execution import -t junit -p TC -te TC-202 tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC -te TC-202 - <tests/junit-test-data.xml

agiletest test-execution import -t junit -p TC tests/junit-test-data.xml

# import multipart
agiletest test-execution import-multipart -t junit -i tests/info.json tests/junit-test-data.xml

# invalid
agiletest --client-id invalid test-execution import -t junit -p TC tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC123 tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC -te TC-9999 tests/junit-test-data.xml

# docker
docker run --env-file .env --rm -i ghcr.io/agiletestapp/agiletest-cli test-execution import -t junit -p TC -te TC-202 - <tests/junit-test-data.xml
docker run --env-file .env --rm -i ghcr.io/agiletestapp/agiletest-cli test-execution import -t junit -p TC -te TC-202 <tests/junit-test-data.xml

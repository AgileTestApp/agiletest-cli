# agiletest cli
agiletest test-execution import -t junit -p TC -te TC-202 tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC -te TC-202 - <tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC tests/junit-test-data.xml
agiletest test-execution import -t junit -p AUT tests/junit-test-data.xml
# with options: plan-keys test-environments, fix-versions, milestone-id, revision
agiletest test-execution import -t junit -p AUT -te AUT-6794 -pk AUT-6648 --test-environments Staging -envs Develop --fix-versions test -fv range --milestone-id 5780 --revision 1234 tests/junit-test-data.xml


# import multipart
agiletest test-execution import-multipart -t junit -i tests/info.json tests/junit-test-data.xml

# invalid
agiletest --client-id invalid test-execution import -t junit -p TC tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC123 tests/junit-test-data.xml
agiletest test-execution import -t junit -p TC -te TC-9999 tests/junit-test-data.xml

# docker
docker run --env-file .env --rm -i ghcr.io/agiletestapp/agiletest-cli test-execution import -t junit -p TC -te TC-202 - <tests/junit-test-data.xml
docker run --env-file .env --rm -i ghcr.io/agiletestapp/agiletest-cli test-execution import -t junit -p TC -te TC-202 <tests/junit-test-data.xml

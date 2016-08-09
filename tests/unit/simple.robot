
*** Settings ***
| Documentation | Unit tests for my test library
| Library       | Collections
| Library       | OperatingSystem
| Resource      | ${KEYWORD_DIR}/ZWDBKeywords.robot
| Force tags    | zwdb
| Suite Setup   | Initialize suite variables

*** Test Cases ***

| Simple Log to Console
| | [Tags] | smoke
| | Initialize suite variables
| | LOG | Hello World!! | WARN

*** Keywords ***

| Initialize suite variables
| | [Documentation]    | Define some global variables used by the tests in this suite
| | ${test dir}=       | Evaluate | os.path.dirname(r"${SUITE SOURCE}") | os
| | set suite variable | ${KEYWORD DIR} | ${test dir}/keywords
| | set suite variable | ${DATA_DIR}    | ${test dir}/data
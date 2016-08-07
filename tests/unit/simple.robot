
*** Settings ***
| Documentation | Unit tests for my test library
| Library       | Collections
| Library       | OperatingSystem

*** Test Cases ***

| Simple Log to Console
| | [Tags] | smoke
| | LOG | Hello World!! | WARN

*** Settings ***
| Library | OperatingSystem

*** Test Cases ***
| Help for option -l/--library
| | [Documentation]
| | ... | Verify that the help message includes help for -i/--interface
| |
| | Start the bench with options | --help
| | Output should contain
| | ... | -l LIBRARY, --library LIBRARY
| | ... | load the given LIBRARY (eg: -l DatabaseLibrary)

*** Keywords ***
| Start the bench with options
| | [Arguments] | ${options}
| | [Documentation]
| | ... | Attempt to start the bench with the given options
| | ... |
| | ... | The stdout of the process will be in a test suite
| | ... | variable named \${output}
| |
| | ${output} | Run | python -m rfbench ${options}
| | Set test variable | ${output}

| Output should contain
| | [Arguments] | @{patterns}
| | [Documentation]
| | ... | Fail if the output from the previous command doesn't contain the given string
| | ... |
| | ... | This keyword assumes the output of the command is in
| | ... | a test suite variable named \${output}
| | ... |
| | ... | Note: the help will be automatically wrapped, so
| | ... | you can only search for relatively short strings.
| |
| | :FOR | ${pattern} | IN | @{patterns}
| | | Run keyword if | '''${pattern}''' not in '''${output}'''
| | | ... | Fail | Output did not contain '${pattern}'

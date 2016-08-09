*** Keywords ***
| Create new ZWDB instance
| | [Documentation]
| | ... | Creates and returns a new instance of the ZWDB object.
| | ... | This object will have no libraries added by default. The
| | ... | object is available in the suite variable ${ZWDB}
| | ${ZWDB}= | evaluate | rfbench.kwdb.KeywordTable() | rfbench
| | Set test variable | ${ZWDB}

| Load installed keywords into ZWDB
| | [Documentation]
| | ... | This calls a method to add all installed libraries into
| | ... | the database referenced by the suite variable ${ZWDB}
| | Call method | ${ZWDB} | add_installed_libraries

| Get keywords from ZWDB
| | [Documentation]
| | ... | This calls the get_keywords method of the kwdb object
| | ... | referenced by ${ZWDB}. It returns the data returned
| | ... | by that method.
| | ${keywords}= | Call method | ${ZWDB} | get_keywords | *
| | [Return] | ${keywords}

| Load a resource file into ZWDB
| | [Arguments] | ${name or path}
| | [Documentation]
| | ... | Loads one library by name, or resoure file by path
| | ... | to the database referenced by the suite variable ${ZWDB}
| | Call method | ${ZWDB} | add | ${name or path}
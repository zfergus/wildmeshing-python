# TriWild (https://github.com/wildmeshing/TriWild)
# License: MPL-2.0
if(TARGET triwild::triwild)
    return()
endif()

message(STATUS "Third-party: creating target 'triwild::triwild'")

include(CPM)
CPMAddPackage("gh:zfergus/TriWild#ebb8a6abd0554bac577a18ccfa5dc05802fe3db7")
# fTetWild (https://github.com/wildmeshing/fTetWild)
# License: MPL-2.0
if(TARGET ftetwild::ftetwild)
    return()
endif()

message(STATUS "Third-party: creating target 'ftetwild::ftetwild'")

include(CPM)
CPMAddPackage("gh:zfergus/fTetWild#4f854061c6e0d635d2a3711c074544c52896d8d9")
# fTetWild (https://github.com/wildmeshing/fTetWild)
# License: MPL-2.0
if(TARGET ftetwild::ftetwild)
    return()
endif()

message(STATUS "Third-party: creating target 'ftetwild::ftetwild'")

include(CPM)
CPMAddPackage("gh:zfergus/fTetWild#5f9656a7e3c62d61c0993635bde3f75d0287566f")
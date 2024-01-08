# TriWild (https://github.com/wildmeshing/TriWild)
# License: MPL-2.0
if(TARGET triwild::triwild)
    return()
endif()

message(STATUS "Third-party: creating target 'triwild::triwild'")

# Make sure the libigl predicates are enabled
set(LIBIGL_PREDICATES ON CACHE BOOL "Use exact predicates" FORCE)

include(CPM)
CPMAddPackage("gh:zfergus/TriWild#a9ffc6db5d9bf12184c3c4f2326550fe91e97e2a")
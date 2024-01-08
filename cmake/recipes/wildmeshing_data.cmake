# data (https://github.com/wildmeshing/data)
# License: MPL-2.0

if(TARGET wildmeshing::data)
    return()
endif()

include(ExternalProject)

set(WILDMESHING_DATA_DIR "${PROJECT_SOURCE_DIR}/data/" CACHE PATH "Where should polyfem download and look for test data?")

ExternalProject_Add(
    wildmeshing_data_download
    PREFIX ${FETCHCONTENT_BASE_DIR}/wildmeshing-data
    SOURCE_DIR ${WILDMESHING_DATA_DIR}
    GIT_REPOSITORY https://github.com/wildmeshing/data
    GIT_TAG 1484054abbac36e9c8340c3b32d87ad6eee45016
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    LOG_DOWNLOAD ON
)

# Create a dummy target for convenience
add_library(wildmeshing_data INTERFACE)
add_library(wildmeshing::data ALIAS wildmeshing_data)

add_dependencies(wildmeshing_data wildmeshing_data_download)

target_compile_definitions(wildmeshing_data INTERFACE  WILDMESHING_DATA_DIR=\"${WILDMESHING_DATA_DIR}\")

# Detects whether this is a top-level project
get_directory_property(HAS_PARENT PARENT_DIRECTORY)
if(HAS_PARENT)
	set(WILDMESHING_TOPLEVEL_PROJECT OFF)
else()
	set(WILDMESHING_TOPLEVEL_PROJECT ON)
endif()

# Check required CMake version
set(REQUIRED_CMAKE_VERSION "3.18.0")
if(WILDMESHING_TOPLEVEL_PROJECT)
	cmake_minimum_required(VERSION ${REQUIRED_CMAKE_VERSION})
else()
	# Don't use cmake_minimum_required here to avoid implicitly overriding parent policies
	if(${CMAKE_VERSION} VERSION_LESS ${REQUIRED_CMAKE_VERSION})
		message(FATAL_ERROR "CMake required version to build IPC Toolkit is ${REQUIRED_CMAKE_VERSION}")
	endif()
endif()

# Include user-provided default options if available. We do that before the main
# `project()` so that we can define the C/C++ compilers from the option file.
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/WildMeshingOptions.cmake)
	message(STATUS "Using local options file: ${CMAKE_CURRENT_SOURCE_DIR}/WildMeshingOptions.cmake")
	include(${CMAKE_CURRENT_SOURCE_DIR}/WildMeshingOptions.cmake)
endif()

# Enable ccache if available
find_program(CCACHE_PROGRAM ccache)
if(CCACHE_PROGRAM)
	option(WILDMESHING_WITH_CCACHE "Enable ccache when building IPC Toolkit" ${WILDMESHING_TOPLEVEL_PROJECT})
else()
	option(WILDMESHING_WITH_CCACHE "Enable ccache when building IPC Toolkit" OFF)
endif()
if(WILDMESHING_WITH_CCACHE AND CCACHE_PROGRAM)
	message(STATUS "Enabling Ccache support (${CCACHE_PROGRAM})")
	set(ccacheEnv
		CCACHE_BASEDIR=${CMAKE_BINARY_DIR}
		CCACHE_SLOPPINESS=clang_index_store,include_file_ctime,include_file_mtime,locale,pch_defines,time_macros
	)
	foreach(lang IN ITEMS C CXX)
		set(CMAKE_${lang}_COMPILER_LAUNCHER
			${CMAKE_COMMAND} -E env ${ccacheEnv} ${CCACHE_PROGRAM}
		)
	endforeach()
endif()

################################################################################
# CMake Policies
################################################################################

cmake_policy(SET CMP0054 NEW) # Only interpret if() arguments as variables or keywords when unquoted.
cmake_policy(SET CMP0076 NEW) # target_sources() command converts relative paths to absolute.
if(CMAKE_VERSION VERSION_GREATER_EQUAL "3.24")
  cmake_policy(SET CMP0135 NEW) # Set the timestamps of all extracted contents to the time of the extraction.
endif()

################################################################################

project(WildMeshing
		DESCRIPTION "Python bindings for WildMeshing"
		LANGUAGES C CXX)

# Set default minimum C++ standard
if(WILDMESHING_TOPLEVEL_PROJECT)
	set(CMAKE_CXX_STANDARD 14)
	set(CMAKE_CXX_STANDARD_REQUIRED ON)
	set(CMAKE_CXX_EXTENSIONS OFF)
endif()

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/wildmeshing/")
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/recipes/")

# General CMake utils
include(wildmeshing_cpm_cache)
include(wildmeshing_use_colors)

# Generate position independent code by default
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Sort projects inside the solution
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

################################################################################
# Bindings
################################################################################

include(pybind11)

pybind11_add_module(wildmeshing
	src/binding.cpp
	src/utils.cpp
	src/triangulate_data.cpp
	src/triangulate.cpp
	src/tetrahedralize.cpp
)

target_include_directories(wildmeshing PRIVATE src)

set_target_properties(wildmeshing PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}" SUFFIX "${PYTHON_MODULE_EXTENSION}")

################################################################################
# Dependencies
################################################################################

# triwild
include(triwild)
target_link_libraries(wildmeshing PUBLIC triwild::triwild)

# tetwild
include(ftetwild)
target_link_libraries(wildmeshing PUBLIC ftetwild::ftetwild)

#for testing purpose
include(wildmeshing_data)
target_link_libraries(wildmeshing PUBLIC wildmeshing::data)

# Extra warnings (link last for highest priority)
include(wildmeshing_warnings)
target_link_libraries(wildmeshing PRIVATE wildmeshing::warnings)

################################################################################
# Compiler options
################################################################################

# Use C++14
target_compile_features(wildmeshing PUBLIC cxx_std_14)
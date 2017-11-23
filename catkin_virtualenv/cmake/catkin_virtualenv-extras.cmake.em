@[if DEVELSPACE]@
set(@(PROJECT_NAME)_CMAKE_DIR @(CMAKE_CURRENT_SOURCE_DIR)/cmake)
@[else]@
set(catkin_virtualenv_CMAKE_DIR ${@(PROJECT_NAME)_DIR})
@[end if]@

# Include cmake modules from @(PROJECT_NAME)
include(${@(PROJECT_NAME)_CMAKE_DIR}/catkin_generate_virtualenv.cmake)
include(${@(PROJECT_NAME)_CMAKE_DIR}/catkin_install_python.cmake)

@[if DEVELSPACE]@

set(@(PROJECT_NAME)_CMAKE_DIR @(CMAKE_CURRENT_SOURCE_DIR)/cmake)
set(${PROJECT_NAME}_VENV_DIRECTORY ${CATKIN_DEVEL_PREFIX}/${CATKIN_GLOBAL_SHARE_DESTINATION}/${PROJECT_NAME}/venv)

@[else]@

set(catkin_virtualenv_CMAKE_DIR ${@(PROJECT_NAME)_DIR})
set(${PROJECT_NAME}_VENV_DIRECTORY ${CMAKE_INSTALL_PREFIX}/${CATKIN_GLOBAL_SHARE_DESTINATION}/${PROJECT_NAME}/venv)

@[end if]@

# Include cmake modules from @(PROJECT_NAME)
include(${@(PROJECT_NAME)_CMAKE_DIR}/catkin_generate_virtualenv.cmake)
include(${@(PROJECT_NAME)_CMAKE_DIR}/catkin_install_python.cmake)

# Software License Agreement (GPL)
#
# \file      catkin_generate_virtualenv.cmake
# \authors   Paul Bovbel <pbovbel@locusrobotics.com>
# \copyright Copyright (c) (2017,), Locus Robotics, All rights reserved.
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
function(catkin_generate_virtualenv)
  cmake_parse_arguments(ARG "PYTHON3" "" "" ${ARGN})

  if(${ARG_PYTHON3})
    set(build_venv_extra "--python3")
    set(PYTHON_VERSION_MAJOR 3)
  endif()

  if(NOSETESTS)
    if(${ARG_PYTHON3})
      find_program(nosetests NAMES
        "nosetests${PYTHON_VERSION_MAJOR}"
        "nosetests-${PYTHON_VERSION_MAJOR}"
        "nosetests")
    else()
      set(nosetests ${NOSETESTS})
    endif()

    set(nosetests "${${PROJECT_NAME}_VENV_DIRECTORY}/bin/python${PYTHON_VERSION_MAJOR} ${nosetests}")

    # (pbovbel): NOSETESTS originally set by catkin here:
    # <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
    message(STATUS "Using virtualenv to run Python nosetests: ${nosetests}")
    set(NOSETESTS ${nosetests} PARENT_SCOPE)
  endif()

  # Check if this package already has a virtualenv target before creating one
  if(TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(WARNING "catkin_generate_virtualenv was called twice")
    return()
  endif()

  # Collect all exported pip requirements files, from this package and all dependencies
  execute_process(
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${catkin_virtualenv_CMAKE_DIR}/glob_requirements.py --package-name ${PROJECT_NAME}
    OUTPUT_VARIABLE requirements_list
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  set(generated_requirements ${CMAKE_BINARY_DIR}/generated_requirements.txt)

  foreach(requirements_txt ${requirements_list})
     # Trigger a re-configure if any requirements file changes
    stamp(${requirements_txt})
    message(STATUS "Including ${requirements_txt} in bundled virtualenv")
  endforeach()

  # Combine requirements into one list
  add_custom_command(OUTPUT ${generated_requirements}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${catkin_virtualenv_CMAKE_DIR}/combine_requirements.py --requirements-list ${requirements_list} --output-file ${generated_requirements}
    DEPENDS ${requirements_list}
  )

  # Build a virtualenv, fixing up paths for its eventual location in ${PROJECT_NAME}_VENV_DIRECTORY
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/venv
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${catkin_virtualenv_CMAKE_DIR}/build_venv.py --requirements ${generated_requirements} --root-dir ${${PROJECT_NAME}_VENV_DIRECTORY} ${build_venv_extra}
    DEPENDS ${generated_requirements}
  )

  # Symlink virtualenv to the destination - this really only has an effect in devel-space.
  add_custom_command(OUTPUT ${${PROJECT_NAME}_VENV_DIRECTORY}
    COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_BINARY_DIR}/venv ${${PROJECT_NAME}_VENV_DIRECTORY} || true
    DEPENDS ${CMAKE_BINARY_DIR}/venv
  )

  add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
    DEPENDS ${${PROJECT_NAME}_VENV_DIRECTORY}
    SOURCES ${requirements_list}
  )

  install(DIRECTORY ${CMAKE_BINARY_DIR}/venv
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    USE_SOURCE_PERMISSIONS)

  install(FILES ${generated_requirements}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

endfunction()

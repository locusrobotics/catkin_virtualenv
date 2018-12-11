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
  set(oneValueArgs PYTHON_VERSION PYTHON_VERSION_MAJOR USE_SYSTEM_PACKAGES ISOLATE_REQUIREMENTS)
  set(multiValueArgs EXTRA_PIP_ARGS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  # Check if this package already has a virtualenv target before creating one
  if(TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(WARNING "catkin_generate_virtualenv was called twice")
    return()
  endif()

  # Backwards compatibility for PYTHON_VERSION_MAJOR, overriding PYTHON_VERSION
  if(DEFINED ARG_PYTHON_VERSION_MAJOR)
    set(ARG_PYTHON_VERSION ${ARG_PYTHON_VERSION_MAJOR})
    message(WARNING "PYTHON_VERSION_MAJOR has been deprecated, please set PYTHON_VERSION instead")
  endif()

  if(NOT DEFINED ARG_PYTHON_VERSION)
    set(ARG_PYTHON_VERSION 2)
  endif()

  if(NOT DEFINED ARG_USE_SYSTEM_PACKAGES)
    set(ARG_USE_SYSTEM_PACKAGES TRUE)
  endif()

  if(NOT DEFINED ARG_ISOLATE_REQUIREMENTS)
    set(ARG_ISOLATE_REQUIREMENTS FALSE)
  endif()

  if (NOT DEFINED ARG_EXTRA_PIP_ARGS)
    set(ARG_EXTRA_PIP_ARGS "-qq")
  endif()
  # Convert CMake list to ' '-separated list
  string(REPLACE ";" "\ " processed_pip_args "${ARG_EXTRA_PIP_ARGS}")
  # Double-escape needed to get quote down through cmake->make->shell layering
  set(processed_pip_args \\\"${processed_pip_args}\\\")

  set(venv_dir venv)

  set(venv_devel_dir ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})
  set(venv_install_dir ${CMAKE_INSTALL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})

  set(${PROJECT_NAME}_VENV_DEVEL_DIR ${venv_devel_dir} PARENT_SCOPE)
  set(${PROJECT_NAME}_VENV_INSTALL_DIR ${venv_install_dir} PARENT_SCOPE)

  if(${ARG_ISOLATE_REQUIREMENTS})
    message(STATUS "Only using requirements from this catkin package")
    set(glob_args "--no-deps")
  endif()

  # Collect all exported pip requirements files, from this package and all dependencies
  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv glob_requirements
      --package-name ${PROJECT_NAME} ${glob_args}
    OUTPUT_VARIABLE requirements_list
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  # Include common requirements that ROS makes available in system environment for py2
  list(APPEND requirements_list ${catkin_virtualenv_CMAKE_DIR}/common_requirements.txt)

  set(generated_requirements ${CMAKE_BINARY_DIR}/generated_requirements.txt)

  # Trigger a re-configure if any requirements file changes
  foreach(requirements_txt ${requirements_list})
    stamp(${requirements_txt})
    message(STATUS "Including ${requirements_txt} in bundled virtualenv")
  endforeach()

  # Combine requirements into one list
  add_custom_command(OUTPUT ${generated_requirements}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv combine_requirements
      --requirements-list ${requirements_list} --output-file ${generated_requirements}
    DEPENDS ${requirements_list}
  )

  if(${ARG_USE_SYSTEM_PACKAGES})
    message(STATUS "Using system site packages")
    set(venv_args "--use-system-packages")
  endif()

  # Generate a virtualenv, fixing up paths for devel-space
  add_custom_command(OUTPUT ${venv_devel_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv build_venv
      --root-dir ${venv_devel_dir} --requirements ${generated_requirements} --retries 3
      --python-version ${ARG_PYTHON_VERSION} ${venv_args} --extra-pip-args ${processed_pip_args}
    WORKING_DIRECTORY ${venv_devel_dir}/..
    DEPENDS ${generated_requirements}
  )

  # Generate a virtualenv, fixing up paths for install-space
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv build_venv
      --root-dir ${venv_install_dir} --requirements ${generated_requirements} --retries 3
      --python-version ${ARG_PYTHON_VERSION} ${venv_args} --extra-pip-args ${processed_pip_args}
    DEPENDS ${generated_requirements}
  )

  # Per-package virtualenv target
  add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
    DEPENDS ${CMAKE_BINARY_DIR}/${venv_dir}
    DEPENDS ${venv_devel_dir}
    SOURCES ${requirements_list}
  )

  install(DIRECTORY ${CMAKE_BINARY_DIR}/${venv_dir}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    USE_SOURCE_PERMISSIONS)

  install(FILES ${generated_requirements}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

  # (pbovbel): NOSETESTS originally set by catkin here:
  # <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
  message(STATUS "Using virtualenv to run Python nosetests: ${nosetests}")
  set(NOSETESTS "${venv_devel_dir}/bin/python -m nose" PARENT_SCOPE)

endfunction()

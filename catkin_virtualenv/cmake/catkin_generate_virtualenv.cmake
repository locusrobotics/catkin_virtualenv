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
  set(oneValueArgs PYTHON_VERSION PYTHON_INTERPRETER USE_SYSTEM_PACKAGES ISOLATE_REQUIREMENTS INPUT_REQUIREMENTS)
  set(multiValueArgs EXTRA_PIP_ARGS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  ### Handle argument defaults and deprecations

  if(DEFINED ARG_PYTHON_VERSION)
    message(WARNING "PYTHON_VERSION has been deprecated, set 'PYTHON_INTERPRETER python${ARG_PYTHON_VERSION}' instead")
    set(ARG_PYTHON_INTERPRETER "python${ARG_PYTHON_VERSION}")
  endif()

  if(NOT DEFINED ARG_PYTHON_INTERPRETER)
    set(ARG_PYTHON_INTERPRETER "python2")
  endif()

  if(NOT DEFINED ARG_USE_SYSTEM_PACKAGES OR ARG_USE_SYSTEM_PACKAGES)
    message(STATUS "Using system site packages")
    set(venv_args "${venv_args} --use-system-packages")
  endif()

  if(ARG_ISOLATE_REQUIREMENTS)
    message(STATUS "Only using requirements from this catkin package")
    set(lock_args "${lock_args} --no-deps")
  endif()

  if(NOT DEFINED ARG_INPUT_REQUIREMENTS)
    message(WARNING "Please define an INPUT_REQUIREMENTS and generate a lock file - see https://github.com/locusrobotics/catkin_virtualenv/blob/master/README.md#locking-dependencies")
  endif()

  if (NOT DEFINED ARG_EXTRA_PIP_ARGS)
    set(ARG_EXTRA_PIP_ARGS "-qq" "--retries 10" "--timeout 30")
  endif()

  # Convert CMake list to ' '-separated list
  string(REPLACE ";" "\ " processed_pip_args "${ARG_EXTRA_PIP_ARGS}")
  # Double-escape needed to get quote down through cmake->make->shell layering
  set(processed_pip_args \\\"${processed_pip_args}\\\")

  # Check if this package already has a virtualenv target before creating one
  if(TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(WARNING "catkin_generate_virtualenv was called twice")
    return()
  endif()

  ### Start building virtualenv

  set(venv_dir venv)

  set(venv_devel_dir ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})
  set(venv_install_dir ${CMAKE_INSTALL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})

  set(${PROJECT_NAME}_VENV_DEVEL_DIR ${venv_devel_dir} PARENT_SCOPE)
  set(${PROJECT_NAME}_VENV_INSTALL_DIR ${venv_install_dir} PARENT_SCOPE)

  # Collect requirements from each catkin package in the dependency chain
  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv collect_requirements
      --package-name ${PROJECT_NAME} ${lock_args}
    OUTPUT_VARIABLE requirements_list
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv collect_requirements --no-deps
      --package-name ${PROJECT_NAME} ${lock_args}
    OUTPUT_VARIABLE package_requirements
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  add_custom_command(COMMENT "Generate virtualenv in ${CMAKE_BINARY_DIR}/${venv_dir}"
    OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_init ${venv_dir}
      --python ${ARG_PYTHON_INTERPRETER} ${venv_args} --extra-pip-args ${processed_pip_args}
  )

  if(DEFINED ARG_INPUT_REQUIREMENTS AND NOT package_requirements STREQUAL "")
    add_custom_command(COMMENT "Lock input requirements if they don't exist"
      OUTPUT ${package_requirements}
      COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_lock ${venv_dir}
        --package-name ${PROJECT_NAME} --input-requirements ${CMAKE_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
        --no-overwrite --extra-pip-args ${processed_pip_args}
      DEPENDS
        ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
        ${CMAKE_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
    )
  endif()

  add_custom_command(COMMENT "Install requirements to ${CMAKE_BINARY_DIR}/${venv_dir}"
    OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}/bin/activate
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_install ${venv_dir}
      --requirements ${requirements_list} --extra-pip-args ${processed_pip_args}
    DEPENDS
      ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
      ${package_requirements}
      ${requirements_list}
  )

  add_custom_command(COMMENT "Prepare relocated virtualenvs for develspace and installspace"
    OUTPUT ${venv_devel_dir} install/${venv_dir}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} ${venv_devel_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate ${venv_devel_dir} --target-dir ${venv_devel_dir}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} install/${venv_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate install/${venv_dir} --target-dir ${venv_install_dir}
    DEPENDS ${CMAKE_BINARY_DIR}/${venv_dir}/bin/activate
  )

  add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
    COMMENT "Per-package virtualenv target"
    DEPENDS
      ${venv_devel_dir}
      install/${venv_dir}
  )

  add_custom_target(venv_lock
    COMMENT "Manually invoked target to write out ${ARG_LOCK_FILE}"
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_lock ${venv_dir}
      --package-name ${PROJECT_NAME} --input-requirements ${CMAKE_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
      --extra-pip-args ${processed_pip_args}
    DEPENDS
      ${venv_devel_dir}
      ${CMAKE_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
  )

  install(DIRECTORY ${CMAKE_BINARY_DIR}/install/${venv_dir}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    USE_SOURCE_PERMISSIONS)

  install(FILES ${ARG_LOCK_FILE}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

  # (pbovbel): NOSETESTS originally set by catkin here:
  # <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
  message(STATUS "Using virtualenv to run Python nosetests: ${nosetests}")
  set(NOSETESTS "${venv_devel_dir}/bin/python -m nose" PARENT_SCOPE)

endfunction()

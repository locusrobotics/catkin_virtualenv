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
  set(oneValueArgs PYTHON_VERSION PYTHON_INTERPRETER USE_SYSTEM_PACKAGES ISOLATE_REQUIREMENTS INPUT_REQUIREMENTS CHECK_VENV)
  set(multiValueArgs EXTRA_PIP_ARGS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  ### Handle argument defaults and deprecations

  if(DEFINED ARG_PYTHON_VERSION)
    message(WARNING "PYTHON_VERSION has been deprecated, set 'PYTHON_INTERPRETER python${ARG_PYTHON_VERSION}' instead")
    set(ARG_PYTHON_INTERPRETER "python${ARG_PYTHON_VERSION}")
  endif()

  if(NOT DEFINED ARG_PYTHON_INTERPRETER)
    set(ARG_PYTHON_INTERPRETER "python3")
  endif()

  if(NOT DEFINED ARG_USE_SYSTEM_PACKAGES OR ARG_USE_SYSTEM_PACKAGES)
    message(STATUS "Using system site packages")
    set(venv_args "--use-system-packages")
  endif()

  if(ARG_ISOLATE_REQUIREMENTS)
    message(STATUS "Only using requirements from this catkin package")
    set(lock_args "${lock_args} --no-deps")
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

  # Make sure CATKIN_* paths are initialized
  catkin_destinations()  # oh the places we'll go

  ### Start building virtualenv
  set(venv_dir venv)

  set(venv_devel_dir ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})
  set(venv_install_dir ${CMAKE_INSTALL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/${venv_dir})

  set(${PROJECT_NAME}_VENV_DEVEL_DIR ${venv_devel_dir} PARENT_SCOPE)
  set(${PROJECT_NAME}_VENV_INSTALL_DIR ${venv_install_dir} PARENT_SCOPE)

  # Store just _this_ project's requirements file in ${package_requirements}
  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv collect_requirements --no-deps
      --package-name ${PROJECT_NAME} ${lock_args}
    OUTPUT_VARIABLE package_requirements
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  # Collect all of this project's inherited requirements into ${requirements_list}
  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv collect_requirements
      --package-name ${PROJECT_NAME} ${lock_args}
    OUTPUT_VARIABLE requirements_list
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  # Trigger rebuild if any of the requirements files change
  foreach(requirements_file ${requirements_list})
    if(EXISTS ${requirements_file})
      stamp(${requirements_file})
    endif()
  endforeach()

  add_custom_command(COMMENT "Generate virtualenv in ${CMAKE_BINARY_DIR}/${venv_dir}"
    OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_init ${venv_dir}
      --python ${ARG_PYTHON_INTERPRETER} ${venv_args} --extra-pip-args ${processed_pip_args}
  )

  if(DEFINED ARG_INPUT_REQUIREMENTS AND NOT package_requirements STREQUAL "")
    add_custom_command(COMMENT "Lock input requirements if they don't exist"
      OUTPUT ${package_requirements}
      COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_lock ${CMAKE_BINARY_DIR}/${venv_dir}
        --package-name ${PROJECT_NAME} --input-requirements ${ARG_INPUT_REQUIREMENTS}
        --no-overwrite --extra-pip-args ${processed_pip_args}
      WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
      DEPENDS
        ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
        ${PROJECT_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
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
    # CMake copy_directory doesn't preserve symlinks https://gitlab.kitware.com/cmake/cmake/issues/14609
    # COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} ${venv_devel_dir}
    # COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} install/${venv_dir}
    COMMAND mkdir -p ${venv_devel_dir} && cp -r ${venv_dir}/* ${venv_devel_dir}
    COMMAND mkdir -p install/${venv_dir} && cp -r ${venv_dir}/* install/${venv_dir}

    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate ${venv_devel_dir} --target-dir ${venv_devel_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate install/${venv_dir} --target-dir ${venv_install_dir}
    DEPENDS ${CMAKE_BINARY_DIR}/${venv_dir}/bin/activate
  )

  add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
    COMMENT "Per-package virtualenv target"
    DEPENDS
      ${venv_devel_dir}
      install/${venv_dir}
  )

  add_custom_target(${PROJECT_NAME}_venv_lock
    COMMENT "Manually invoked target to generate the lock file on demand"
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_lock ${CMAKE_BINARY_DIR}/${venv_dir}
      --package-name ${PROJECT_NAME} --input-requirements ${ARG_INPUT_REQUIREMENTS}
      --extra-pip-args ${processed_pip_args}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    DEPENDS
      ${venv_devel_dir}
      ${PROJECT_SOURCE_DIR}/${ARG_INPUT_REQUIREMENTS}
  )

  if(CATKIN_ENABLE_TESTING AND NOT package_requirements STREQUAL "" AND (NOT DEFINED ARG_CHECK_VENV OR ARG_CHECK_VENV))
    file(MAKE_DIRECTORY ${CATKIN_TEST_RESULTS_DIR}/${PROJECT_NAME})
    catkin_run_tests_target("venv_check" "${PROJECT_NAME}-requirements" "venv_check-${PROJECT_NAME}-requirements.xml"
      COMMAND "${CATKIN_ENV} rosrun catkin_virtualenv venv_check ${venv_dir} --requirements ${package_requirements} \
        --extra-pip-args \"${processed_pip_args}\" \
        --xunit-output ${CATKIN_TEST_RESULTS_DIR}/${PROJECT_NAME}/venv_check-${PROJECT_NAME}-requirements.xml"
      DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
      WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
  endif()

  install(DIRECTORY ${CMAKE_BINARY_DIR}/install/${venv_dir}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    USE_SOURCE_PERMISSIONS)

  # (pbovbel): NOSETESTS originally set by catkin here:
  # <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
  message(STATUS "Using virtualenv to run Python nosetests: ${nosetests}")
  set(NOSETESTS "${venv_devel_dir}/bin/python -m nose" PARENT_SCOPE)

endfunction()

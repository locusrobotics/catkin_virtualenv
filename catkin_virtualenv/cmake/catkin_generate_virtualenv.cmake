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
  set(oneValueArgs PYTHON_VERSION PYTHON_INTERPRETER USE_SYSTEM_PACKAGES ISOLATE_REQUIREMENTS LOCK_FILE)
  set(multiValueArgs EXTRA_PIP_ARGS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  # Check if this package already has a virtualenv target before creating one
  if(TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(WARNING "catkin_generate_virtualenv was called twice")
    return()
  endif()

  # Handle defaults and warnings
  if(DEFINED ARG_PYTHON_VERSION)
    message(WARNING "PYTHON_VERSION has been deprecated, set 'PYTHON_INTERPRETER python${ARG_PYTHON_VERSION}' instead")
    set(ARG_PYTHON_INTERPRETER "python${ARG_PYTHON_VERSION}")
  endif()

  if(NOT DEFINED ARG_PYTHON_INTERPRETER)
    set(ARG_PYTHON_INTERPRETER "python2")
  endif()

  if(NOT DEFINED ARG_USE_SYSTEM_PACKAGES)
    set(ARG_USE_SYSTEM_PACKAGES TRUE)
  endif()

  if(NOT DEFINED ARG_ISOLATE_REQUIREMENTS)
    set(ARG_ISOLATE_REQUIREMENTS FALSE)
  endif()

  if(NOT DEFINED ARG_LOCK_FILE)
    set(ARG_LOCK_FILE "${CMAKE_BINARY_DIR}/requirements.txt")
    message(WARNING "Please define a LOCK_FILE relative to your sources, and commit together to prevent dependency drift.")
  endif()

  if (NOT DEFINED ARG_EXTRA_PIP_ARGS)
    # set(ARG_EXTRA_PIP_ARGS "-qq" "--retries 10" "--timeout 30")
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
    set(freeze_args "--no-deps")
  endif()

  if(${ARG_USE_SYSTEM_PACKAGES})
    message(STATUS "Using system site packages")
    set(venv_args "${venv_args} --use-system-packages")
  endif()

  # Generate a virtualenv
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_init ${venv_dir}
      --python ${ARG_PYTHON_INTERPRETER} ${venv_args} --extra-pip-args ${processed_pip_args}
  )

  # Freeze requirements
  add_custom_command(OUTPUT ${ARG_LOCK_FILE}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_freeze ${venv_dir}
      --package-name ${PROJECT_NAME} --output-requirements ${ARG_LOCK_FILE} ${freeze_args}
      --no-overwrite --extra-pip-args ${processed_pip_args}
    DEPENDS ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
  )

  # Sync requirements
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/${venv_dir}/bin/activate
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_sync ${venv_dir}
      --requirements ${ARG_LOCK_FILE} --extra-pip-args ${processed_pip_args} --no-overwrite
    DEPENDS
      ${CMAKE_BINARY_DIR}/${venv_dir}/bin/python
      ${ARG_LOCK_FILE}
  )

  # Prepare relocated versions for develspace and installspace
  add_custom_command(OUTPUT ${venv_devel_dir} install/${venv_dir}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} ${venv_devel_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate ${venv_devel_dir} --target-dir ${venv_devel_dir}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${venv_dir} install/${venv_dir}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_relocate install/${venv_dir} --target-dir ${venv_install_dir}
    DEPENDS ${CMAKE_BINARY_DIR}/${venv_dir}/bin/activate
  )

  # Per-package virtualenv target
  add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
    DEPENDS
      ${venv_devel_dir}
      install/${venv_dir}
  )

  # Manually-invoked target to write out ARG_LOCK_FILE
  add_custom_target(${PROJECT_NAME}_freeze
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv venv_freeze ${venv_devel_dir}
      --package-name ${PROJECT_NAME} --output-requirements ${ARG_LOCK_FILE} ${freeze_args}
      --extra-pip-args ${processed_pip_args}
    DEPENDS ${venv_devel_dir}
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

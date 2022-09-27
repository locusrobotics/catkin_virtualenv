# Software License Agreement (GPL)
#
# \file      catkin_install_python.cmake
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
function(catkin_install_python)
  # See https://github.com/ros/catkin/blob/kinetic-devel/cmake/catkin_install_python.cmake for overriden function
  set(options OPTIONAL)
  set(oneValueArgs DESTINATION RENAME_PROCESS)
  set(multiValueArgs PROGRAMS)
  cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

  if(NOT ARG_PROGRAMS)
    message(FATAL_ERROR "catkin_install_python() called without required PROGRAMS argument.")
  endif()
  if(NOT ARG_DESTINATION)
    message(FATAL_ERROR "catkin_install_python() called without required DESTINATION argument.")
  endif()

  if(NOT TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(FATAL_ERROR "${PROJECT_NAME} loaded catkin_virtualenv, but never invoked 'catkin_generate_virtualenv'")
    return()
  endif()

  if (NOT DEFINED ARG_RENAME_PROCESS)
    set(ARG_RENAME_PROCESS TRUE)
  endif()

  # Use CMake templating to create virtualenv loaders for all specified python scripts
  set(install_programs "")

  foreach(program_path ${ARG_PROGRAMS})
    if(NOT IS_ABSOLUTE ${program_path})
      set(program_path "${CMAKE_CURRENT_SOURCE_DIR}/${program_path}")
    endif()
    get_filename_component(program_basename ${program_path} NAME)

    if(EXISTS ${program_path})
      stamp(${program_path})  # Reconfigure when the python script changes. This mirrors upstream behaviour.

      execute_process(
        COMMAND ${CATKIN_ENV} test -x ${program_path}
        RESULT_VARIABLE is_program_executable
      )

      if(is_program_executable STREQUAL "0")
        message(WARNING "Making ${program_path} non-executable. Otherwise 'rosrun ${PROJECT_NAME} ${program_basename}' \
will not work as expected.")
        execute_process(
          COMMAND ${CATKIN_ENV} chmod -x ${program_path}  # This is touching the source space
        )
      endif()

      set(program_install_location ${CATKIN_PACKAGE_SHARE_DESTINATION}/catkin_virtualenv_scripts)

      # For devel-space support, we generate a bash script that invokes the source script via the virtualenv's
      # python interpreter.
      set(devel_program ${CATKIN_DEVEL_PREFIX}/${ARG_DESTINATION}/${program_basename})
      configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.devel.in ${devel_program})
      execute_process(
        COMMAND ${CATKIN_ENV} chmod +x ${devel_program}
      )

      # For install-space support, we install the source script, and then generate a bash script to invoke it using
      # the virtualenv's python interpreter.
      set(install_program ${CMAKE_BINARY_DIR}/${program_basename})
      configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.install.in ${install_program})
      execute_process(
        COMMAND ${CATKIN_ENV} chmod +x ${install_program}
      )

      install(
        FILES ${program_path}
        DESTINATION ${program_install_location}
      )

      install(
        PROGRAMS ${install_program}
        DESTINATION ${ARG_DESTINATION}
      )

    elseif(NOT ARG_OPTIONAL)
      message(FATAL_ERROR "catkin_install_python() called with non-existent file '${program_path}'.")
    endif()
  endforeach()

endfunction()

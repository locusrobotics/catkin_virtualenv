function(catkin_install_python)
  # See https://github.com/ros/catkin/blob/kinetic-devel/cmake/catkin_install_python.cmake for overriden function
  cmake_parse_arguments(ARG "OPTIONAL" "DESTINATION" "PROGRAMS" ${ARGN})
  if(NOT ARG_PROGRAMS)
    message(FATAL_ERROR "catkin_install_python() called without required PROGRAMS argument.")
  endif()
  if(NOT ARG_DESTINATION)
    message(FATAL_ERROR "catkin_install_python() called without required DESTINATION argument.")
  endif()

  # If this package doesn't need a virtualenv, bypass processing python scripts
  if(NOT TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(FATAL_ERROR "${PROJECT_NAME} loaded catkin_virtualenv, but never invoked 'catkin_generate_virtualenv'")
    return()
  endif()

  # # Use CMake templating to load virtualenv into all specified python scripts
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
        message(WARNING "Making ${program_path} non-executable. Otherwise 'rosrun ${PROJECT_NAME} ${program_basename}' will not work as expected.")
        execute_process(
          COMMAND ${CATKIN_ENV} chmod -x ${program_path}  # This is touching the source space
        )
      endif()

      # For develspace support, we generate a bash script that invokes the source script via the virtualenv's
      # python interpreter.
      set(devel_program ${CATKIN_DEVEL_PREFIX}/${ARG_DESTINATION}/${program_basename})
      configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.devel.in ${devel_program})
      execute_process(
        COMMAND ${CATKIN_ENV} chmod +x ${devel_program}
      )

      # For installspace support, we install the source script, and then generate a bash script to invoke it using
      # the virtualenv's python interpreter.
      set(install_program ${CMAKE_BINARY_DIR}/${program_basename})
      configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.install.in ${install_program})
      execute_process(
        COMMAND ${CATKIN_ENV} chmod +x ${install_program}
      )

      install(
        FILES ${program_path}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/catkin_virtualenv_scripts
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

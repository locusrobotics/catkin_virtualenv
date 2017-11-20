# (pbovbel): CATKIN_PACKAGE_SHARE_DESTINATION is not configured yet as catkin_package has not been called
# set(${PROJECT_NAME}_VENV_DIRECTORY ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/venv)
set(${PROJECT_NAME}_VENV_DIRECTORY ${CATKIN_DEVEL_PREFIX}/share/${PROJECT_NAME}/venv)

# (pbovbel): NOSETESTS originally set by catkin here:
# <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
if(NOSETESTS)
  set(NOSETESTS "${${PROJECT_NAME}_VENV_DIRECTORY}/bin/python ${NOSETESTS}")
  message(STATUS "Using virtualenv to run Python nosetests: ${NOSETESTS}")
endif()

function(catkin_generate_virtualenv)
  # Check if this package already has a virtualenv target before creating one
  if(NOT TARGET ${PROJECT_NAME}_generate_virtualenv)

    # Collect all exported pip requirements files, from this package and all dependencies
    execute_process(
      COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv glob_requirements --package-name ${PROJECT_NAME}
      OUTPUT_VARIABLE requirements_list
      OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    if(requirements_list)
      set(generated_requirements ${CMAKE_BINARY_DIR}/generated_requirements.txt)

      foreach(requirements_txt ${requirements_list})
        message(STATUS "Including ${requirements_txt} in bundled virtualenv")
        stamp(${requirements_txt})  # trigger a re-configure if any requirements file changes
      endforeach()

      add_custom_command(OUTPUT ${generated_requirements}
        COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv combine_requirements --requirements-list ${requirements_list} --output-file ${generated_requirements}
        DEPENDS ${requirements_list}
      )

      add_custom_command(OUTPUT ${${PROJECT_NAME}_VENV_DIRECTORY}
        COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv build_venv ${generated_requirements} ${${PROJECT_NAME}_VENV_DIRECTORY} ${PROJECT_NAME}
        DEPENDS ${generated_requirements}
      )

      add_custom_target(${PROJECT_NAME}_generate_virtualenv ALL
        DEPENDS ${${PROJECT_NAME}_VENV_DIRECTORY}
        SOURCES ${requirements_list}
      )

      install(DIRECTORY ${${PROJECT_NAME}_VENV_DIRECTORY}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        USE_SOURCE_PERMISSIONS)

      install(FILES ${generated_requirements}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

    endif()

  endif()
endfunction()

function(catkin_install_python)
  # See https://github.com/ros/catkin/blob/kinetic-devel/cmake/catkin_install_python.cmake for overriden function
  cmake_parse_arguments(ARG "OPTIONAL" "DESTINATION" "PROGRAMS" ${ARGN})
  if(NOT ARG_PROGRAMS)
    message(FATAL_ERROR "catkin_install_python() called without required PROGRAMS argument.")
  endif()
  if(NOT ARG_DESTINATION)
    message(FATAL_ERROR "catkin_install_python() called without required DESTINATION argument.")
  endif()

  catkin_generate_virtualenv()

  # If this package doesn't need a virtualenv, bypass processing python scripts
  if(NOT TARGET ${PROJECT_NAME}_generate_virtualenv)
    # Call upstream catkin_install_python with the original parameters
    _catkin_install_python(
      PROGRAMS ${ARG_PROGRAMS}
      DESTINATION ${ARG_DESTINATION}
      OPTIONAL ${ARG_OPTIONAL}
    )

  else()
    # Use CMake templating to load virtualenv into all specified python scripts
    set(install_programs "")
    foreach(program_file ${ARG_PROGRAMS})
      if(NOT IS_ABSOLUTE ${program_file})
        set(program_file "${CMAKE_CURRENT_SOURCE_DIR}/${program_file}")
      endif()

      if(EXISTS ${program_file})
        stamp(${program_file})  # Reconfigure when the python script changes. This mirrors upstream behaviour.

        execute_process(
          COMMAND ${CATKIN_ENV} test -x ${program_file}
          RESULT_VARIABLE program_executable
        )

        get_filename_component(program_basename ${program_file} NAME)

        if(program_executable STREQUAL "0")
          message(WARNING "${program_file} is executable. This will confuse 'rosrun ${PROJECT_NAME} ${program_basename}', fixing...")
          execute_process(
            COMMAND ${CATKIN_ENV} chmod -x ${program_file}  # This is touching the source space
          )
        endif()

        # We generate two new python scripts using CMake templating:
        #  - devel_program is placed in the develspace, and uses execfile to run the original source file. This means
        #    the workspace does not need to be recompiled for python changes during development
        #  - install_program contains a copy of the original script, and is installed to the installspace/debian.
        set(devel_program ${CATKIN_DEVEL_PREFIX}/${ARG_DESTINATION}/${program_basename})
        set(install_program ${CMAKE_BINARY_DIR}/${program_basename})

        file(READ ${program_file} program_contents)
        # Escape all '\' as '\\' and '"' as '\"'
        string(REPLACE \\ \\\\ program_contents ${program_contents})
        string(REPLACE \" \\\" program_contents ${program_contents})

        configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.develspace.in ${devel_program})
        configure_file(${catkin_virtualenv_CMAKE_DIR}/templates/program.installspace.in ${install_program})

        execute_process(
          COMMAND ${CATKIN_ENV} chmod +x ${devel_program}
        )
        execute_process(
          COMMAND ${CATKIN_ENV} chmod +x ${install_program}
        )

        list(APPEND install_programs ${install_program})

      elseif(NOT ARG_OPTIONAL)
        message(FATAL_ERROR "catkin_install_python() called with non-existent file '${program_file}'.")
      endif()
    endforeach()

    # Call upstream catkin_install_python with all the generated python scripts
    _catkin_install_python(
      PROGRAMS ${install_programs}
      DESTINATION ${ARG_DESTINATION}
      OPTIONAL ${ARG_OPTIONAL}
    )
  endif()
endfunction()

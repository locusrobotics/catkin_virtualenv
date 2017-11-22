# (pbovbel): NOSETESTS originally set by catkin here:
# <https://github.com/ros/catkin/blob/kinetic-devel/cmake/test/nosetests.cmake#L86>
set(NOSETESTS "${${PROJECT_NAME}_VENV_DIRECTORY}/bin/python ${NOSETESTS}")
message(STATUS "Using virtualenv to run Python nosetests: ${${PROJECT_NAME}_VENV_DIRECTORY}")

function(catkin_generate_virtualenv)
  cmake_parse_arguments(ARG "PYTHON3" "" "" ${ARGN})

  # Check if this package already has a virtualenv target before creating one
  if(TARGET ${PROJECT_NAME}_generate_virtualenv)
    message(WARNING "catkin_generate_virtualenv was called twice")
    return()
  endif()

  # Collect all exported pip requirements files, from this package and all dependencies
  execute_process(
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv glob_requirements --package-name ${PROJECT_NAME}
    OUTPUT_VARIABLE requirements_list
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  if(${ARG_PYTHON3})
    set(build_venv_extra "--python3")
  endif()

  set(generated_requirements ${CMAKE_BINARY_DIR}/generated_requirements.txt)

  foreach(requirements_txt ${requirements_list})
     # Trigger a re-configure if any requirements file changes
    stamp(${requirements_txt})
    message(STATUS "Including ${requirements_txt} in bundled virtualenv")
  endforeach()

  # Combine requirements into one list
  add_custom_command(OUTPUT ${generated_requirements}
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv combine_requirements --requirements-list ${requirements_list} --output-file ${generated_requirements}
    DEPENDS ${requirements_list}
  )

  # Build a virtualenv, fixing up paths for its eventual location in ${PROJECT_NAME}_VENV_DIRECTORY
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/venv
    COMMAND ${CATKIN_ENV} rosrun catkin_virtualenv build_venv --requirements ${generated_requirements} --root-dir ${${PROJECT_NAME}_VENV_DIRECTORY} ${build_venv_extra}
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

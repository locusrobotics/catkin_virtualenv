cmake_minimum_required(VERSION 3.5.1)
project(catkin_virtualenv)

find_package(catkin REQUIRED)

catkin_package(CFG_EXTRAS ${PROJECT_NAME}-extras.cmake)

catkin_python_setup()

install(DIRECTORY cmake
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ${PROJECT_NAME}-extras.cmake* EXCLUDE
)

catkin_install_python(
  PROGRAMS
    scripts/build_venv
    scripts/combine_requirements
    scripts/glob_requirements
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

if(CATKIN_ENABLE_TESTING)
  find_package(roslint REQUIRED)
  roslint_python()
  roslint_add_test()

  catkin_add_nosetests(test)
endif()

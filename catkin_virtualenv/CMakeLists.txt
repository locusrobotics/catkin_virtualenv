cmake_minimum_required(VERSION 2.8.3)
project(catkin_virtualenv)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(CFG_EXTRAS ${PROJECT_NAME}-extras.cmake)

catkin_python_setup()

catkin_install_python(
  PROGRAMS
    scripts/build_venv
    scripts/combine_requirements
    scripts/glob_requirements
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY cmake
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ${PROJECT_NAME}-extras.cmake* EXCLUDE
)

if(CATKIN_ENABLE_TESTING)
  find_package(roslint)
  roslint_python()
  roslint_add_test()
endif()

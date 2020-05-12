cmake_minimum_required(VERSION 3.5.1)
project(catkin_virtualenv)

find_package(catkin REQUIRED)

catkin_package(CFG_EXTRAS ${PROJECT_NAME}-extras.cmake)

catkin_python_setup()

install(DIRECTORY cmake
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ${PROJECT_NAME}-extras.cmake* EXCLUDE
)

set(python_scripts
  scripts/venv_init
  scripts/venv_freeze
  scripts/venv_sync
  scripts/venv_relocate
)

catkin_install_python(PROGRAMS ${python_scripts}
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  find_package(roslint REQUIRED)
  roslint_python()
  roslint_python(${python_scripts})
  roslint_add_test()

  catkin_add_nosetests(test)
endif()

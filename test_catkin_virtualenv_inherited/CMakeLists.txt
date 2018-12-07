cmake_minimum_required(VERSION 3.5.1)
project(test_catkin_virtualenv_inherited)

find_package(catkin REQUIRED COMPONENTS catkin_virtualenv)

catkin_package()

catkin_generate_virtualenv()

install(FILES requirements.txt
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)

  catkin_install_python(
    PROGRAMS
      test/test_virtualenv_script
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

  catkin_add_nosetests(test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )

  add_rostest(test/virtualenv_script.test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )

endif()

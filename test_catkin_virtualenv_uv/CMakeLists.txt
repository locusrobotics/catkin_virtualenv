cmake_minimum_required(VERSION 3.5.1)
project(test_catkin_virtualenv_uv)

find_package(catkin REQUIRED COMPONENTS catkin_virtualenv)

catkin_generate_virtualenv(
  INPUT_REQUIREMENTS requirements.in
  USE_UV TRUE
  UV_CACHE /tmp/testing/uv/cache
)

# Order with catkin_generate_virtualenv shouldn't matter
catkin_package()

install(FILES requirements.txt
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)

  catkin_install_python(
    PROGRAMS
      test/test_virtualenv_script_uv
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

  # Nose isn't supported for python 3.10
  #catkin_add_nosetests(test
  #  DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  #)

  add_rostest(test/virtualenv_script.test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )

endif()

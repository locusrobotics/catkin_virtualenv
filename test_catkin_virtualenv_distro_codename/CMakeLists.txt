cmake_minimum_required(VERSION 3.5.1)
project(test_catkin_virtualenv_distro_codename)

find_package(catkin REQUIRED COMPONENTS catkin_virtualenv)

catkin_generate_virtualenv(
  INPUT_REQUIREMENTS requirements.in
)

catkin_package()

install(FILES requirements.txt requirements-jammy.txt requirements-noble.txt
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(test
    DEPENDENCIES ${PROJECT_NAME}_generate_virtualenv
  )
endif()

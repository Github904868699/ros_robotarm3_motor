cmake_minimum_required(VERSION 3.0.2)
project(web_ui)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY www DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(PROGRAMS scripts/simple_http_server.py scripts/ws_bridge.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

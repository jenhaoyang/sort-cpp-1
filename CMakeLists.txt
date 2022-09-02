cmake_minimum_required(VERSION 3.16.1)
project(sortcpp)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
# python -m pybind11 --cmakedir 可以印出pybind11位置
# https://pybind11.readthedocs.io/en/stable/changelog.html?highlight=cmakedir
set(pybind11_DIR ${PROJECT_SOURCE_DIR}/venv/lib/python3.8/site-packages/pybind11/share/cmake/pybind11)

# Try to find OpenCV
find_package(OpenCV REQUIRED)
if (OpenCV_FOUND)
    # If the package has been found, several variables will
    # be set, you can find the full list with descriptions
    # in the OpenCVConfig.cmake file.
    # Print some message showing some of them
    message(STATUS "OpenCV library status:")
    message(STATUS "    version: ${OpenCV_VERSION}")
    message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")
else ()
    message(FATAL_ERROR "Could not locate OpenCV")
endif()

# Try to find Boost
find_package(Boost COMPONENTS program_options filesystem REQUIRED)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Could not locate Boost")
endif()

find_package (Python3 COMPONENTS Interpreter Development REQUIRED)
if(Python3_FOUND)
    message(STATUS "Python3 library status:")
    message(STATUS "    version: ${Python3_VERSION}")
    message(STATUS "    include path: ${Python3_INCLUDE_DIRS}")
    include_directories(${Python3_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Could not locate Python3")
endif()

# Try to find Eigen headers
find_package(Eigen3 REQUIRED)
if(Eigen3_FOUND)
    include( ${EIGEN3_USE_FILE} )
    message(STATUS "Eigen3 library status:")
    message(STATUS "    version: ${Eigen3_VERSION}")
    message(STATUS "    include path: ${Eigen3_INCLUDE_DIRS}")
else ()
    message(FATAL_ERROR "Could not locate Eigen3")
endif()

# include 我們自己的資料夾
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/python)

file (GLOB SOURCE_FILES ${PROJECT_SOURCE_DIR}/include/*.cpp)
file (GLOB HEADER_FILES ${PROJECT_SOURCE_DIR}/src/*.hpp)
file (GLOB PYTHON_FILES ${PROJECT_SOURCE_DIR}/python/*.cpp ${PROJECT_SOURCE_DIR}/python/*.hpp)


# print include dir
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()

# Set up such that XCode organizes the files
source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCE_FILES} ${HEADER_FILES} ${PYTHON_FILES} )

find_package(pybind11 REQUIRED)

message(STATUS "    SOURCE_FILES: ${SOURCE_FILES}")
message(STATUS "    HEADER_FILES: ${HEADER_FILES}")
message(STATUS "    PYTHON_FILES: ${PYTHON_FILES}")
pybind11_add_module(sortcpp 
	"/home/ai_server/2005013/ai_surve/sort-cpp-1/python/sort_cpp.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/src/kalman_filter.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/src/main.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/src/munkres.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/src/track.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/src/tracker.cpp"
    "/home/ai_server/2005013/ai_surve/sort-cpp-1/include/matrix.cpp"
)


target_link_libraries(sortcpp PUBLIC)

install(TARGETS sortcpp
  COMPONENT python
  LIBRARY DESTINATION "/home/ai_server/2005013/ai_surve/sort-cpp-1/venv/lib/python3.8/site-packages"
)



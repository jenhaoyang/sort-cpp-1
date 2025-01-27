cmake_minimum_required(VERSION 3.16.1)
project(sort-cpp)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

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
    include_directories(${OpenCV_INCLUDE_DIRS})
    link_libraries(${OpenCV_LIBRARIES})
else ()
    message(FATAL_ERROR "Could not locate OpenCV")
endif()

# Try to find Eigen headers
find_package(Eigen3 REQUIRED)
if(Eigen3_FOUND)
    get_target_property(EIGEN3_INCLUDE_DIR Eigen3::Eigen INTERFACE_INCLUDE_DIRECTORIES)
    #include( ${EIGEN3_USE_FILE} ) #This line not work on windows
    include_directories( ${EIGEN3_INCLUDE_DIR})
    message(STATUS "Eigen3 library status:")
    message(STATUS "    version: ${Eigen3_VERSION}")
    message(STATUS "    include path: ${EIGEN3_INCLUDE_DIR}")
else ()
    message(FATAL_ERROR "Could not locate Eigen3")
endif()

# Try to find Boost
# find_package(Boost COMPONENTS program_options filesystem REQUIRED)
# if(Boost_FOUND)
#     include_directories(${Boost_INCLUDE_DIRS})
# else ()
#     message(FATAL_ERROR "Could not locate Boost")
# endif()

find_package (Python3 COMPONENTS Interpreter Development REQUIRED)
if(Python3_FOUND)
    message(STATUS "Python3 library status:")
    message(STATUS "    version: ${Python3_VERSION}")
    message(STATUS "    include path: ${Python3_INCLUDE_DIRS}")
    include_directories(${Python3_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Could not locate Python3")
endif()

include_directories(${PROJECT_SOURCE_DIR}/include ${PROJECT_SOURCE_DIR}/pybind11/include)

# print include dir
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()

file(GLOB SOURCE_FILES src/*.cpp)


# Scikit-Build does not add your site-packages to the search path
# automatically, so we need to add it _or_ the pybind11 specific directory
# here.
message(STATUS "Python3_EXECUTABLE ${Python3_EXECUTABLE}")
execute_process(
  COMMAND "${Python3_EXECUTABLE}" -c
          "import pybind11; print(pybind11.get_cmake_dir())"
  OUTPUT_VARIABLE _tmp_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
set(pybind11_DIR "${_tmp_dir}")
message(STATUS "pybind11_DIR ${_tmp_dir}")





# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core MODULE src/tracker.cpp src/track.cpp src/munkres.cpp src/kalman_filter.cpp include/matrix.cpp) # _core出現在__init__.py

target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _core DESTINATION .)

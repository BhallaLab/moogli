cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules")
option(BUILD_STATIC "Link osg statically. Useful for creating standalone packages" OFF)

add_definitions(-std=c++11)

if(APPLE)
    add_definitions( "-stdlib=libc++" )
endif(APPLE)
add_definitions(-fPIC)

find_package(PythonDev REQUIRED)
find_package(SIP REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

find_package(PyQt5 REQUIRED)
message("++ Found SIP flags: ${PYQT5_SIP_FLAGS}")
separate_arguments(PYQT5_SIP_FLAGS) # convert space separated values to a list

SET(SIP_CONCAT_PARTS 4)
SET(SIP_EXTRA_OPTIONS ${PYQT5_SIP_FLAGS})

IF("${PYQT5_SIP_FLAGS}" STREQUAL "")
    MESSAGE(FATAL_ERROR "++ No PYQT5_SIP_FLAGS found. Can't continue")
ENDIF()
MESSAGE("++ Using sip flags: ${SIP_EXTRA_OPTIONS}")


IF (NOT BINDINGS_GLOBAL_INSTALL)
    SET(PYTHON_SITE_PACKAGES_DIR ${QGIS_DATA_DIR}/python)
ENDIF (NOT BINDINGS_GLOBAL_INSTALL)
IF (WITH_CUSTOM_WIDGETS)
    SET(PYUIC_WIDGET_PLUGIN_DIRECTORY ${PYQT5_MOD_DIR}/uic/widget-plugins/)
ENDIF (WITH_CUSTOM_WIDGETS)

find_package(Qt5Widgets CONFIG REQUIRED)
find_package(Qt5OpenGL)

find_package(OpenSceneGraph 3.0.2 REQUIRED 
    osgFX 
    osgGA
    osgAnimation 
    osgViewer
    osgManipulator
    osgSim 
    osgText
    osgDB
    osgUtil
    OpenThreads
    )

MESSAGE(STATUS "OSG LIBRARIES: ${OPENSCENEGRAPH_LIBRARIES}")

if(QT_USE_FILE)
    include(${QT_USE_FILE})
endif()

FIND_PROGRAM(SIP_EXECUTABLE sip)
MESSAGE("++ SIP ${SIP_EXECUTABLE}")

include_directories(./include ${PROJECT_SOURCE_DIR}/bin/include ".")
include_directories(${OSGQT_INCLUDE_DIR})
include_directories(${SIP_INCLUDES} ${PYTHON_INCLUDE_DIRS})
include_directories(${OPENSCENEGRAPH_INCLUDE_DIRS})
include_directories(${OSGANIMATION_INCLUDE_DIR})

#qt5 paths.
include_directories(${Qt5Widgets_INCLUDE_DIRS})
include_directories(${Qt5Core_INCLUDE_DIRS})
include_directories(${Qt5OpenGL_INCLUDE_DIRS})

add_subdirectory(${PROJECT_SOURCE_DIR}/bin/sip)
add_subdirectory(${PROJECT_SOURCE_DIR}/bin/src)

# NOTE: moc should be run to genrate these files.
set(MOC_HEADERS ${PROJECT_SOURCE_DIR}/bin/include/view/Viewer.hpp)
set(MOC_SOURCES "")
foreach(_MOC_HEADER ${MOC_HEADERS})
    get_filename_component(_TGT_NAME ${MOC_HEADERS} NAME_WE)
    set(_MOC_SOURCE ${_TGT_NAME}.moc.cpp)
    message(STATUS "Adding target: ${_MOC_HEADER} ->  ${_MOC_SOURCE} using MOC")
    add_custom_command(OUTPUT ${_MOC_SOURCE}
        COMMAND moc ${_MOC_HEADER} -o ${_MOC_SOURCE}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Generating ${_MOC_SOURCE} from ${_MOC_HEADER}"
        )
    add_custom_target(${_TGT_NAME} ALL DEPENDS ${_MOC_SOURCE})
    list(APPEND MOC_SOURCES ${_MOC_SOURCE})
endforeach()
set_source_files_properties(${MOC_SOURCES} GENERATED)

add_library(_moogli SHARED ${MOC_SOURCES})


if(APPLE)
    SET_TARGET_PROPERTIES(_moogli 
        PROPERTIES OUTPUT_NAME "_moogli.so"  
        LINK_FLAGS "-undefined dynamic_lookup"
        SUFFIX ""
        )
else(APPLE)
    SET_TARGET_PROPERTIES(_moogli PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/core"
        PREFIX ""
        )
endif(APPLE)

## Link the following libraries to moogli.
SET(STATIC_LIBRARIES sip src)

SET(DYNAMIC_LIBRARIES Qt5::Core Qt5::OpenGL)

IF(BUILD_STATIC)
    LIST(APPEND STATIC_LIBRARIES ${OPENSCENEGRAPH_LIBRARIES})
ELSE(BUILD_STATIC)
    LIST(APPEND DYNAMIC_LIBRARIES ${OPENSCENEGRAPH_LIBRARIES})
ENDIF(BUILD_STATIC)

IF(APPLE)
    TARGET_LINK_LIBRARIES(_moogli "-Wl,-all_load" ${STATIC_LIBRARIES})
ELSE(APPLE)
    TARGET_LINK_LIBRARIES(_moogli
        "-Wl,--whole-archive"
        ${STATIC_LIBRARIES}
        "-Wl,--no-whole-archive"
        )
ENDIF(APPLE)

target_link_libraries(_moogli ${DYNAMIC_LIBRARIES})

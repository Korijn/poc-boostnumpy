# flake8: noqa
from setuptools import Extension, find_packages, setup

from setup_utils import get_data_files, get_package_data
from version import __version__


packages = find_packages()
package_data = get_package_data(packages, exclude=('.py', '.pyc', '.cpp', '.h'))
print(packages)

setup(
    name='hnpypkg',
    version=__version__,
    packages=packages,
    install_requires=['numpy'],
    ext_modules=[
        Extension('hnpypkg.hello_world', ['hnpypkg/hello_world.cpp'],
                  runtime_library_dirs=["$ORIGIN"],
                  include_dirs=['build_boost/include/boost-1_66'],
                  library_dirs=['hnpypkg'],
                  libraries=["boost_python3", "boost_numpy3"]),
    ],
    package_data=package_data,
    include_package_data=True,
)

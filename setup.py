from setuptools import setup, Extension
from setup_utils import is_win, get_data_files, get_package_data, BinaryDistribution


# leaving out headers for now, slows development cycle down significantly
# 'include/boost-1_66'
data_paths = ['lib', 'bin']
if is_win:
    data_paths = ['libs', 'Scripts']
data_files = get_data_files('build_boost', data_paths)

packages = ['hnpypkg']
package_data = get_package_data(packages, exclude=('.py', '.pyc', '.cpp', '.h'))


setup(
    name='hnpypkg',
    packages=packages,
    install_requires=['numpy'],
    ext_modules=[
        Extension('hnpypkg.hello_world', ['hnpypkg/hello_world.cpp'],
                  runtime_library_dirs=["$ORIGIN"],
                  include_dirs=['build_boost/include/boost-1_66'],
                  library_dirs=['hnpypkg'],
                  libraries=["boost_python3", "boost_numpy3"]),
    ],
    data_files=data_files,
    package_data=package_data,
    include_package_data=True,
    distclass=BinaryDistribution,
)

from setuptools import setup, Extension
from setup_utils import is_win, get_data_files


# leaving out headers for now, slows development cycle down significantly
# 'include/boost-1_66'
data_paths = ['lib', 'bin']
if is_win:
    data_paths = ['libs', 'Scripts']
data_files = get_data_files('build_boost', data_paths)


setup(
    name='hnpypkg',
    packages=['hnpypkg'],
    install_requires=['numpy'],
    ext_modules=[
        Extension('hnpypkg.hello_world', ['hnpypkg/hello_world.cpp'],
                  include_dirs=['build_boost/include/boost-1_66'],
                  library_dirs=[f'build_boost/lib{"s" if is_win else ""}']),
    ],
    data_files=data_files,
)

import logging
import subprocess
from multiprocessing import cpu_count
import sys
from os import listdir, makedirs, unlink
from os.path import join, exists, abspath
import re
import shutil
from sysconfig import get_paths

from setup_utils import get_vcvarsall, is_win, get_lib_dir

sysconfig_paths = get_paths()


def call(cmd, **kwargs):
    cwd = f"{kwargs['cwd']}> " if 'cwd' in kwargs else ""
    msg = f"spawning subprocess: {cwd}{cmd}"
    logging.info(msg)
    subprocess.run(cmd, shell=True, check=True, **kwargs)


def main(args):
    build_prefix = abspath("build_boost")
    pkg_prefix = abspath("hnpypkg")
    toolset = "gcc"
    sh_ext = "sh"
    inlude = sysconfig_paths['include']
    if is_win:
        call(f"\"{get_vcvarsall()}\" amd64")
        toolset = "msvc"
        sh_ext = "bat"
    if "--init" in args:
        call(f"./bootstrap.{sh_ext}", cwd="boost_1_66_0")
    call("./b2"
         f" toolset={toolset}"
         " address-model=64"
         " link=shared"
         " variant=release"
         " threading=multi"
         " runtime-link=shared"
         f" include={inlude}"
         " --with-python"
         f" -j{cpu_count()}"
         " install"
         f" --prefix=\"{build_prefix}\""
         f" --libdir=\"{pkg_prefix}\"",
         cwd="boost_1_66_0")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main(sys.argv[1:])

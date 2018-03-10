import logging
import subprocess
from multiprocessing import cpu_count
import sys
from os import listdir, makedirs, unlink
from os.path import join, exists, abspath
import re
import shutil

from setup_utils import get_vcvarsall, is_win


def call(cmd, **kwargs):
    cwd = f"{kwargs['cwd']}> " if 'cwd' in kwargs else ""
    msg = f"spawning subprocess: {cwd}{cmd}"
    logging.info(msg)
    subprocess.run(cmd, shell=True, check=True, **kwargs)


def main(args):
    prefix = abspath("build_boost")
    if "install" in args:
        prefix = sys.prefix
    bindir = "bin"
    libdir = "lib"
    if is_win:
        bindir = "Scripts"
        libdir = "libs"
        call(f"\"{get_vcvarsall()}\" amd64")
    if "--init" in args:
        call(f"bootstrap", cwd="boost_1_66_0")
    call("b2"
         " toolset=msvc"
         " address-model=64"
         " link=shared"
         " variant=release"
         " threading=multi"
         " runtime-link=shared"
         " --with-python"
         f" -j{cpu_count()}"
         " install"
         f" --prefix=\"{prefix}\""
         f" --libdir=\"{join(prefix, libdir)}\"",
         cwd="boost_1_66_0")
    if is_win:
        makedirs(join(prefix, bindir), exist_ok=True)
        for f in filter(lambda f: re.match('boost_.*\.(dll|exe)$', f), listdir(join(prefix, libdir))):
            s = join(prefix, libdir, f)
            d = join(prefix, bindir, f)
            if not exists(d):
                logging.info(f"moving misplaced binary {s} to {d}")
                shutil.copy(s, d)
            if exists(s):
                logging.info(f"removing misplaced binary {s}")
                unlink(s)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main(sys.argv[1:])

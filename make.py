from setuptools import Extension, setup
import subprocess
import os
import sysconfig


def build(kwargs):
    subprocess.check_call(["sh", "./build.sh", sysconfig.get_path("include")])
    setup(
        **kwargs,
    )

    """ext_modules=[
            Extension(
                name="pbs_ifl",
                sources=["python_pbs/extensions/pbs/pbs_ifl_wrap.c"],
                extra_compile_args=[
                    "-Wall",
                    "-Wno-unused-variable",
                    "-fPIC",
                    "-shared",
                    "-I/opt/pbs/include",
                ],
                extra_link_args=[
                    "-L/opt/pbs/lib",
                    "-lpbs",
                    f"-o{os.path.abspath('./python_pbs/extensions/pbs/_pbs_ifl.so')}",
                ],
            ),
        ],"""

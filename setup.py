#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for PyDSE.

    This file was generated with PyScaffold 0.5, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    https://github.com/blue-yonder/pyscaffold
"""

import os
import sys
import inspect
from distutils.cmd import Command

import versioneer
import setuptools
from setuptools.command.test import test as TestCommand
from setuptools import setup

__location__ = os.path.join(os.getcwd(), os.path.dirname(
    inspect.getfile(inspect.currentframe())))

# Change these settings according to your needs
MAIN_PACKAGE = "pydse"
DESCRIPTION = "Dynamic System Estimation for Python"
LICENSE = "new BSD"
URL = "http://pydse.readthedocs.org/"
AUTHOR = "Florian Wilhelm"
EMAIL = "Florian.Wilhelm@blue-yonder.com"

COVERAGE_XML = False
COVERAGE_HTML = False
JUNIT_XML = False

# Add here all kinds of additional classifiers as defined under
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'License :: OSI Approved :: BSD License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.4',
               'Intended Audience :: Science/Research',
               'Topic :: Scientific/Engineering :: Mathematics'
               ]

# Add here console scripts like ['hello_world = pydse.module:function']
CONSOLE_SCRIPTS = []

# temporarily redirect configuration directory
# to prevent matplotlib import testing for
#  writeable directory outside of sandbox
os.environ['MPLCONFIGDIR'] = "."

# Versioneer configuration
versioneer.versionfile_source = os.path.join(MAIN_PACKAGE, '_version.py')
versioneer.versionfile_build = os.path.join(MAIN_PACKAGE, '_version.py')
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = MAIN_PACKAGE + '-'


class PyTest(TestCommand):
    user_options = [("cov=", None, "Run coverage"),
                    ("cov-xml=", None, "Generate junit xml report"),
                    ("cov-html=", None, "Generate junit html report"),
                    ("junitxml=", None, "Generate xml of test results")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.cov_xml = False
        self.cov_html = False
        self.junitxml = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        if self.cov is not None:
            self.cov = ["--cov", self.cov, "--cov-report", "term-missing"]
            if self.cov_xml:
                self.cov.extend(["--cov-report", "xml"])
            if self.cov_html:
                self.cov.extend(["--cov-report", "html"])
        if self.junitxml is not None:
            self.junitxml = ["--junitxml", self.junitxml]

    def run_tests(self):
        try:
            import pytest
        except:
            raise RuntimeError("py.test is not installed, "
                               "run: pip install pytest")
        params = {"args": self.test_args}
        if self.cov:
            params["args"] += self.cov
            params["plugins"] = ["cov"]
        if self.junitxml:
            params["args"] += self.junitxml
        errno = pytest.main(**params)
        sys.exit(errno)


def sphinx_builder():
    try:
        from sphinx.setup_command import BuildDoc
        from sphinx import apidoc
    except ImportError:
        class NoSphinx(Command):
            user_options = []

            def initialize_options(self):
                raise RuntimeError("Sphinx documentation is not installed, "
                                   "run: pip install sphinx")

        return NoSphinx

    class BuildSphinxDocs(BuildDoc):

        def run(self):
            output_dir = os.path.join(__location__, "docs/_rst")
            module_dir = os.path.join(__location__, MAIN_PACKAGE)
            cmd_line_template = "sphinx-apidoc -f -o {outputdir} {moduledir}"
            cmd_line = cmd_line_template.format(outputdir=output_dir,
                                                moduledir=module_dir)
            apidoc.main(cmd_line.split(" "))
            BuildDoc.run(self)

    return BuildSphinxDocs


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    return [req for req in content.split("\\n") if req != '']


def read(fname):
    return open(os.path.join(__location__, fname)).read()


# Assemble additional setup commands
cmdclass = versioneer.get_cmdclass()
cmdclass['docs'] = sphinx_builder()
cmdclass['doctest'] = sphinx_builder()
cmdclass['test'] = PyTest

# Some help variables for setup()
version = versioneer.get_version()
docs_path = os.path.join(__location__, "docs")
docs_build_path = os.path.join(docs_path, "_build")
install_reqs = get_install_requirements("requirements.txt")


def setup_package():
    command_options = {
        'docs': {'project': ('setup.py', MAIN_PACKAGE),
                 'version': ('setup.py', version.split('-', 1)[0]),
                 'release': ('setup.py', version),
                 'build_dir': ('setup.py', docs_build_path),
                 'config_dir': ('setup.py', docs_path),
                 'source_dir': ('setup.py', docs_path)},
        'doctest': {'project': ('setup.py', MAIN_PACKAGE),
                    'version': ('setup.py', version.split('-', 1)[0]),
                    'release': ('setup.py', version),
                    'build_dir': ('setup.py', docs_build_path),
                    'config_dir': ('setup.py', docs_path),
                    'source_dir': ('setup.py', docs_path),
                    'builder': ('setup.py', 'doctest')},
        'test': {'test_suite': ('setup.py', 'tests'),
                 'cov': ('setup.py', 'pydse')}
    }
    if JUNIT_XML:
        command_options['test']['junitxml'] = ('setup.py', 'junit.xml')
    if COVERAGE_XML:
        command_options['test']['cov_xml'] = ('setup.py', True)
    if COVERAGE_HTML:
        command_options['test']['cov_html'] = ('setup.py', True)

    setup(name=MAIN_PACKAGE,
          version=version,
          url=URL,
          description=DESCRIPTION,
          author=AUTHOR,
          author_email=EMAIL,
          license=LICENSE,
          long_description=read('README.rst'),
          classifiers=CLASSIFIERS,
          test_suite='tests',
          packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
          install_requires=install_reqs,
          cmdclass=cmdclass,
          tests_require=['pytest-cov', 'pytest'],
          include_package_data=True,
          package_data={MAIN_PACKAGE: ['data/*']},
          command_options=command_options,
          entry_points={'console_scripts': CONSOLE_SCRIPTS})

if __name__ == "__main__":
    setup_package()

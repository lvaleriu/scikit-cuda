#!/usr/bin/env python

import sys
import os
from glob import glob
from setuptools.command.build_py import build_py
from distutils.command.install_headers import install_headers
from setuptools import find_packages
from numpy.distutils.core import setup
from version import __version__

NAME =               'scikits.cuda'
VERSION =            __version__
AUTHOR =             'Lev Givon'
AUTHOR_EMAIL =       'lev@columbia.edu'
URL =                'http://bionet.ee.columbia.edu/code/'
DESCRIPTION =        'Python utilities for CUDA'
LONG_DESCRIPTION =   DESCRIPTION
DOWNLOAD_URL =       URL
LICENSE =            'BSD'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development']
NAMESPACE_PACKAGES = ['scikits']
PACKAGES =           find_packages()


# Overwrite the copy of scikits/cuda/__info__.py that will be
# installed with the actual header installation path. This is
# necessary so that PyCUDA can find the headers when executing the
# kernels in this package that use it:
class custom_build_py(build_py):
    def run(self):
        build_py.run(self)
        package_dir = self.get_package_dir('scikits.cuda')
        inst_obj = self.distribution.command_obj['install']
        install_headers_pdir, _ = os.path.split(inst_obj.install_headers)
        self.install_dir = install_headers_pdir + '/scikits/cuda'

        filename = os.path.join(self.build_lib, package_dir, '__info__.py')
        f = open(filename, 'w')
        f.write('# Installation location of C headers:\n')
        f.write('install_headers = \"%s\"\n' % self.install_dir)
        f.close()

# Install the C headers in scikits/cuda rather than scikits.cuda:
class custom_install_headers(install_headers):
    def run(self):
        inst_obj = self.distribution.command_obj['install']
        install_headers_pdir, _ = os.path.split(inst_obj.install_headers)
        self.install_dir = install_headers_pdir + '/scikits/cuda'
        install_headers.run(self)

def configuration(parent_package='', top_path=None,
                  package_name=NAME):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path,
                           version = VERSION,
                           author = AUTHOR,
                           author_email = AUTHOR_EMAIL,
                           license = LICENSE,
                           url = URL,
                           download_url = DOWNLOAD_URL,
                           description = DESCRIPTION,
                           long_description = LONG_DESCRIPTION,
                           classifiers = CLASSIFIERS)
    config.set_options(
        ignore_setup_xxx_py = True,
        assume_default_configuration = True,
        delegate_options_to_subpackages = True,
        quiet = True,
        )
    
    config.add_subpackage('scikits')
    config.add_data_files('scikits/__init__.py')

    config.add_subpackage(NAME)
    
    return config

if __name__ == "__main__":
    setup(configuration = configuration,
          name = NAME,
          namespace_packages = NAMESPACE_PACKAGES,
          packages = PACKAGES,
          headers = glob('scikits/cuda/*.h'),
          install_requires = ["numpy",
                              "pycuda >= 0.94rc"], 
          cmdclass={"build_py": custom_build_py,
                    "install_headers": custom_install_headers})


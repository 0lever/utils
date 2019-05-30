# -*- coding: utf-8 -*-
import os
import pkg_resources
from setuptools import setup, find_packages

requirements = pkg_resources.resource_string(__name__, "requirements.txt")
requires = requirements.decode().split(os.linesep)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='0lever-utils',

      version="0.1.6",

      url='https://github.com/0lever/utils',

      author='fqiyou',

      author_email='yc.fqiyou@gmail.com',

      description=u'utils',

      install_requires=requires,

      packages=find_packages(),

      # long_description=open('README.md').read(),

      # long_description=long_description,

      # long_description_content_type="text/markdown",

      package_data={
      },
      entry_points={
      }

)

# pip freeze
# source activate execpython
# python setup.py sdist
# python setup.py install
# python setup.py bdist_wheel/python setup.py sdist
# python setup.py bdist_wheel upload -r coohua
# python setup.py bdist_wheel upload -r pypi
# pip install --upgrade 0lever-utils -i https://pypi.org/simple/

# /usr/local/app/application/anaconda/anaconda2/envs/python36/bin/python  setup.py bdist_wheel upload -r pypi
# /usr/local/app/application/anaconda/anaconda2/envs/python-tools/bin/python  setup.py bdist_wheel upload -r pypi

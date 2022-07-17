import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup

setup(
    name='micropython-micronet',
    py_modules=['micronet'],
    version='0.0.1',
    description='MicroPython library for networking',
    url='https://github.com/yeranosyanvahan/micronet',
    author='Vahan Yeranosyan',
    author_email='vahan@yeranosyanvahan.com',
    maintainer='Vahan Yeranosyan',
    maintainer_email='vahan@yeranosyanvahan.com',
    license='MIT'
)
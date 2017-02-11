from setuptools import setup

setup(
    name='pykarel',
    version='0.3',
    description='Stanford Karel Interpreter',
    author='Albert Manya',
    packages=['pykarel', 'pykarel.karel',
              'pykarel.parser', 'pykarel.scanner',
              'pykarel.util', 'pykarel.vm'],
)

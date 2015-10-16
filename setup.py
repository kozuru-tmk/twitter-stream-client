from setuptools import setup
import re

def get_version():
    version = '0.0.0'
    with open('twitter_stream/version.py', 'r') as fd:
        regex = re.compile(r'VERSION *= *[\'"]([^\'"]*)[\'"]')
        for line in fd:
            match = regex.search(line)
            if match:
                version = match.group(1)
                break
    return version
__version__ = get_version()

packages = [
    'twitter_stream'
]

requires = []

setup(
    name='twitter_stream',
    version=__version__,
    description='Python twitter stream library',
    license='MIT',
    author='Tomoki Kozuru',
    url='https://github.com/kozuru-tmk/twitter_stream',
    packages=packages,
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        'Development status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ]
)

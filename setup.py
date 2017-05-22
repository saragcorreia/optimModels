from setuptools import setup, find_packages

setup(
    name = 'optimModels',
    version = '0.0.1',
    package_dir = {'':'src'},
    packages = find_packages('src'),
    install_requires = [
        'odespy',
        'inspyred',
        'framed'],
    author = 'Sara Correia',
    author_email = 'sarag.correia@gmail.com',
    description = 'optimModels - strain optimization',
    keywords = 'metabolism modeling',
    url = 'https://github.com/saragcorreia/optimModels.git',
    long_description = open('README.rst').read(),
    classifiers = [
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
    ],
)

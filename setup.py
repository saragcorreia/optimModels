from setuptools import setup, find_packages

setup(
    name = 'optimModels',
    version = '0.0.3',
    package_dir = {'':'src'},
    packages = find_packages('src'),
    install_requires = [
        'odespy',
        'inspyred',
        'framed'],
    author = 'Sara Correia',
    author_email = 'sarag.correia@gmail.com',
    description = 'optimModels - strain optimization',
    license = 'Apache License Version 2.0',
    keywords = 'strain design',
    url = 'https://github.com/saragcorreia/optimModels.git',
    long_description = open('README.rst').read(),
    classifiers = [
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
    ],
)

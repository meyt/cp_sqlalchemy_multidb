from setuptools import setup

readme = open('README.rst').read()

requirements = [
    'cherrypy',
    'sqlalchemy',
]

setup(
    name='cp_sqlalchemy_multidb',
    version='0.2.1',
    description='SQLAlchemy with multiple database support plugin for cherrypy',
    long_description=readme,
    author='Mahdi Ghane.g',
    author_email='eric@ionrock.org',
    url='https://github.com/meyt/cp_sqlalchemy_multidb',
    packages=[
        'cp_sqlalchemy_multidb',
    ],
    package_dir={'cp_sqlalchemy_multidb':
                 'cp_sqlalchemy_multidb'},
    include_package_data=True,
    install_requires=requirements,
    license='GPLv3',
    zip_safe=False,
    keywords='cp_sqlalchemy_multidb sqlalchemy cherrypy multiple_database',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Framework :: CherryPy',
        'Topic :: Database',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)

from setuptools import setup
setup(
    name='userexit',
    version='0.1',
    description="Use exceptions to abort without a traceback, rather than sys.exit()",
    long_description='',
    url='https://github.com/datagrok/python-userexit',
    author='Michael F. Lamb',
    author_email='mike@datagrok.org',
    license='AGPL-3.0+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='sysexit systemexit exception traceback exit abort',
    py_modules=["userexit"],
)

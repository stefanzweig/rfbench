from setuptools import setup

filename = 'rfbench/version.py'
exec(open(filename).read())

setup(
    name             = 'robotframework workbench',
    version          = __version__,
    author           = 'Stefan Zweig',
    author_email     = 'stefan.zweig@gmail.com',
    url              = 'https://github.com/stefanzweig/rfbench/',
    keywords         = 'robotframework',
    license          = 'Apache License 2.0',
    description      = 'Simple toolkits for robotframework',
    long_description = open('README.md').read(),
    zip_safe         = True,
    include_package_data = True,
    install_requires = ['Flask', 'watchdog', 'robotframework'],
    classifiers      = [
        "Development Status :: 0 - Draft",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Robot Framework",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
        ],
    packages         =[
        'rfbench',
        ],
    scripts          =[],
    entry_points={
        'console_scripts': [
            "rfbench = rfbench.__main__:main"
        ]
    }
)
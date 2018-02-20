from setuptools import setup
setup(
        name='alpharank',
        packages=['alpharank'],
        include_package_data=True,
        install_requires=[
            'alpharank',
            ],
        setup_requires=[
            'pytest-runner',
            ],
        tests_require=[
            'pytest',
            ],
        )

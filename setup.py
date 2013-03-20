from setuptools import Command, setup, find_packages

setup(
        name='mobiledetector',
        version='0.0.2',
        url='http://github.com/lojack/mobiledetector',
        license='BSD',
        author='Robert Clark',
        author_email='robert@bablmedia.com',
        packages=['mobiledetector'],
        test_suite='mobiledetector.tests',
        include_package_data=True
)

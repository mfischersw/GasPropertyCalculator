from setuptools import setup, find_packages


setup(
    name='gaspropertycalculator',
    version='0.0.2',
    description='GasPropertyCalculator',
    long_description='GasPropertyCalculator',
    author='Michael Fischer',
    author_email='mfischer.sw@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7, <4',
    entry_points={
        'console_scripts': [
            'gaspropertycalculator=gaspropertycalculator:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/mfischersw/GasPropertyCalculator/',
    }
)

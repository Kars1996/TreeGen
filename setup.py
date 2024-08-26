from setuptools import setup, find_packages

setup(
    name='tree',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'to-tree=tree.tree:main',
        ],
    },
)

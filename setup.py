from setuptools import setup, find_packages

setup(
    name="gov-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.:
        # 'requests',
    ],
    entry_points={
        'console_scripts': [
            'gov-cli = gov_cli.__main__:main',
        ],
    },
    author="Sudip Bhattarai",
    author_email="sudip@sireto.io",
    description="cardano-cli ",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/cardanoapi/gov-cli",  # Update with your project's URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
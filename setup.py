from setuptools import setup, find_packages

setup(
    name='soccer-penalty-detection',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        # add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'detect-penalties = soccer_penalty_detection.main:main'
        ]
    },
    author='ul611',
    author_email='ul7610@pm.me',
    description='A package for detecting penalties in soccer games',
    long_description='This package provides computer vision algorithms for detecting when a penalty is being taken in soccer games, as well as tools for collecting statistics about the penalty kick.',
    url='https://github.com/your-username/soccer-penalty-detection',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

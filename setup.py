from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lcmto',
      version='0.1',
      description='LCM Decoding tools',
      url='http://tbd',
      author='Eric Martin',
      author_email='emartin@mbari.org',
      license='MIT',
      packages=['lcmto'],
      install_requires=['lcm', 'pandas'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='sam-template-creator',
      version='0.1',
      description='Creates a SAM template for a given project',
      long_description=long_description,
      url='https://github.com/VanOvermeire/sam-template-creator',
      author='Sam Van Overmeire',
      author_email='sam.van.overmeire@hotmail.com',
      license='MIT',
      install_requires=[
          'ruamel.yaml >= 0.15.89'
      ],
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      entry_points={
            'console_scripts': ['template-creator=template_creator.command_line:main'],
      },
      zip_safe=False)

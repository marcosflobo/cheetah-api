from setuptools import setup, find_packages


with open('README.rst') as f:
      readme = f.read()

with open('LICENSE') as f:
      license_content = f.read()

setup(name='cheetah-api',
      version='0.1.0',
      description='API for Cheetah project',
      long_description=readme,
      url='https://github.com/marcosflobo/cheetah-api',
      author='Marcos F. Lobo',
      author_email='marcos.lobo@nexthink.com',
      license=license_content,
      packages=find_packages(exclude=('tests', 'docs'))
      )

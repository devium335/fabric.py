from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.10',
  'Natural Language :: English',
  'Topic :: Games/Entertainment'
]
 
setup(
  name='fabric.py',
  version='0.0.1',
  description='Create Fabric Minecraft Mods with Python',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='',  
  author='Devium',
  author_email='devium335@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='util', 
  packages=find_packages(),
  install_requires=[''] 
)

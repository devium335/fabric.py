#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
	name="fabricpy",
	version="0.1.0-alpha",
	description="A Python library to create Fabric Minecraft mods in Python.",
	author="Daniel Korkin",
	author_email="daniel.d.korkin@gmail.com",
	url="https://github.com/danielkorkin/fabricpy",
	packages=find_packages(),
	include_package_data=True,
	install_requires=[],
	entry_points={
		"console_scripts": [
			"fabricpy = fabricpy.cli:main",
		],
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
	python_requires=">=3.7",
)

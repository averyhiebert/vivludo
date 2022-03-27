from setuptools import setup

with open("README.md","r") as f:
    long_description = f.read()

setup(name="vivludo",
      version="0.0.2",
      description="A cellular automaton library.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Avery Hiebert",
      author_email="averyhiebert@gmail.com",
      license="MIT",
      packages=["vivludo"],
      url="https://github.com/averyhiebert/vivludo",
      install_requires=[
        "numpy",
        "scipy",
        "imageio"
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.5')

from distutils.core import setup  # pylint: disable=deprecated-module

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pywykop3",
    packages=["pywykop3"],
    version="0.3",
    license="MIT",
    description="Wykop v2 REST API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mateusz Rynkiewicz",
    author_email="rynkiewiczmate@gmail.com",
    url="https://github.com/KaiserMovet/pywykop3",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",
    keywords=["WYKOP"],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)

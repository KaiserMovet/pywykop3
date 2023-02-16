from distutils.core import setup  # pylint: disable=deprecated-module

setup(
    name="pywykop3",
    packages=["pywykop3"],
    version="0.2",
    license="MIT",
    description="Wykop v2 REST API Client",
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

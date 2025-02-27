from setuptools import setup, find_packages

setup(
    name="pca-reports",
    version="0.0.1",
    author="Dave Redmin",
    author_email="david.redmin@trio.dhs.gov",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["bin/pca-report", "bin/pca-template-preview"],
    # url='http://pypi.python.org/pypi/cyhy/',
    license="LICENSE",
    description="Reporting for Phishing Campaign Assessment",
    long_description=open("README.md").read(),
    install_requires=[
        "pymongo >= 3.4",
        "python-dateutil >= 2.2",
        "pymodm >= 0.4.0",
        "pycrypto >= 2.6",
        "docopt >= 0.6.2",
        "PyYAML >= 3.0",
        "pystache >= 0.5.4",
    ],
    extras_require={"dev": ["pytest", "ipython >= 7.0"],},
)

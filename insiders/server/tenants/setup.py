from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.tenants",
    version="2022.10",
    description="Multi-carrier shipping API muti-tenant module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="Karrio Enterprise",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "karrio.server.core",
        "django-tenants",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)

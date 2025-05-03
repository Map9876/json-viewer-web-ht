from setuptools import setup, find_packages

setup(
    name="web-json",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.25.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A web-based JSON viewer for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/web-json",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "web_json": ["templates/*.html"],
    },
)
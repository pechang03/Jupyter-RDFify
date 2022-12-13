import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupyter-rdfify",
    version="1.0.2",
    author="Lars Pieschel & Md. Rezaul Karim",
    author_email="rezaul.karim@rwth-aachen.de",
    description="IPython Extension for semantic web technology support (Turtle, SPARQL, ShEx, SHACL, etc.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AwesomeDeepAI/Jupyter-RDFify",
    packages=setuptools.find_packages(),
    install_requires=[
        "rdflib~=5.0",
        "ipython>=7.0.0",
        "graphviz",
        "sparqlwrapper>=1.8.5",
        "sparqlslurper~=0.4",
        "PyShEx",
        "pyshacl",
        "owlrl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: IPython",
    ],
    python_requires='>=3.6',
)

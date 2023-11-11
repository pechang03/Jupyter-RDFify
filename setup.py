import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupyter-rdfify",
    version="1.1.0",
    author="Lars Pieschel & Md. Rezaul Karim",
    author_email="rezaul.karim@rwth-aachen.de",
    description="IPython Extension for semantic web technology support (Turtle, SPARQL, ShEx, SHACL, etc.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AwesomeDeepAI/Jupyter-RDFify",
    packages=setuptools.find_packages(),
    install_requires=[
        "rdflib>=6.2",
        "ipython>=7.3.0",
        "graphviz",
        "SPARQLWrapper>=2.0.0",
        "sparqlslurper>=0.5.1",
        "PyShEx>=0.8.1",
        "pyshacl>=0.20.0",
        "owlrl>=6.0.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: IPython",
    ],
    python_requires='>=3.7',
)
#    install_requires=[
##        "rdflib==6.2.0",
#        "jsonasobj==1.3.1",
#        "ipython>=7.3",
#        "graphviz==0.20.1",
#        "SPARQLWrapper==2.0.0",
#        "CFGraph==0.2.1",
#        "chardet==5.1.0",
#        "charset-normalizer==2.1.1",
#        "sparqlslurper==0.5.1",
#        "PyShEx==0.8.1",
#        "PyShExC==0.9.1",
#        "html5lib==1.1",
#        "pyshacl==0.20.0",
#        "rdflib-shim==1.0.3",
#        "requests==2.28.1",
#        "ShExJSG==0.8.2",
#        "prettytable==2.5.0",
#        "urllib3==1.26.13",
#        "owlrl==6.0.2",
#        "webencodings==0.5.1",
##        "pyzmq==19.0.2",
#        "pyparsing==3.0.9",
#        "PyJSG==0.11.10",
#        "prettytable==2.5.0"
#    ],

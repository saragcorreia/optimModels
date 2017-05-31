#!/bin/bash
# http://www.sphinx-doc.org/en/stable/tutorial.html 
# mkdir doc  
# cd doc
# sphinx-quickstart .. activate autodoc
# configure conf.py  

#remove old html files
rm -rf _build/*

#get api documentation from source code
sphinx-apidoc -f -o api/ ../src/optimModels

# build html pages
make html
    

#!/usr/bin/perl
`curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py`;
`curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py`;
`python ez_setup.py`;
`python get-pip.py`;
`pip install nltk`;
`pip install colorama`;

`python -m nltk.downloader stopwords`;
`python -m nltk.downloader wordnet`;
`python -m nltk.downloader punkt`;


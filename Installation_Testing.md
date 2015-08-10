# Introduction #

Fuxi is currently developed and supported for Python version 2.6.1 and lower.  Later versions of Python may work with FuXi.

The simplest way to install FuXi and its dependencies is using [pip](http://www.pip-installer.org/en/latest/) in this way (after [installing it](http://www.pip-installer.org/en/latest/installing.html#python-os-support))

```
pip install http://cheeseshop.python.org/packages/source/p/pyparsing/pyparsing-1.5.5.tar.gz
pip install https://fuxi.googlecode.com/hg/layercake-python.tar.bz2
pip install https://pypi.python.org/packages/source/F/FuXi/FuXi-1.4.1.production.tar.gz
```

# Details #

To build FuXi from the latest version in the mercurial repository using pip, follow these steps:

```
pip install http://cheeseshop.python.org/packages/source/p/pyparsing/pyparsing-1.5.5.tar.gz
pip install https://fuxi.googlecode.com/hg/layercake-python.tar.bz2
hg clone https://chimezie@code.google.com/p/fuxi/ 
pip install fuxi/
```


# Testing and Maintenance #

To verify FuXi installation and functioning, run some tests.  A good place to start is with the standalone unit tests found under `fuxi/test`.  These can be executed individually at the command line.

The module `testOWL.py` requires some manual setup to provide useful results.  Refer to `OWL-TESTS.txt` in `/fuxi/test/OWL` for instructions to download the current W3C OWL test battery.  Unzip that file and move its folders directly beneath the `/fuxi/test/OWL` folder.  At this point you can invoke the battery by executing testOWL at the command line.  By default testOWL runs the battery using the `gms` inference strategy, but `sld` and `bfp` can alternatively be specified using the `--strategy` flag.
Besides standalone unit tests, FuXi embeds unit tests and/or doctests in most production modules.  These can typically be invoked at the command line (as "test mains").

You also can invoke all tests--standalone and embedded, unittest and doctest--by running  `/fuxi/test/suite.py`.  The `--variants` switch with this command causes testOWL to run with each of the strategies gms, sld and bfp .

FuXi may be released with some tests in error.  Consult the release notes for further information.  Also, refer to the [issues list](http://code.google.com/p/fuxi/issues/list?thanks=12&ts=1277984968) for outstanding maintenance and enhancement requests.
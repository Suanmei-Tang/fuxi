

# Introduction #

FuXi comes bundled with harnesses for running various external (mostly W3C tests):

  * OWL tests ([test/OWL/](http://code.google.com/p/fuxi/source/browse/test/OWL/))
  * SPARQL 1.1 Entailment Regime tests ([test/SPARQL/](http://code.google.com/p/fuxi/source/browse/test/SPARQL/))

# OWL tests #

The test harness for the OWL tests is [test/testOWL.py](http://code.google.com/p/fuxi/source/browse/test/testOWL.py).  It requires the OWL tests themselves and they can be downloaded [here](http://www.w3.org/2002/03owlt/approved.zip) and unzipped into **test/OWL**:

```
$ pwd
[...]/test/OWL
$ wget http://www.w3.org/2002/03owlt/approved.zip
[...]
$ unzip approved.zip
```

Then it can be run from the **test/** directory producing results similar to what you see below (with different runtimes, of course):

```
$ pwd
[...]test
$ python testOWL.py 
[...]
{'OWL/AllDifferent/Manifest001.rdf': '7.59289288521 seconds',
 'OWL/FunctionalProperty/Manifest003.rdf': '256.750106812 milli seconds',
 'OWL/FunctionalProperty/Manifest004.rdf': '531.212091446 milli seconds',
 'OWL/InverseFunctionalProperty/Manifest003.rdf': '261.646032333 milli seconds',
 'OWL/InverseFunctionalProperty/Manifest004.rdf': '580.085039139 milli seconds',
 'OWL/SymmetricProperty/Manifest001.rdf': '126.343011856 milli seconds',
 'OWL/TransitiveProperty/Manifest001.rdf': '150.070905685 milli seconds',
 'OWL/allValuesFrom/Manifest001.rdf': '67.7130222321 milli seconds',
 'OWL/complementOf/Manifest001.rdf': '145.536899567 milli seconds',
 'OWL/differentFrom/Manifest001.rdf': '354.184150696 milli seconds',
 'OWL/differentFrom/Manifest002.rdf': '7.03669381142 seconds',
 'OWL/disjointWith/Manifest001.rdf': '368.032932281 milli seconds',
 'OWL/disjointWith/Manifest002.rdf': '339.851856232 milli seconds',
 'OWL/distinctMembers/Manifest001.rdf': '6.9694519043 seconds',
 'OWL/intersectionOf/Manifest001.rdf': '710.019111633 milli seconds',
 'OWL/inverseOf/Manifest001.rdf': '88.1650447845 milli seconds',
 'OWL/unionOf/Manifest001.rdf': '64.8121833801 milli seconds'}
ok

----------------------------------------------------------------------
Ran 1 test in 29.172s

```

It can also be run with the --groundQuery option to get a similar set of results:
```
$ python testOWL.py --groundQuery
[...]
{'OWL/AllDifferent/Manifest001.rdf': '694.902896881 milli seconds',
 'OWL/FunctionalProperty/Manifest003.rdf': '385.773897171 milli seconds',
 'OWL/FunctionalProperty/Manifest004.rdf': '456.007003784 milli seconds',
 'OWL/InverseFunctionalProperty/Manifest003.rdf': '227.980136871 milli seconds',
 'OWL/InverseFunctionalProperty/Manifest004.rdf': '752.804994583 milli seconds',
 'OWL/SymmetricProperty/Manifest001.rdf': '88.9918804169 milli seconds',
 'OWL/TransitiveProperty/Manifest001.rdf': '497.193098068 milli seconds',
 'OWL/allValuesFrom/Manifest001.rdf': '44.2929267883 milli seconds',
 'OWL/complementOf/Manifest001.rdf': '74.9800205231 milli seconds',
 'OWL/differentFrom/Manifest001.rdf': '259.169101715 milli seconds',
 'OWL/differentFrom/Manifest002.rdf': '614.264011383 milli seconds',
 'OWL/disjointWith/Manifest001.rdf': '219.238042831 milli seconds',
 'OWL/disjointWith/Manifest002.rdf': '246.393918991 milli seconds',
 'OWL/distinctMembers/Manifest001.rdf': '904.661893845 milli seconds',
 'OWL/intersectionOf/Manifest001.rdf': '257.449150085 milli seconds',
 'OWL/inverseOf/Manifest001.rdf': '104.188203812 milli seconds',
 'OWL/unionOf/Manifest001.rdf': '70.4469680786 milli seconds'}
ok

----------------------------------------------------------------------
Ran 1 test in 8.068s
```

# SPARQL 1.1 Entailment tests #

The test harness for the SPARQL 1.1 Entailment tests is [test/SPARQL/test.py](http://code.google.com/p/fuxi/source/browse/test/SPARQL/test.py).  It requires the _entailment_  directory from the SPARQL 1.1 WG [test area](http://www.w3.org/2009/sparql/docs/tests/), which can downloaded from [here](http://www.w3.org/2009/sparql/docs/tests/sparql11-test-suite-20121023.tar.gz)

It can be unarchived somewhere else and the _entailment_ directory can be linked into the [test/SPARQL/W3C](http://code.google.com/p/fuxi/source/browse/test/SPARQL/W3C) directory.

Then it can be run from the **test/** directory producing results similar to what you see below (with different runtimes, of course):

```
$ pwd
[...]test
$ dir SPARQL/W3C/entailment
[...] SPARQL/W3C/entailment -> [...]tests/data-sparql11/entailment
$ python SPARQL/test.py
test_bind01 (__main__.TestSequence) ... ok
test_bind02 (__main__.TestSequence) ... ok
test_bind03 (__main__.TestSequence) ... ok
test_bind04 (__main__.TestSequence) ... ok
test_bind05 (__main__.TestSequence) ... ok
test_bind06 (__main__.TestSequence) ... ok
test_bind07 (__main__.TestSequence) ... ok
test_bind08 (__main__.TestSequence) ... ok
[...]
test_paper-sparqldl-Q1-rdfs FAIL
test_paper-sparqldl-Q4 ERROR
[...]
test_rdf03 (__main__.TestSequence) ... FAIL
[...]
test_rdfs12 (__main__.TestSequence) ... FAIL
[...]

Ran 44 tests in 267.616s

FAILED (failures=9, errors=2)
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix earl: <http://www.w3.org/ns/earl#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix myfoaf: <http://metacognition.info/public_rdf/n3/foaf.ttl#> .
@prefix software: <http://metacognition.info/software/> .
@prefix test: <http://www.w3.org/2009/sparql/docs/tests/data-sparql11/entailment/manifest#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

software:fuxi a doap:Project;
    doap:maintainer myfoaf:chime;
    doap:release [ a doap:Version;
            doap:name "1.4" ];
    foaf:homepage <http://code.google.com/p/fuxi/> .
[...]
```
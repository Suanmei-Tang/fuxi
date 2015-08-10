The general idea is to leverage the efficiency of the **RETE-UL** algorithm and a logic programming meta-interpreter  as the 'engine' for a Python-based open-source expert system for the semantic web, built on Python.  It is inspired by its predecessors: [cwm](http://www.w3.org/2000/10/swap/doc/CwmInstall), [pychinko - Rete-based RDF friendly rule engine](http://www.mindswap.org/~katz/pychinko/), and [euler - Euler proof mechanism](http://www.agfa.com/w3c/euler/).

## Prerequisites ##

Fuxi requires [layercake](http://code.google.com/p/python-dlp/wiki/LayerCakePythonDivergence) (preferred) and it is not compatible with rdflib 3.+ or 4+.  See the install documentation (below)

## Installation ##

There is a [wiki](http://code.google.com/p/fuxi/wiki/Installation_Testing) with instructions on installing FuXi for a first-time user or developer.

## Testing ##

There is a [document](Testing.md) that covers testing

## Documentation ##

There is a _hello-world_  [Tutorial](http://code.google.com/p/fuxi/wiki/Tutorial).  API  documentation is [here](http://fuxi.googlecode.com/hg/documentation/html/index.html).

## Semantics ##

**New** FuXi has a sketched out formal semantics (based on classic Logic Programming), see: FuXiSemantics

References:
  * [Description Logic Programs: Combining Logic Programs with Description Logic](http://www.cs.man.ac.uk/~horrocks/Publications/download/2003/p117-grosof.pdf)
  * [A Realistic Architecture for the Semantic Web](http://www.inf.unibz.it/~jdebruijn/publications/msa-ruleml05.pdf)
  * [SWRL: A Semantic Web Rule Language Combining OWL and RuleML](http://www.w3.org/Submission/SWRL/)
  * [W3C RIF WG Core (Draft)](http://www.w3.org/2005/rules/wg/wiki/Core)
  * [Completeness, decidability and complexity of entailment for RDF Schema and a semantic extension involving the OWL vocabulary](http://www.websemanticsjournal.org/ps/pub/2005-15)
  * [Production Matching for Large Learning Systems](http://reports-archive.adm.cs.cmu.edu/anon/1995/CMU-CS-95-113.pdf)
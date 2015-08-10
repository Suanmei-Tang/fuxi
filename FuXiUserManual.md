

# Introduction #

FuXi (pronounced foo-shee) is a bi-directional (forward or bottom up methods and backward or top-down reasoning methods) logical reasoning system for the Semantic Web and Python.  FuXi was originally meant as a Python swiss army knife for all things semantic web related.  It works as a companion to RDFLib, a Python library for working with RDF.

# The Primary Modules #

An overview of the top-level modules in FuXi serves as an introduction to the general features of FuXi.  The FuXi libraries are divided as follows:

  * FuXi.Horn
  * FuXi.Syntax
  * FuXi.DLP
  * FuXi.LP
  * FuXi.Rete
  * FuXi.SPARQL

## FuXi.Horn ##

The Horn module was originally meant as a reference implementation of the W3C's Rule Interchange Format Basic Logic Dialect ( work in progress ) but eventually evolved into a Pythonic API for managing an abstract Logic Programming syntax.  This module is heavily used by both the DLP and Rete modules for (respectively) creating the rulesets converted from OWL RDF expressions and creating a Horn ruleset from a parsed Notation 3 graph.

The Horn module includes Python classes for each of the major components of the RIF BLD abstract syntax ([EBNF Grammar for the Presentation Syntax of RIF-BLD](http://www.w3.org/TR/rif-bld/#EBNF_Grammar_for_the_Presentation_Syntax_of_RIF-BLD)):

  * FuXi.Horn.HornRules.Ruleset
  * FuXi.Horn.HornRules.Rule
  * FuXi.Horn.HornRules.Clause
  * FuXi.Horn.PositiveConditions.Condition
  * FuXi.Horn.PositiveConditions.And
  * FuXi.Horn.PositiveConditions.Or
  * FuXi.Horn.PositiveConditions.Uniterm
  * ... etc ..

Horn rulesets can be built from the ground up by instantiating the objects piecemeal:

> Example: {?C rdfs:subClassOf ?SC. ?M a ?C} => {?M a ?SC}.

```
>>> clause = Clause(And([Uniterm(RDFS.subClassOf,[Variable('C'),Variable('SC')]),
...                      Uniterm(RDF.type,[Variable('M'),Variable('C')])]),
...                 Uniterm(RDF.type,[Variable('M'),Variable('SC')]))
>>> Rule(clause,[Variable('M'),Variable('SC'),Variable('C')])
Forall ?M ?SC ?C ( ?SC(?M) :- And( rdfs:subClassOf(?C ?SC) ?C(?M) ) )

>>> And([Uniterm(RDF.type,[RDFS.comment,RDF.Property]),
...      Uniterm(RDF.type,[OWL.Class,RDFS.Class])])
And( rdf:Property(rdfs:comment) rdfs:Class(owl:Class) )

>>> Exists(formula=Or([Uniterm(RDF.type,[RDFS.comment,RDF.Property]),
...                    Uniterm(RDF.type,[OWL.Class,RDFS.Class])]),
...        declare=[Variable('X'),Variable('Y')])
Exists ?X ?Y ( Or( rdf:Property(rdfs:comment) rdfs:Class(owl:Class) ) )

>>> And([Uniterm(RDF.type,[RDFS.comment,RDF.Property]),
...      Uniterm(RDF.type,[OWL.Class,RDFS.Class])]).n3()
u'rdfs:comment a rdf:Property .\\n owl:Class a rdfs:Class'
```

RIF BLD objects can also be constructed by parsing a Notation 3 document like so:

```
>>> from FuXi.Horn.HornRules import HornFromN3
>>> rs=HornFromN3('http://www.agfa.com/w3c/euler/rdfs-rules.n3')
>>> for r in rs: print r
... 
Forall ?P ?S ?O ( rdf:Property(?P) :- ?P(?S ?O) )
Forall ?P ?C ?S ?O ( ?C(?S) :- And( rdfs:domain(?P ?C) ?P(?S ?O) ) )
Forall ?P ?C ?S ?O ( ?C(?O) :- And( rdfs:range(?P ?C) ?P(?S ?O) ) )
Forall ?P ?S ?O ( rdfs:Resource(?S) :- ?P(?S ?O) )
Forall ?P ?S ?O ( rdfs:Resource(?O) :- ?P(?S ?O) )
Forall ?Q ?P ?R ( rdfs:subPropertyOf(?P ?R) :- And( rdfs:subPropertyOf(?Q ?R) rdfs:subPropertyOf(?P ?Q) ) )
Forall ?P ?S ?R ?O ( ?R(?S ?O) :- And( rdfs:subPropertyOf(?P ?R) ?P(?S ?O) ) )
Forall ?C ( rdfs:subClassOf(?C rdfs:Resource) :- rdfs:Class(?C) )
Forall ?A ?S ?B ( ?B(?S) :- And( rdfs:subClassOf(?A ?B) ?A(?S) ) )
Forall ?A ?C ?B ( rdfs:subClassOf(?A ?C) :- And( rdfs:subClassOf(?B ?C) rdfs:subClassOf(?A ?B) ) )
Forall ?X ( rdfs:subPropertyOf(?X rdfs:member) :- rdfs:ContainerMembershipProperty(?X) )
Forall ?X ( rdfs:subClassOf(?X rdfs:Literal) :- rdfs:Datatype(?X) )
Forall ?S ( And(  ) :- And( rdf:XMLLiteral(?S) e:clashesWith(?S rdf:XMLLiteral) ) )
```

### Serialization ###

From the example(s) above, instantiated RIF BLD objects can be serialized in one of two ways: as human-readable RIF syntax or as Notation 3.  The former serialization is built in by overriding the repr class method; a standard mechanism used in order to ".. compute the ``official'' string representation of an object.".  The latter serialization can be achieved by invoking the _n3_ method on any RIF BLD Python object.

The Horn module simplifies the process of serializing appropriate QNames (or [curies](http://www.w3.org/TR/curie/)) for the URIs associated with Uniterms.  Uniterms can be thought of as the RIF equivalent of RDF statements or Logic Programming _atoms_.  In order to associate a namespace mapping dictionary (a Python dictionary of prefixes to rdflib.URIRef instances of the corresponding fully qualified namespace URI), a Uniterm constructor can be invoked and passed such a dictionary via the _newNss_ keyword argument

### Parsing RIF Core ###

The Horn module also provides APIs for parsing rules from either the [XML serialization](http://www.w3.org/TR/rif-core/#XML_Serialization_Syntax_for_RIF-Core) or [RIF in RDF](http://www.w3.org/TR/rif-in-rdf/) syntaxes for RIF Core.  In particular, the RIFCoreParser class in the FuXi.Horn.RIFCore module provides this capability:

```
>>> from FuXi.Horn.RIFCore import RIFCoreParser
>>> from pprint import pprint
>>> rif_document = ''http://www.w3.org/2005/rules/test/repository/tc/Frames/Frames-premise.rif'
>>> rif_parser = RIFCoreParser(location=rif_document,debug=True)
RIF document URL provided  http://www.w3.org/2005/rules/test/repository/tc/Frames/Frames-premise.rif
Extracted rules from RIF XML format
>>> rs = rif_parser.getRuleset()
>>> pprint(rs)
[Forall ?Customer ( ns1:discount(?Customer 10) :- ns1:status(?Customer "gold"^^<http://www.w3.org/2001/XMLSchema#string>) ),
 Forall ?Customer ( ns1:discount(?Customer 5) :- ns1:status(?Customer "silver"^^<http://www.w3.org/2001/XMLSchema#string>) )]
```

It returns a list of FuXi.Horn.HornRules.Rule instances

Note that this parser introduces a dependency on the [Amara 2.0](http://wiki.xml3k.org/Amara/Install) Python library.

### Rule Safety ###

The [safeness criteria](http://www.w3.org/TR/rif-core/#Safeness_Criteria) of RIF-Core is enforced by the library that manages RIF document logically as Python objects.  Every rule has a **isSafe** method that returns a boolean indicating whether or not it is safe and can be used to enforce safety for the purpose of ensuring (for example) that the use of the RETE-UL network to forward-propagate a ruleset will terminate and not run forever.

The FuXi.Horn module has three top-level flags used in the command-line, the HornFromDL method described below, and the setupDescriptionLogicProgramming method on networks:

  * FuXi.Horn.DATALOG\_SAFETY\_NONE
  * FuXi.Horn.DATALOG\_SAFETY\_STRICT
  * FuXi.Horn.DATALOG\_SAFETY\_LOOSE

The first will not do any safety checking, the second will through a SyntaxError exception if any unsafe rules are extracted from description logic formulae, and the third will simply skip any unsafe rules (ensuring any returned ruleset is safe)

## FuXi.Syntax ##

The FuXi.Syntax module incorporates the InfixOwl library (see the linked Wiki for more information).

## FuXi.Rete ##

At the heart of the python-dlp framework is an implementation of most of the RETE-UL algorithms outlined in the PhD thesis (1995) of Robert Doorenbos:

> Production Matching for Large Learning Systems.

Robert's thesis describes a modification of the original Rete algorithm that (amongst other things) limits the fact syntax (referred to as Working Memory Elements) to 3-item tuples (which corresponds quite nicely with the RDF abstract syntax). The thesis also describes methods for using hash tables to improve efficiency of alpha nodes and beta nodes.

Instances of the FuXi.Rete.ReteNetwork class are RETE-UL networks.  So, to programmatically build a RETE-UL network, a developer would write:
```
>>> from rdflib.Graph import Graph
>>> from FuXi.Rete.RuleStore import SetupRuleStore
>>> rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True,additionalBuiltins=...)
Time to build production rule (RDFLib): 0.000193119049072 seconds
>>> closureDeltaGraph=Graph()
>>> network.inferredFacts = closureDeltaGraph
>>> network
<Network: 0 rules, 0 nodes, 0 tokens in working memory, 0 inferred tokens>
```

First, a rule store, a rule graph, and a RETE-UL decision network are built using the **SetupRuleStore** method.  The additionalBuiltins argument can be used to pass in an (optional) dictionary for user-specified built-ins.  For a list of 'standard' CWM builtins, see: [CWM Builtins](http://www.w3.org/2000/10/swap/doc/CwmBuiltins).  Note, the RETE-UL implementation doesn't support denoting (or calculating) built-ins.  It only supports built-in predicates that compare existing values.  So, for example math:product is not supported, but math:lessThan is.  The additionalBuiltins keyword argument expects a dictionary where the key is an RDFLib URIRef instance (the URI of the built-in predicate) and the value is a Python callable which should take two arguments as input and return a boolean value that corresponds to the expected semantics for the custom built-in predicate.

Then, a graph is created where the inferred RDF statements will be stored (the entailed graph) and attached to the network.
If a closure delta graph is not provided, one will be created.  In either case, the _inferredFacts_ attribute of the network will be set to the closure delta graph.

This method also takes a n3Stream keyword argument that is a stream whose content is an N3 document to use as the original rules for the network.  A network can also be explicitly built from a ruleset using the **buildNetworkFromClause** method for _ReteNetwork_ instances.  So, the  **HornFromN3** method can be used with **SetupRuleStore** to build a decision network from a N3 document more concisely:

```
>>> for rule in HornFromN3('http://www.agfa.com/w3c/euler/rdfs-rules.n3'): network.buildNetworkFromClause(rule)
... 
__main__:1: SyntaxWarning: Integrity constraints (rules with empty heads) are not supported!: Forall ?S ( And(  ) :- And( rdf:XMLLiteral(?S) e:clashesWith(?S rdf:XMLLiteral) ) )
>>> network
<Network: 10 rules, 28 nodes, 0 tokens in working memory, 0 inferred tokens>
>>> network.rules
set([...])

```

From here, RDF facts can be fed into the network in order to calculate the inferred RDF statements and add them to the closure delta graph:

```
from FuXi.Rete.Util import generateTokenSet

network.feedFactsToAdd(generateTokenSet(someRDFGraph))
```

Here, _someRDFGraph_ is an RDFLib Graph instance that contains the RDF facts to pass into the network.  At this point, _network.inferredFacts_ should consist of the RDF statements that can be inferred from the given ruleset and initial RDF facts.

## FuXi.Rete.Magic ##

This module is where the [Sideways Information Passing](http://code.google.com/p/fuxi/wiki/Overview#Sideways_Information_Passing) reasoning capabilities are implemented.  It provides a core method shown below:

```
def MagicSetTransformation(
  factGraph,
  rules,
  GOALS,
  derivedPreds=None,
  strictCheck = ...,
  noMagic=[],
  defaultPredicates=None)
```

> that takes as input:

  * A list of derived predicates (if an empty list is provided this indicates the user wants the method to determine the list of derived predicates by inspecting the factGraph and update the given list in place): **derivedPreds**
  * The fact graph that we want to ask the query against (used to find derived predicates if an empty list is given): **factGraph**
  * A list of 3-item tuples each representing a SPARQL Basic Graph Pattern: **GOALS**
  * A set of [safe](http://www.w3.org/TR/rif-core/#Safeness_Criteria) RIF-Core rules: **rules**
  * Additional parameters described below

It re-writes the rules into a more optimal form.  The rules are modified so that they only search the proof space relevant for the query posed by the user.  For most classes of problems, when the re-written rules are evaluated will be evaluated just as efficiently via forward-chaining as it would via backwards chaining (using a Prolog-like mechanism, for instance).  So, the RETE-UL network can be used to evaluate queries (expressed as SPARQL BGPs) via forward-propagation or using the backward chaining capabilities

The method returns a generator over the re-written rules and updates the given factGraph, adding to the adorned program via the  **.adornedProgram** attribute.  An adorned program is a ruleset where the literals have been _adorned_ with information about how variable bindings make their way from a goal through the series of rules that are applicable and is used to create the re-written ruleset and also used by the backward chainer (see below).

The MagicSetTransformation  method requires some input about which predicates are derived (it assumes the others are base predicates).  For more information on this distinction, see [Base and Derived Predicates](http://code.google.com/p/fuxi/wiki/Overview#Base_and_Derived_Predicates).  In addition, the method also takes a flag that takes 1 of 4 values (the **strictCheck** argument) determining how strictly to adhere to a clean separation between the two:

  1. FuXi.Rete.Magic.DDL\_STRICTNESS\_LOOSE
  1. FuXi.Rete.Magic.DDL\_STRICTNESS\_HARSH
  1. FuXi.Rete.Magic.DDL\_STRICTNESS\_FALLBACK\_BASE
  1. FuXi.Rete.Magic.DDL\_STRICTNESS\_FALLBACK\_DERIVED

Finally, it also takes a **defaultPredicates** argument that is a two item tuple where the first item is a list of _default_ base predicates and the second is a list of _default_ derived predicates.  These are meant to be used with the last two strictness flags.

When the first flag is used, this indicates that the rule-rewriting state should not check to ensure that predicates are not both base and derived.  The second flag indicates that an exception will be raised if any predicate is found to be both.  The third and forth with cause a clashing predicate to be labeled as either a base or derived predicate respectively (i.e., the default fallback if there is a clash).  This rule will be overridden by the user-provided list of default base and derived predicates.  So, for example, if the user indicates the third flag (fallback to base) but a clashing predicate is in the provided list of derived predicates, it will be marked as a derived predicate.

### IdentifyDerivedPredicates ###

A helper function which takes a [DDL](http://code.google.com/p/fuxi/wiki/DataDescriptionLanguage) graph, an OWL graph (the TBox), and a ruleset and returns the set of derived predicates.  See the [signature](http://code.google.com/p/fuxi/source/browse/lib/Rete/Magic.py?spec=svna57d85d65ec920ad247f8bbb6fbfd85565031cd3&r=a57d85d65ec920ad247f8bbb6fbfd85565031cd3#710) of the method.

## FuXi.SPARQL ##

The implementation for a BackwardsChainingStore.  A backwards chaining store can be setup this way:

```
            from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore
            topDownStore=TopDownSPARQLEntailingStore(
                                        factGraph.store,
                                        factGraph,
                                        set(dPreds),
                                        rules,
                                        nsBindings=nsMap,
                                        DEBUG=DEBUG) 
            targetGraph = Graph(topDownStore)
            topDownStore.targetGraph = targetGraph 

```

Where **factGraph** is an rdflib graph instance, **dPreds** is a set of URIs each of which is the name of a derived predicate in the IDB, **rules** is a set of clauses that comprise the IDB, and **nsBindings** is a namespace mapping.  At this point, a SPARQL query can be dispatched to targetGraph (via targetGraph.query('... SPARQL ...') using derived predicates and the sip strategy will be used to solve the (high-level) query through a series of query re-writing which produce base queries (i.e., queries only involving base predicates) to evaluate against  factGraph and combine such answers in order to answer the original query.

In this way, a (possibly large) [SQL-based RDFLib backend](http://code.google.com/p/rdflib/wiki/SQL_Backend) can be queried using derived predicates defined by a domain theory expressed as any combination of RIF Core, N3, and/or OWL2-RL such that additional answers that follow from the domain theory will be provided to the query.

## FuXi.Rete.TopDown ##

The _FuXi.Rete.TopDown_ module has since been **deprecated** by the Backwards Fixpoint Procedure ([BFP](http://code.google.com/p/fuxi/wiki/FuXiUserManual#FuXi_.LP)).  See [backward chaining](http://code.google.com/p/fuxi/wiki/Overview#Backward_Chaining_/_Top_Down_Evaluation)

### SPARQL FILTER Templates and Top Down Builtins ###

Building a ruleset with a set of defined builtin implementations (as Python functions) will provide the means to use builtins for forward chained inference via the RETE-UL network.  However, as mentioned [here](http://code.google.com/p/fuxi/wiki/Overview#Builtin_Infrastructure) the backward chaining inference engine can be used to as a kind of semantic query mediator to solve a SPARQL triple pattern (that uses derived predicates) by dispatching and combining answers from a series of intermediate SPARQL queries.  Any builtins in the body (or antecedent) of a rule can be sent along with these queries using an RDF-based templating system that specifies how to convert a builtin function into a SPARQL FILTER expression.

The factGraph given to the SipStrategy method can have attached to it, a mapping from predicates to SPARQL FILTER expressions which are Python string templates that will be substituted with the parameters of the builtin as it is used to solve the original query.  Given a graph such as the example in the overview, we can create and attach the mapping this way:

```
        factGraph.templateMap = \
            dict([(pred,template)
                      for pred,_ignore,template in 
                            builtinTemplateGraph.triples(
                                (None,
                                 TEMPLATES.filterTemplate,
                                 None))])
```

Where _builtinTemplateGraph_ is a graph of the templates.  A SPARQL FILTER template builtin (N3) graph can be specified to the FuXi command-line via the **--builtinTemplates** options (see example below):

#### SPARQL Filter Templates Example ####

```
$ FuXi  --safety=loose --strictness=defaultDerived \
        --idb=owl:sameAs  \
        --why="ASK { ex:subject1 owl:sameAs ex:subject2 }" \
        --debug  \
        --ns=ex=http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#  \
        --pDSemantics --builtinTemplates=http://fuxi.googlecode.com/hg/RuleBuiltinSPARQLTemplates.n3 \
        --dlp http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001.rdf
[..snip..]
Goal/Query:  (rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject1'), rdflib.URIRef('http://www.w3.org/2002/07/owl#sameAs'), rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject2'))
[..snip..]
Inferred triple:  (rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject2'), rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://www.w3.org/2002/07/owl#sameAs_query_fb'))  from  owl:sameAs_query_fb(?T2) :- 
[..snip..]
SELECT ?P ?S ?O {
	<http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject2> ?P ?O .
	?P  a  <http://www.w3.org/2002/07/owl#InverseFunctionalProperty> .
	?S ?P ?O .
	FILTER(?S != <http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject2>)
}-> []
{?O: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#object'),
 ?P: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#prop'),
 ?S: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject1')}
[..snip..]
Inferred triple:  (rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject1'), rdflib.URIRef('http://www.w3.org/2002/07/owl#sameAs'), rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject2'))  
[..snip..]
Reached ground goal. Terminated BFP!
Time to reach answer ground goal answer of True: [...] milli seconds
```

Here the semantics of log:notEqualTo are converted into SPARQL's term comparison methods (!=)

The key query is (re-written with prefix bindings for brevity)

```
PREFIX : <<http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#>
SELECT ?P ?S ?O {
	:subject2 ?P ?O .
	?P  a  owl:InverseFunctionalProperty .
	?S ?P ?O .
	FILTER(?S != :subject2>)
}-> []
{?O: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#object'),
 ?P: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#prop'),
 ?S: rdflib.URIRef('http://www.w3.org/2002/03owlt/InverseFunctionalProperty/premises001#subject1')}
```

This is made possible via:

```
log:notEqualTo  templ:filterTemplate "%s != %s" .
```

In the SPARQL template RDF serialization in the source tree (_[RuleBuiltinSPARQLTemplates.n3](http://code.google.com/p/fuxi/source/browse/RuleBuiltinSPARQLTemplates.n3)_)

## FuXi.DLP ##

This module is a Description Horn Logic implementation as defined by Grosof, B. et.al. ("Description Logic Programs: Combining Logic Programs with
Description Logic" ) in section 4.4.  As such, it implements recursive mapping functions "T", "Th" and "Tb" which result in "custom" (dynamic) rulesets.

For the non logic-inclined, this essentially allows OWL ontologies (or a subset of OWL ontologies) to be automatically converted to a set of rules that exactly capture the semantics of the OWL document.  This mechanism is fundamental to the larger framework that FuXi is a part of (python-dlp).  The premise is two-fold.

First (and most importantly), the ruleset(s) generated from an OWL ontology will be much more tailored to the specific constraints of the ontology than a general-purpose ruleset would.  As such, the inference mechanism will be several orders of magnitude more efficient.

Secondly, tools that are used for authoring OWL ontologies are significantly more mature than those used for authoring Notation 3 rulesets (or any other comparable semantic web rule language).  Using the DLP mechanism, a domain expert can model the semantics of a particular domain using any off-the-shelf OWL editor and generate a corresponding ruleset.

To invoke the DLP implementation, a developer would do the following:

```
from FuXi.Rete.Util import generateTokenSet
from FuXi.DLP.DLNormalization import NormalFormReduction

NormalFormReduction(tBoxGraph)
network.setupDescriptionLogicProgramming(tBoxGraph)
network.feedFactsToAdd(generateTokenSet(tBoxGraph))
network.feedFactsToAdd(generateTokenSet(someRDFGraph))
```

The _setupDescriptionLogicProgramming_ method can be invoked on a ReteNetwork instance, passing in an RDFLib Graph that consists of the OWL assertions that we wish to translate to a ruleset as the only argument.  This method will return a list of RuleSet objects each of which represents a rule that was translated from the OWL assertions.

This method also takes a **safety** keyword that is any of the safety flags described above.

Note, the TBox OWL RDF graph is _normalized_ before using the _setupDescriptionLogicProgramming_  method.  This is necessary in order to handle certain OWL nested axioms.

The following line then sends the OWL RDF assertions through the network.  This is necessary to fully classify the OWL ontology.  Then finally, an RDF graph of facts are sent through the network.  Typically, a user will have an RDF graph with instance-level statements (the [ABox](http://en.wikipedia.org/wiki/ABox)) and an OWL RDF graph that describes the vocabulary terms used in the instance graph (the [TBox](http://en.wikipedia.org/wiki/TBox)).  After following the three steps above, the _network.inferredFacts_ graph will now have all the RDF statements that can be inferred from the combination of the OWL graph and the instance graph.  Note, the DLP algorithm only supports a subset of OWL-DL, so not all OWL graphs will be properly axiomatized.

Finally, a network can be _reset_ via the network.reset() method.  This will _clear_ the RETE-UL network, and is useful when you want to setup a network once from an OWL graph and calculate the closure delta graph for multiple instance graphs from the same ruleset.  After resetting the network, the TBox graph will both need to be sent through the network again, followed by the subsequent instance graph:

```
network.setupDescriptionLogicProgramming(tBoxGraph)
network.feedFactsToAdd(generateTokenSet(tBoxGraph))
network.feedFactsToAdd(generateTokenSet(someRDFGraph1))
network.reset()
network.feedFactsToAdd(generateTokenSet(tBoxGraph))
network.feedFactsToAdd(generateTokenSet(someRDFGraph2))
..etc..
```

Or, consider the use of HornFromDL to do something similar, but more directly:

```
>>> from FuXi.Horn.HornRules import HornFromDL
>>> from rdflib.Graph import Graph
>>> from rdflib.util import first
>>> first([r for r in HornFromDL(Graph().parse('http://www.lehigh.edu/%7Ezhp2/2004/0401/univ-bench.owl')) if not r.isSafe()])
Forall ?X ( Exists _:tCDCSqnL314 ( Course(tCDCSqnL314) ) :- TeachingAssistant(?X) )
```

Here, the first unsafe rule from the Lehigh University Benchmark ontology is printed out.  The rule is unsafe because the existential variable in the rule head does not appear in the body.

We can look at the OWL formulae associated with the TeachingAssistant class to see why its conversion to rules includes an unsafe rule:

```
$ FuXi --class=:TeachingAssistant  --output=man-owl  
http://www.lehigh.edu/%7Ezhp2/2004/0401/univ-bench.owl 
... snip ...
Class: :TeachingAssistant 
    ## A Defined Class (university teaching assistant) ##
    EquivalentTo: :Person that ( :teachingAssistantOf some :Course )
```

## FuXi.LP ##

A backwards fixpoint procedure (BFP) [implementation](http://code.google.com/p/fuxi/source/browse/lib/LP/BackwardFixpointProcedure.py) in Python.

A sound and complete query answering method for recursive databases based on meta-interpretation called Backward Fixpoint Procedure

Uses RETE-UL as the RIF PRD implementation of
a meta-interpreter of an adorned ruleset that builds large, conjunctive (BGPs) SPARQL queries.

Uses the specialized BFP meta-interpretation rules to build a RETE-UL decision
network that is modified to support the propagation of bindings from the evaluate
predicates into a supplimental magic set sip strategy and the generation of subqueries.
The end result is a bottom-up simulation of SLD resolution with complete, sound, and safe
memoization in the face of recursion.

Specialization is applied to the BFP meta-interpreter with respect to the rules of the object program. For each rule of the meta-interpreter that includes a premise referring to a rule of the object program, one specialized version is created for each rule of the object program.

OpenQuery is used with predicate symbols to indicate a query without any bindings provided to the program (disadvantageous for GMS).

The semantics of the evaluate predicate is as follows: in each case, we add entailed evaluate bindings (as high-arity predicates) directly into RETE-UL beta node memories in a circular fashion, propagating their successor.

The Beta Nodes are changed in the following way:

Take a BetaNode (and a BFP rule) that joins values from an evaluate condition with other conditions and replace the alpha node (and memory) used to represent the condition with a pass-thru beta with no parent nodes but whose right memory will be used to add bindings instantiated  from evaluate assertions in the BFP algorithm.

# The Command Line #

Installing FuXi should install a command-line script called: FuXi.  It is meant as a swiss-army knife for all things related to RDF inference, OWL, N3, RIF, etc.. For additional information on using Fuxi as a query mediating
expert system with a KB that uses expressive description logics and horn-clauses in a truth-preserving manner, see TopDownSW .

Below is the use-case driven list of its various operating modes:

```
FuXi [options] factFile1 factFile2 ... factFileN
```

## Input / Output formats and switches ##

The **--input-format** option can be one of the following RDF serialization syntaxes:

  * xml
  * n3
  * trix
  * nt
  * rdfa

This determines the format it assumes the factFiles are written in.  Note, the **--closure** option indicates whether or not to serialize the inferred triples along with the original triples.  Otherwise (the default behavior), only the inferred triples are serialized.

The **--rules** and **--filter** options are used to specify N3 documents to load.  The latter is meant to replicate the behavior of CWM with this option.  The --ruleFacts options will indicate that the rule documents also have facts to accumulate (otherwise only the horn-like N3 rules - N3-Datalog - are extracted)

The **--rules** option loads rules from N3 documents by default but can also load them from RIF Core XML or RIF in  RDF documents via providing a value of 'rif' to the --ruleFormat.

The **--builtins** option points to a Python module (as a filesystem path) with a ADDITIONAL\_FILTERS dictionary from URIRefs to Python callables.  This is the extension point for developer-specified builtins.

The **--output** option determines (depending on the usage mode) what kind of output format to use.  For modes where we want to serialize the inferred RDF statements  and/or the RDF statements of the original fact graph, the following options are relevant:

  * pretty-xml (concise RDF/XML)
  * nt (NTriples)
  * turtle (Turtle)
  * n3 (N3)
  * conflict

The **--sparqlEndpoint** options is used to identify an RDF dataset to query over HTTP.

**--ddlGraph** points to an N3 document describing the IDB and EDB predicate symbols..

The latter options is for whenever the forward-chaining engine is used and will print out information about which rules were fired, how often and information about the terminal nodes for those rules (the variables involved, state information about the RETE network, et..)

_closure_ indicates that the closure graph is serialized (i.e., the graph of the entailed statements that were not in the original graph)

The **--stdin** option indicates that FuXi should parse RDF content from STDIN (useful for piping operations on LINUX/UNIX machines).  **--normalForm** will cause the factGraph to be treated as an OWL2/OWL RDF graph and reduced using certain standard transformations (this is done automatically with the **--dlp** options).

There are additional output values:

  * rif

This writes out the RIF ruleset used for inference - if applicable.

### Namespace Management ###

The **--ns** option can be used to a provide '-' separated prefix to namespace URI reference mapping for general use


### Manchester OWL Output Syntax ###

The man-owl output value writes out the [Manchester OWL syntax](http://www.co-ode.org/resources/reference/manchester_syntax/) representation of the OWL file parsed in from the factFiles.  It can be used with the --normalize options to attempt to determine if the ontology is 'normalized' [[Rector, A. 2003](http://doi.acm.org/10.1145/945645.945664)]

The **--class** and **--property** options can be used to specify (via QNames) classes and properties to serialize via Manchester OWL (see below)

## Description Logic Programming (DLP) ##

As described above, FuXi implements DLP and this capability can be used to extract rules from OWL/OWL2 RL documents.  Note, FuXi currently only supports OWL 1 RDF syntax, so the support for [OWL2 RL](http://www.w3.org/TR/owl2-profiles/#OWL_2_RL) is limited to the extent that the OWL2 RL is [backwards compatible](http://www.w3.org/TR/2009/WD-owl2-overview-20090611/#Relationship_to_OWL_1) with OWL.

The **--dlp** options indicates that either the fact files or any files identified via the **--ontology** option are used as the source of OWL2 RL axioms to convert into the RIF ruleset used for inference

## Rule Safety ##

The **--safety** option is used to set the use of the rule safety flags:

```
  --safety=RULE_SAFETY  Determines how to handle RIF Core safety.  A value of
                        'loose'  means that unsafe rules will be ignored.  A
                        value of 'strict'  will cause a syntax exception upon
                        any unsafe rule.  A value of 'none' (the default) does
                        nothing
```

## Sideways Information Passing (SIP) for SPARQL / OWL / RIF ##

FuXi also has support for efficient backwards and forward chaining to solve the answers to a user-specified query (see: [Sideways Information Passing (SIP)](http://code.google.com/p/fuxi/wiki/Overview#Sideways_Information_Passing)).  This mode can be used via the **--why** option, which takes a SPARQL query that consists only of simple BGP representing the user's query.

It will consider every BGP in the query a _goal_ that is used as input to the magic set algorithm.

The **--edb** and **--idb** options are used to determine the user-specified list of default base and derived predicates, respectively.  See: [Base and Derived Predicates](http://code.google.com/p/fuxi/wiki/Overview#Base_and_Derived_Predicates)

The FuXi will use the Backwards Fixpoint Procedure  evaluation method to solve the given query

There is a **--firstAnswer** which, when used with wither bfp or sld and **--why** will cause only the first goal to be solved, rather than searching the proof space exaustively.

**--builtinTemplates** is the path to an N3 document of mappings form builtin predicate URIs to SPARQL FILTER expression templates as Python string expressions with 2 arguments for builtin terms.

# Examples #

```
$ FuXi --ruleFacts --why="ASK { test:Ghent test:path test:Amsterdam }"   
    --ns=test=http://www.w3.org/2002/03owlt/TransitiveProperty/premises001# --dlp  --output=conflict 
    --debug  --method=sld --strict=defaultDerived http://www.w3.org/2002/03owlt/TransitiveProperty/premises001
Time to build production rule (RDFLib): 0.000124931335449 seconds
../FuXi/Rete/Magic.py:515: UserWarning: predicate symbol of test:path(?X ?lNHNLsHP20) is in both IDB and EDB. Marking as derived
  "predicate symbol of %s is in both IDB and EDB. Marking as %s"%(term,mark))
reduction in size of program: -200.0 (1 -> 3 clauses)
Derived predicates  [u'test:path']
Sideways Information Passing (sip) graph: 
{ path, path } -> ?lNHNLsHP19, ?lNHNLsHP20 path_lNHNLsHP19_lNHNLsHP20
{ path } -> ?X path_X_lNHNLsHP19
Magic seed fact (used in bottom-up evaluation) :path_magic(:Ghent :Amsterdam)
	Solving :path(:Ghent :Amsterdam)
	Processing rule :path_bb(?X ?lNHNLsHP20) :- And( :path_bf(?X ?lNHNLsHP19) :path_bb(?lNHNLsHP19 ?lNHNLsHP20) )
	Solving :path(:Ghent ?lNHNLsHP19)
SELECT ?lNHNLsHP19 { 	test:Ghent test:path ?lNHNLsHP19 } 2 apriori binding(s)-> [ .. 1 answers .. ]
	Solving :path(:Antwerp :Amsterdam)
	Processing rule :path_bb(?X ?lNHNLsHP20) :- And( :path_bf(?X ?lNHNLsHP19) :path_bb(?lNHNLsHP19 ?lNHNLsHP20) )
	Solving :path(:Antwerp ?lNHNLsHP19)
SELECT ?lNHNLsHP19 { 	test:Antwerp test:path ?lNHNLsHP19 } 2 apriori binding(s)-> [ .. 1 answers .. ]
	Solving :path(:Amsterdam :Amsterdam)
	Processing rule :path_bb(?X ?lNHNLsHP20) :- And( :path_bf(?X ?lNHNLsHP19) :path_bb(?lNHNLsHP19 ?lNHNLsHP20) )
	Solving :path(:Amsterdam ?lNHNLsHP19)
SELECT ?lNHNLsHP19 { 	test:Amsterdam test:path ?lNHNLsHP19 } 2 apriori binding(s)-> []
ASK { 	test:Amsterdam test:path test:Amsterdam } 3 apriori binding(s)-> False
ASK { 	test:Antwerp test:path test:Amsterdam } 3 apriori binding(s)-> True
Time to reach answer True via top-down SPARQL sip strategy: 25.2461433411 milli seconds
Time to calculate closure on working memory:  7.8558921814 milli seconds
<Network: 3 rules, 13 nodes, 47 tokens in working memory, 6 inferred tokens>
<TerminalNode (pass-thru): CommonVariables: [?X, ?lNHNLsHP20] (0 in left, 3 in right memories)>
	:path_magic(?X) :- :path_magic(?X ?lNHNLsHP20)
		3 instanciations
<TerminalNode : CommonVariables: [?X] (3 in left, 3 in right memories)>
	:path_magic(?lNHNLsHP19 ?lNHNLsHP20) :- And( :path_magic(?X ?lNHNLsHP20) :path_bf(?X ?lNHNLsHP19) :path_magic(?X) )
		2 instanciations
<TerminalNode : CommonVariables: [?X, ?lNHNLsHP19] (6 in left, 3 in right memories)>
	:path_bb(?X ?lNHNLsHP20) :- And( :path_magic(?X ?lNHNLsHP20) 
                                                                      :path_magic(?X) 
                                                                      :path_bf(?X ?lNHNLsHP19) 
                                                                      :path_magic(?lNHNLsHP19 ?lNHNLsHP20) 
                                                                      :path_bb(?lNHNLsHP19 ?lNHNLsHP20) )
		1 instanciations
```
```
$ FuXi --ns=ex=http://www.agfa.com/w3c/euler/subclass# \
       --why="ASK { ex:i a ex:A }" --debug --method=bfp \
       --input-format=n3 --dlp http://www.agfa.com/w3c/euler/subclass.n3
[..snip..]
 maximal db conjunction Query triggered for  ns1:B_query(?X) :- bfp:evaluate(rule:1 0)
ASK { 	<http://www.agfa.com/w3c/euler/subclass#i>  a  <http://www.agfa.com/w3c/euler/subclass#B> }-> True

Inferred triple:  (rdflib.URIRef('http://www.agfa.com/w3c/euler/subclass#i'), rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://www.agfa.com/w3c/euler/subclass#A'))  from  ns1:A_b(?X) :- And( ns1:A_query_b(?X) bfp:evaluate(rule:1 1) )

Reached ground goal. Terminated BFP!
Time to reach answer ground goal answer of True: [...] milli seconds
```


```
$ FuXi \
--output=rif --safety=loose --strictness=loose \
--ddlGraph=test/drugBankDDL.n3 --method=sld 
--output=n3 \
--why="SELECT ?label { ?drug a drugbank:InfluenzaDrug; rdfs:label ?label }" 
--debug --ontology=test/drugBankOnt.n3 
--ontologyFormat=n3 
--builtinTemplates=http://fuxi.googlecode.com/hg/RuleBuiltinSPARQLTemplates.n3 
--sparqlEndpoint --dlp http://www4.wiwiss.fu-berlin.de/drugbank/sparql

## Full SPARQL Algebra expression ##
BGP((?drug,rdf:type,drugbank:InfluenzaDrug),(?drug,rdfs:label,?label))
###################################
No SIP graph!
Goal/Query:  (?drug, rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugbank/InfluenzaDrug'))
        Solving :InfluenzaDrug(?drug) {}
        Processing rule :InfluenzaDrug_f(?X) :- drugbank:affectedOrganism(?X "Influenza Virus")
                Solving :affectedOrganism(?X "Influenza Virus") {}
SELECT ?X {     ?X <http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugbank/affectedOrganism> "Influenza Virus" }-> []
FtWarning: Creation of InputSource without a URI
Evaluating TP against EDB:  SELECT ?label {     <http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/DB00198> <http://www.w3.org/2000/01/rdf-schema#label> ?label }
Time to reach answer Oseltamivir via top-down SPARQL sip strategy: 731.135129929 milli seconds

$ FuXi \
--output=rif --safety=loose --strictness=loose --ddlGraph=test/drugBankDDL.n3 \
--method=bfp --output=n3 \
--why="SELECT ?label { ?drug a drugbank:InfluenzaDrug; rdfs:label ?label }" \
--debug --ontology=test/drugBankOnt.n3 --ontologyFormat=n3 \
--builtinTemplates=http://fuxi.googlecode.com/hg/RuleBuiltinSPARQLTemplates.n3 \
--sparqlEndpoint \
--dlp http://www4.wiwiss.fu-berlin.de/drugbank/sparql

## Full SPARQL Algebra expression ##
BGP((?drug,rdf:type,drugbank:InfluenzaDrug),(?drug,rdfs:label,?label))
###################################
No SIP graph!
Goal/Query:  (?drug, rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugbank/InfluenzaDrug'))
Time to build production rule (RDFLib): 0.000101089477539 seconds
        1. Forall ?X ( :InfluenzaDrug_f(?X) :- drugbank:affectedOrganism(?X "Influenza Virus") )
Asserting initial BFP query  :OpenQuery(:InfluenzaDrug)
Query triggered for  :affectedOrganism_query(?X "Influenza Virus") :- bfp:evaluate(rule:1 0)
FtWarning: Creation of InputSource without a URI
SELECT ?X {     ?X <http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugbank/affectedOrganism> "Influenza Virus" }-> []
        Answer to BFP triggered query drugbank:affectedOrganism(:DB00198 "Influenza Virus") : {?X: rdflib.URIRef('http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/DB00198')}
Goal/Query:  (?drug, rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), rdflib.URIRef('http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugbank/InfluenzaDrug'))
Query was not ground
Evaluating TP against EDB:  SELECT ?label {     <http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/DB00198> <http://www.w3.org/2000/01/rdf-schema#label> ?label }
FtWarning: Creation of InputSource without a URI
Time to reach answer Oseltamivir via top-down SPARQL sip strategy: 725.481987 milli seconds

```
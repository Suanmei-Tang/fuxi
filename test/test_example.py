"""
For question: "OWL reasoning example with FuXi (Rdflib / Python)"

http://answers.semanticweb.com/questions/22619/owl-reasoning-example-with-fuxi-rdflib-python
"""

from FuXi.Syntax.InfixOWL import *
from rdflib import plugin, BNode, Namespace, Literal, RDFS
from rdflib.Graph import Graph
from rdflib.util import first
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.DLP.DLNormalization import NormalFormReduction
from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore

EX_NS = Namespace('http://example.com#')
EX_FACTORY = ClassNamespaceFactory(EX_NS)

def main():
    g = Graph()
    Individual.factoryGraph = g
    g.bind('ex', EX_NS, override=False)

    isChildOf   = Property(EX_NS.isChildOf)
    isMarriedTo = Property(EX_NS.isMarriedTo)


    woman = Class(EX_NS.Woman)
    man   = Class(EX_NS.Man,
                  subClassOf=[isMarriedTo|only|woman],
                  # complementOf=woman
    )
    woman.subClassOf = [isMarriedTo|only|man]

    # Class(OWL_NS.Thing,subClassOf=[isMarriedTo|min|Literal(1)])

    man.extent = [EX_NS.John,EX_NS.Tim]
    woman.extent = [EX_NS.Kate,EX_NS.Mary]

    #Semantically equivalent to Abox assertion below
    # anon_cls1 = Class(
    #     subClassOf=[isMarriedTo|some|EnumeratedClass(members=[EX_NS.Mary])]
    # )
    # anon_cls1.extent = [EX_NS.John]
    g.add((EX_NS.John,isMarriedTo.identifier,EX_NS.Mary))

    #Semantically equivalent to Abox assertion below
    # anon_cls2 = Class(
    #     subClassOf=[isChildOf|some|EnumeratedClass(members=[EX_NS.John])]
    # )
    # anon_cls2.extent = [EX_NS.Kate]
    g.add((EX_NS.Kate,isChildOf.identifier,EX_NS.John))

    #Semantically equivalent to Abox assertion below
    # anon_cls3 = Class(
    #     subClassOf=[isChildOf|some|EnumeratedClass(members=[EX_NS.Mary])]
    # )
    # anon_cls3.extent = [EX_NS.Tim]
    g.add((EX_NS.Tim,isChildOf.identifier,EX_NS.Mary))

    print g.serialize(format='pretty-xml')

    rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
    network.nsMap = { u'ex' : EX_NS }

    # NormalFormReduction(g)
    dlp=network.setupDescriptionLogicProgramming(
                             g,
                             addPDSemantics=False,
                             constructNetwork=False
    )
    for rule in dlp:
        print rule

    topDownStore=TopDownSPARQLEntailingStore(
                    g.store,
                    g,
                    idb=dlp,
                    DEBUG=True,
                    derivedPredicates=[EX_NS.Man,EX_NS.Woman],
                    nsBindings=network.nsMap,
                    identifyHybridPredicates = True)
    targetGraph = Graph(topDownStore)
    rt=targetGraph.query("ASK { ex:Tim ex:isMarriedTo ex:John }",
                         initNs=network.nsMap)
    print rt.askAnswer[0]

    topDownStore.DEBUG = False

    for ind in g.query("SELECT ?ind { ?ind a ?class FILTER(isUri(?ind) && ?class != owl:Class ) }"):
        print "Individual: ", ind
        print "--- Children ---"
        for child in targetGraph.query("SELECT ?child { ?child ex:isChildOf %s }"%ind.n3(),
                                       initNs=network.nsMap):
            print "\t- ", child
        print "----------------"

if __name__ == '__main__':
    main()

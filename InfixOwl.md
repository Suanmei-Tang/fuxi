_[/trunk/python-dlp/fuxi/lib/Syntax/InfixOWL.py](http://python-dlp.googlecode.com/svn/trunk/fuxi/lib/Syntax/)_

This has been [integrated](http://groups.google.com/group/fuxi-discussion/t/ea670004f8b018ec) into FuXi.

[DOAP](http://usefulinc.com/doap/) file: _[/trunk/InfixOWL/InfixOWL.rdf](http://python-dlp.googlecode.com/svn/trunk/InfixOWL/InfixOWL.rdf)_


# Introduction #

An infix syntax for Python, [Manchester OWL](http://owl-workshop.man.ac.uk/acceptedLong/submission_9.pdf), OWL Abstract [Syntax](http://www.w3.org/TR/owl-semantics/syntax.html), and RDF (via RDFLib).

# First Class Infix Operators #

Other Python equivalents of Manchester OWL:

  * |only|
  * |max|
  * |min|
  * |exactly|
  * |value|

# A Recent Example of Usage #

```
    from FuXi.Syntax.InfixOWL import *
    from rdflib import plugin, BNode, Namespace, Literal, OWL
    from rdflib.Literal import _XSD_NS
    from rdflib.syntax.NamespaceManager import NamespaceManager
    from rdflib.Graph import Graph, ConjunctiveGraph
    from rdflib.util import first

    HHCO_NS   = Namespace('http://purl.org/hhco/')
    CPR_NS    = Namespace('http://purl.org/cpr/')
    RO_NS     = Namespace('http://www.obofoundry.org/ro/ro.owl#')
    FRBR_NS   = Namespace('http://purl.org/vocab/frbr/core#')

    SKOS      = Namespace('http://www.w3.org/2004/02/skos/core#')
    HHCO      = ClassNamespaceFactory(HHCO_NS)
    CPR       = ClassNamespaceFactory(CPR_NS)
    FRBR      = ClassNamespaceFactory(FRBR_NS)
    VCARD     = Namespace('http://www.w3.org/2006/vcard/ns#')

    DC        = Namespace('http://purl.org/dc/elements/1.1/')
    FOAF      = Namespace('http://xmlns.com/foaf/0.1/')
    SNAP      = Namespace('http://www.ifomis.org/bfo/1.1/snap#')
    SPAN      = Namespace('http://www.ifomis.org/bfo/1.1/span#')

    namespace_manager = NamespaceManager(Graph())
    namespace_manager.bind('hhco', HHCO_NS, override=False)
    namespace_manager.bind('foaf', FOAF, override=False)
    namespace_manager.bind('dc', DC, override=False)
    namespace_manager.bind('cpr', CPR_NS, override=False)
    namespace_manager.bind('snap', SNAP, override=False)
    namespace_manager.bind('span', SPAN, override=False)
    g = Graph()
    g.namespace_manager = namespace_manager
    Individual.factoryGraph = g

    clinicalAct              = CPR['clinical-act']
    patient                  = CPR.patient
    person                   = CPR.person
    spacialRegion            = Class(SNAP['SpatialRegion'])
    representationalArtifact = CPR['representational-artifact']
    corporateBody            = FRBR['CorporateBody']
    processualEntity         = Class(SPAN.ProcessualEntity)

    representationOf         = Property(RO_NS['representationOf'])
    representedBy            = Property(CPR_NS['representedBy'])
    hasPart                  = Property(RO_NS['has_part'])
    hasOutput                = Property(CPR_NS['hasOutput'])
    outputOf                 = Property(CPR_NS['outputOf'])
    hasParticipant           = Property(RO_NS['has_participant'])
    hasAgent                 = Property(RO_NS['has_agent'])
    charge                   = Property(HHCO_NS['charge'],baseType=OWL.DatatypeProperty)
    payment                  = Property(HHCO_NS['paid'],baseType=OWL.DatatypeProperty)

    billedAccordingTo        = Property(HHCO_NS.billedAccordingTo)
    insurer                  = Property(HHCO_NS.insurer)
    policyHolder             = Property(HHCO_NS.policyHolder)


    Ontology(
        HHCO_NS,
        imports=[CPR_NS,URIRef('http://vocab.org/frbr/core.rdf')],
        comment=Literal('An ontology describing home health care services and billing'))

    hhcPayorSource = Class(
        HHCO_NS['PayorSource'],
        subClassOf=[corporateBody],
        nameAnnotation = 'payor source',
        nameIsLabel=True,
        nounAnnotations=('payor source','payor sourcees')
    )

    policy = Class(
        HHCO_NS['Policy'],
        subClassOf=[
            insurer     |some|hhcPayorSource,
            policyHolder|some|patient,
        ],
        nameAnnotation = 'home care policy',
        nameIsLabel=True,
        nounAnnotations=('home care policy','home care policies')
    )

    home = Class(
        HHCO_NS['Home'],
        subClassOf=[spacialRegion],
        nameAnnotation = 'home',
        nameIsLabel=True,
        nounAnnotations=('home','homes')
    )

    asf = Class(
        HHCO_NS['AssistedLivingFacility'],
        subClassOf=[spacialRegion],
        nameAnnotation = 'assisted living facility',
        nameIsLabel=True,
        nounAnnotations=('assisted living facility','assisted living facility')
    )

    hhcProvider = Class(
        HHCO_NS['Provider'],
        subClassOf = [person],
        nameAnnotation = 'home healthcare provider',
        nameIsLabel=True,
        nounAnnotations=('home healthcare provider','home healthcare providers')
    )

    hhcVisit = Class(
        HHCO_NS['Visit'],
        subClassOf=[hasAgent|some|hhcProvider],
        nameAnnotation = 'home care visit',
        nameIsLabel=True,
        nounAnnotations=('home care visit','home care visits')
    )

    hhcVisitLineItem = Class(
        HHCO_NS['VisitLineItem'],
        subClassOf=[
            representationalArtifact,
            representationOf|some|hhcVisit
        ],
        nameAnnotation = 'home care visit line item',
        nameIsLabel=True,
        nounAnnotations=('home care visit line item','home care visit line items')
    )

    charge.domain = hhcVisitLineItem
    charge.range   = _XSD_NS.int

    payment.domain = hhcVisitLineItem
    payment.range   = _XSD_NS.int

    hhcBill = Class(
        HHCO_NS['Claim'],
        subClassOf=[
            representationalArtifact,
            hasPart|only|hhcVisitLineItem,
            billedAccordingTo|some|policy
        ],
        nameAnnotation = 'home care claim',
        nameIsLabel=True,
        nounAnnotations=('home care claim','home care claims')
    )

    billedAccordingTo.domain = hhcBill
    billedAccordingTo.range  = policy

    insurer.domain = policy
    insurer.range  = hhcPayorSource

    policyHolder.domain = policy
    policyHolder.range  = patient

    billProcessMD = [
        (HHCO_NS['ClaimPreparation'],
         'home care claim preparation',
         'home care claim preparation'),
        (HHCO_NS['ClaimDenialClarification'],
         'home care claim denial clarification',
         'home care claim denial clarification'),
        # (HHCO_NS['ClaimResubmissionPreparation'],
        #  'home care claim re-submission preparation',
        #  'home care claim re-submission preparation'),
        (HHCO_NS['ClaimRemitProcess'],
         'home care claim remit process',
         'home care claim remit processes'),
    ]

    billProcesses = []

    for _id,name,nounAnnotationPl in billProcessMD:
        _cl = Class(
            _id,
            subClassOf=[
                processualEntity,
                hasParticipant|some|hhcBill
                ],
            nameAnnotation = name,
            nameIsLabel=True,
            nounAnnotations=(name,nounAnnotationPl)
        )
        billProcesses.append(_cl)

    billProcessDisj = BooleanClass(operator=OWL_NS.unionOf,members=billProcesses)
    billProcessDisj.label = [Literal('Home care claim processes')]
```

An example of using _extent_ [properties](http://docs.python.org/2/library/functions.html#property) to manipulate the ABox via InfixOWL class objects
```
    someBill    = BNode()
    somePolicy  = BNode()

    hhcBill.extent           = [someBill]
    policy.extent            = [somePolicy]
    billedAccordingTo.extent = [(someBill,somePolicy)] 

```
# Introduction #

For reference, the **ddl** prefix is bound to the URI: _http://code.google.com/p/fuxi/wiki/DataDescriptionLanguage#_

# Details #

The following classes and classes can be used to assign one or more URIs as [derived or base predicates](http://code.google.com/p/fuxi/wiki/Overview#Base_and_Derived_Predicates)

## ddl:DerivedClassList and ddl:DerivedPropertyList ##

The class of RDF [lists](http://www.w3.org/TR/rdf-mt/#collections) whose members are each URIs of derived predicates

## ddl:BaseClassList ##

Same structure as ddl:DerivedClassList except the members are URIs of base predicates

## ddl:DerivedPropertyPrefix ##

The class of RDF [lists](http://www.w3.org/TR/rdf-mt/#collections) whose members are each URIs that are a common prefix for the URIs of derived, binary predicates and is a good way to specify an entire terminology (which shares a common namespace URI) as derived

## ddl:DerivedClassPrefix ##

Same as ddl:DerivedPropertyPrefix except the prefix identifies URIs of derived unary predicates

## ddl:BaseClassPrefix ##

Similar to ddl:DerivedClassPrefix except the prefix identifies URIs of base unary predicates

## ddl:BasePropertyPrefix ##

Similar to ddl:DerivedPropertyPrefix except it provides a common prefix for base binary predicates

## ddl:DerivedClassQuery ##

The class of RDF strings that are SPARQL queries which when evaluated against a given OWL graph returns the URIs of derived, unary predicates
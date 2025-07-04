# NFL Syntax Specification (v0.3)

The following grammar formally defines Node Form Language (NFL) using
Extended Backus–Naur Form. Blocks are determined by indentation similar
to Python. Comments beginning with `//` or surrounded by `/* ... */` are
ignored by the parser.

```ebnf
(*  NFL v0.3 – grammar in Extended Backus–Naur Form                         *)
(*  Square brackets …   = optional                                           *)
(*  Curly braces   …    = zero-or-more repetitions                           *)
(*  Vertical bar  |     = choice                                             *)

NFL            ::= { NodeDefinition | Comment | SectionDivider } ;

Comment        ::= "//" { ~NEWLINE } NEWLINE ;
SectionDivider ::= "/*" { ~"*/" } "*/" ;

NodeDefinition ::= "node:" NodeId InlineAttrs? NEWLINE Indent
                     { TraitLine | EdgeLine | Comment }*
                   Dedent ;

InlineAttrs    ::= "|" AttrAssignment { "," AttrAssignment } ;
AttrAssignment ::= AttrKey ":" StringLiteral ;

TraitLine      ::= "trait:" TraitKey ":" TraitValue NEWLINE ;
EdgeLine       ::= "edge:" EdgeType "->" "node:" NodeId NEWLINE ;

(*  -------------------- Lexical tokens ----------------------------------  *)

NodeId         ::= Ident ;
AttrKey        ::= Ident ;
TraitKey       ::= Ident ;
EdgeType       ::= Ident ;

TraitValue     ::= StringLiteral
                |  JsonObject
                |  JsonArray ;

JsonObject     ::= "{"  …valid JSON object…  "}" ;
JsonArray      ::= "["  …valid JSON array…   "]" ;

StringLiteral  ::= '"' { ~'"' } '"' ;

Ident          ::= ( ALPHA | "_" )
                   { ALPHA | DIGIT | "_" | "-" } ;

Indent         ::=  ⬅ implicit, one level deeper than parent line
Dedent         ::=  ⬅ implicit, back to parent indent

NEWLINE        ::= "\n" ;
```

### Example

```
// NFL v0.3
node: sample_workflow | isa:"Workflow"
    trait: trigger: "new_ticket"
    edge: step -> node: first_step

node: first_step | isa:"Step"
    trait: action_py: "handlers.process"
```

This declares a workflow triggered by the `new_ticket` event which calls a
single step implemented in Python.

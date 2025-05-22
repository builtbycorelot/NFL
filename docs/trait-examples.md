# Trait Examples

Traits qualify how a node behaves. Below are small real-world examples.

```
node:Dataset | trait:public
node:Processor | trait:pci_compliant
edge:Dataset -> Processor | trait:encrypted
```

The `public` trait marks data for open sharing while `pci_compliant` ensures processing meets payment standards.

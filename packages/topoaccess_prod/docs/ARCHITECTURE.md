# Architecture

Production package boundary:

- Required stable dependencies: `topoaccess.v29_common`, `topoaccess.provenance`.
- Optional stable dependencies: V28/V29 release artifacts for dashboards and manifests.
- Exploratory modules: V1-V27 experiment modules are not imported by product code.
- Deprecated/do-not-import: E8 routing, student promotion, global model fallback, cloud backends.

The product package uses thin adapters over the validated V29 wrapper service backend rather than copying exploratory research code.

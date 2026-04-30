# prophet-core-query

`prophet-core-query` owns query contracts and examples for auditable, provenance-first context resolution across SocioProphet surfaces.

## Professional Intelligence context query

The first Professional Intelligence OS query contract binds workroom, entity, search packet, memory context, policy decision, obligation, and evidence references into a validated context-query artifact.

Contract and example:

- `schemas/professional-intelligence-context-query.schema.json`
- `examples/professional-intelligence/context-query.example.json`

Validate locally:

```bash
python -m pip install jsonschema
python scripts/validate_professional_intelligence_context_query.py
```

The workflow `.github/workflows/professional-intelligence-context-query.yml` runs this validation when the schema, example, validator, or workflow changes.

This query contract supports the Gate 3 Professional Intelligence OS demo path by connecting:

- Sherlock search packets;
- Memory Mesh context packs;
- Policy Fabric policy decisions;
- ContractForge obligations;
- Prophet Workspace workrooms;
- Agentplane workflow evidence;
- Prophet Platform evidence and adoption contracts.

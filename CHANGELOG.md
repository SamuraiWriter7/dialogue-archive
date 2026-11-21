# Changelog

All notable changes to Dialogue Archive are documented in this file.

This project follows Semantic Versioning principles.

---

## [0.1.0] - 2026-11-22

### Initial Release

Dialogue Archive v0.1.0 establishes a minimal protocol for preserving human–AI dialogues and linking conversation messages to externally identified questions.

### Added

#### Core Specification

- Initial Dialogue Archive v0.1 protocol specification.
- Structured JSON dialogue record model.
- Dialogue identifiers and conversation metadata.
- Ordered human–AI text messages.
- External question references.
- Private and public visibility declarations.
- Optional content transformation metadata.

#### Structural Validation

Introduced seven structural invariants:

- **DA-001:** Valid dialogue identifiers.
- **DA-002:** Unique dialogue identifiers within a validation dataset.
- **DA-003:** Unique message identifiers within each dialogue.
- **DA-004:** Valid message structure.
- **DA-005:** Local question reference integrity.
- **DA-006:** Valid visibility declarations.
- **DA-007:** JSON Schema conformance.

#### JSON Schema

- Added JSON Schema Draft 2020-12 definition.
- Defined required record fields and supported values.
- Restricted unsupported additional properties.
- Added timestamp format validation.

#### Reference Implementation

- Added Python 3.11-compatible validator.
- Implemented JSON Schema validation.
- Implemented duplicate identifier detection.
- Implemented local message reference checks.
- Added validation error reporting and exit codes.

#### Examples

- Added a synthetic human–AI dialogue example.
- Included three external question references.
- Demonstrated private archive visibility.

#### Continuous Integration

- Added GitHub Actions validation workflow.
- Configured automated validation on push and pull requests.
- Added manual workflow execution support.
- Confirmed successful GitHub Actions execution.

### Integration Boundaries

- External question identifiers remain independent of Dialogue Archive.
- Question derivation validation remains outside the protocol.
- QuestionTube integration is optional.
- External question resolution is not required for v0.1 validation.

### Limitations

Version 0.1.0 does not provide:

- Automatic chat imports.
- Full-text search.
- Blog publishing.
- Semantic question extraction.
- AI long-term memory.
- Autonomous research agents.
- Cryptographic provenance verification.
- Access control enforcement.
- Economic contribution valuation.

The initial CI workflow validates the included sample record.

Comprehensive negative-test coverage is not yet included.

### Design Principle

> Preserve the dialogue. Trace the question. Enable future knowledge reuse.

---

## Future Development

Future versions may introduce additional capabilities when supported by concrete requirements and validation results.

Potential areas include:

- Search integration.
- Question graph visualization.
- Cross-archive references.
- Research memory integration.
- Reasoning artifact reuse.

These are exploratory directions, not committed features.

Dialogue Archive prioritizes minimal structure, independent validation, and incremental evolution.

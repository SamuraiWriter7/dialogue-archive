# Dialogue Archive Protocol Specification v0.1

**Protocol:** Dialogue Archive  
**Version:** 0.1.0  
**Status:** Draft Specification  
**Purpose:** Human–AI Dialogue Preservation and Question Reference Integration

---

## 1. Purpose

Dialogue Archive is a minimal protocol for preserving structured human–AI conversation records and associating them with identifiable questions.

The protocol addresses two fundamental requirements:

1. Preserve human–AI dialogue records in a consistent structure.
2. Maintain references between recorded messages and externally identified questions.

Dialogue Archive does not attempt to independently evaluate the meaning, correctness, or value of conversations.

It also does not define question derivation or contribution verification.

Those responsibilities may be delegated to external protocols such as QuestionTube.

### Core Principle

> Preserve the dialogue without altering its meaning. Connect questions without redefining their relationships.

---

## 2. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY indicate requirement levels.

- **MUST:** Mandatory for conformance.
- **MUST NOT:** Prohibited.
- **SHOULD:** Recommended unless a documented reason exists.
- **SHOULD NOT:** Discouraged unless justified.
- **MAY:** Optional.

A conforming v0.1 implementation MUST satisfy all mandatory requirements defined in this specification.

---

## 3. Scope

### 3.1 Included

Dialogue Archive v0.1 defines:

- Dialogue identifiers.
- Basic conversation metadata.
- Ordered text messages.
- Message identifiers.
- Human and assistant roles.
- External question references.
- Local reference integrity.
- Visibility declarations.
- JSON Schema conformance.
- Structural validation requirements.

### 3.2 Excluded

Dialogue Archive v0.1 does not define:

- Automatic conversation import.
- Platform-specific APIs.
- Full-text search.
- Blog rendering or publishing.
- Semantic question extraction.
- Automatic question classification.
- Question derivation validation.
- AI long-term memory.
- Retrieval-augmented generation.
- Autonomous research continuation.
- Identity authentication.
- Cryptographic provenance.
- Economic contribution valuation.
- Royalty redistribution.
- Cross-repository synchronization.

These exclusions are intentional.

The initial protocol establishes a minimal preservation and reference structure.

---

## 4. Conceptual Architecture

Dialogue Archive separates conversation records from question evolution.

```text
Human–AI Conversation
          |
          v
+----------------------+
|   Dialogue Archive   |
|                      |
| Dialogue Identifier  |
| Metadata             |
| Ordered Messages     |
| Question References  |
| Visibility           |
+----------+-----------+
           |
           | External Question IDs
           v
+----------------------+
|     QuestionTube     |
|                      |
| Question Registry    |
| Derivation Graph     |
| Contribution Records |
| Structural Validation|
+----------------------+
```

Dialogue Archive is responsible for preserving dialogue information.

QuestionTube may independently manage question relationships.

Neither system is required to control the internal data structures of the other.

### 4.1 Independence

A valid Dialogue Archive record MUST NOT require an active QuestionTube service.

External question identifiers MAY remain unresolved during local validation.

### 4.2 Separation of Responsibilities

Dialogue Archive MUST NOT infer question derivation relationships solely from message sequence.

Chronological order is not equivalent to logical derivation.

---

## 5. Dialogue Record Model

A Dialogue Archive record MUST be represented as a JSON object.

The following top-level fields are REQUIRED:

| Field | Type | Description |
|---|---|---|
| `archive_version` | string | Protocol version |
| `dialogue_id` | string | Dialogue identifier |
| `metadata` | object | Conversation metadata |
| `visibility` | string | Publication visibility |
| `messages` | array | Ordered messages |
| `question_links` | array | External question references |

The value of `archive_version` MUST equal `0.1.0`.

Unknown top-level fields MUST be rejected by the v0.1 schema.

---

## 6. Dialogue Identifier

Every dialogue MUST contain a non-empty `dialogue_id`.

Example:

```json
{
  "dialogue_id": "D001"
}
```

### 6.1 Requirements

- The identifier MUST be a string.
- The identifier MUST NOT be empty or whitespace-only.
- The identifier MUST be unique within the validation dataset.
- The identifier MUST remain stable for the same archived record.

Dialogue Archive v0.1 does not require globally unique identifiers across independent archives.

### 6.2 Identifier Scope

The uniqueness boundary is the validation dataset.

Independent repositories MAY use identical dialogue identifiers.

External systems MUST NOT assume that `D001` uniquely identifies a dialogue across all archives.

---

## 7. Metadata

Every dialogue MUST contain a `metadata` object.

Required fields:

| Field | Type | Description |
|---|---|---|
| `title` | string | Dialogue title |
| `created_at` | string | Creation timestamp |
| `source` | string | Declared source |
| `tags` | array | Descriptive labels |

Example:

```json
{
  "metadata": {
    "title": "AI Reasoning and Human Thinking",
    "created_at": "2026-11-21T10:00:00+09:00",
    "source": "manual-import",
    "tags": [
      "ai-reasoning",
      "human-ai-collaboration"
    ]
  }
}
```

### 7.1 Title

The title MUST be a non-empty string.

It MAY be assigned manually.

The title does not establish the factual content or meaning of the conversation.

### 7.2 Timestamp

`created_at` MUST use an RFC 3339-compatible timestamp.

A timezone offset or UTC designation is REQUIRED.

Valid example:

```text
2026-11-21T10:00:00+09:00
```

The timestamp represents the declared creation time of the dialogue.

The protocol does not independently authenticate timestamps.

### 7.3 Source

The `source` field MUST be a non-empty string.

Examples:

```text
manual-import
chat-export
research-record
```

These values are illustrative.

The source field does not authenticate the original platform or participant identities.

### 7.4 Tags

The `tags` field MUST be an array of strings.

An empty array is permitted.

Tags are descriptive labels.

They MUST NOT be interpreted as verified semantic classifications.

### 7.5 Content Transformation Metadata

A dialogue MAY contain the following optional metadata:

- `content_status`
- `source_record_id`

Permitted values of `content_status` are:

```text
original
edited
redacted
unknown
```

`source_record_id` is a non-empty string identifying the declared source record.

When a record is deliberately edited or redacted, its publisher MUST identify that transformation using `content_status`.

The original record SHOULD remain separately preserved when authorization and retention policies permit.

If `content_status` is absent, the transformation status is unspecified.

An unspecified status MUST NOT be interpreted as proof of an unmodified original.

The protocol does not independently verify transformation claims.

---

## 8. Message Model

Every dialogue MUST contain a `messages` array.

The array MUST contain at least one message.

Each message MUST contain:

| Field | Type | Requirement |
|---|---|---|
| `message_id` | string | REQUIRED |
| `role` | string | REQUIRED |
| `content` | string | REQUIRED |

Example:

```json
{
  "messages": [
    {
      "message_id": "M001",
      "role": "human",
      "content": "Can AI reasoning costs decrease?"
    },
    {
      "message_id": "M002",
      "role": "assistant",
      "content": "Reasoning costs may change through improved efficiency."
    }
  ]
}
```

### 8.1 Message Identifiers

Every message MUST have a non-empty identifier.

Message identifiers MUST be unique within their containing dialogue.

Identical message identifiers MAY appear in different dialogues.

### 8.2 Roles

Dialogue Archive v0.1 supports exactly two roles:

```text
human
assistant
```

Other roles are not supported in v0.1.

Records containing unsupported roles MUST fail validation.

### 8.3 Message Content

Every message MUST contain non-empty text content.

Whitespace-only content is invalid.

The protocol stores message content as text.

Images, audio, video, attachments, tool payloads, and multimodal structures are outside the v0.1 data model.

### 8.4 Message Ordering

The order of messages in the array MUST represent the declared conversation sequence.

Consumers MUST preserve that order.

Message identifiers MUST NOT be used to infer chronological ordering.

For example:

```text
messages[0]
messages[1]
messages[2]
```

The array position defines the sequence.

### 8.5 Preservation Integrity

Archiving tools SHOULD preserve message wording and sequence.

Implementations MUST NOT silently substitute summaries for original messages while claiming to preserve the original dialogue.

Edited or redacted records MUST be distinguished according to Section 7.5.

Structural validation does not prove that the recorded conversation matches its original source.

---

## 9. Question Reference Model

Every dialogue MUST contain a `question_links` array.

The array MAY be empty.

Each question link MUST contain:

| Field | Type | Description |
|---|---|---|
| `message_id` | string | Local message reference |
| `question_id` | string | External question identifier |

Example:

```json
{
  "question_links": [
    {
      "message_id": "M001",
      "question_id": "Q001"
    }
  ]
}
```

### 9.1 Local Reference Integrity

Every `message_id` referenced by a question link MUST exist in the same dialogue.

Unknown message references MUST be rejected.

### 9.2 External Question Identifiers

The `question_id` field MUST contain a non-empty string.

Dialogue Archive v0.1 does not require the corresponding external question record to be present.

External existence checks are outside local validation scope.

### 9.3 Cardinality

One dialogue MAY reference multiple questions.

One message MAY reference multiple questions.

The same external question identifier MAY be referenced by multiple messages or dialogues.

### 9.4 Relationship Semantics

A question link means:

> This dialogue message is associated with the specified question identifier.

It does not mean:

- The question originated in that message.
- The question was independently verified.
- The question derives from another question.
- The question is factually valid.
- The question has economic value.

Such interpretations require additional information or external verification.

---

## 10. Visibility Model

Every dialogue MUST declare `visibility`.

Allowed values:

```text
private
public
```

No other values are permitted in v0.1.

### 10.1 Private

`private` indicates that the dialogue is not intended for public publication.

Private records SHOULD be stored in access-controlled environments.

### 10.2 Public

`public` indicates that the dialogue has been designated for public release.

This declaration does not establish publication authorization.

### 10.3 Publication Boundary

Dialogue Archive v0.1 does not implement access control.

A publication system MUST independently enforce authorization and privacy requirements.

Before public release, the publisher SHOULD review:

- Personal information.
- Confidential material.
- Third-party information.
- Publication permissions.
- Editing or redaction requirements.

Changing `visibility` from `private` to `public` MUST NOT itself trigger publication in a conforming standalone validator.

### 10.4 Default Behavior

A missing visibility field is invalid.

Importing or archiving systems SHOULD initialize new records as `private` unless an explicit authorized publication decision has been made.

---

## 11. Complete Example

The following synthetic example illustrates the v0.1 record structure.

```json
{
  "archive_version": "0.1.0",
  "dialogue_id": "D001",
  "metadata": {
    "title": "AI Reasoning and Human Thinking",
    "created_at": "2026-11-21T10:00:00+09:00",
    "source": "manual-import",
    "tags": [
      "ai-reasoning",
      "human-ai-collaboration"
    ]
  },
  "visibility": "private",
  "messages": [
    {
      "message_id": "M001",
      "role": "human",
      "content": "Can AI reasoning costs decrease?"
    },
    {
      "message_id": "M002",
      "role": "assistant",
      "content": "Reasoning costs may decrease through improved efficiency."
    },
    {
      "message_id": "M003",
      "role": "human",
      "content": "How will this affect human thinking?"
    }
  ],
  "question_links": [
    {
      "message_id": "M001",
      "question_id": "Q001"
    },
    {
      "message_id": "M003",
      "question_id": "Q002"
    }
  ]
}
```

This record contains:

- One dialogue identifier.
- One metadata object.
- Three ordered messages.
- Two external question references.
- One visibility declaration.

No derivation relationship between Q001 and Q002 is asserted.

---

## 12. Structural Invariants

Dialogue Archive v0.1 defines seven mandatory structural invariants.

### DA-001 — Dialogue Identification

Every record MUST contain a valid, non-empty `dialogue_id`.

Expected failure:

```text
FAIL: INVALID_DIALOGUE_ID
```

### DA-002 — Unique Dialogue Identifiers

Dialogue identifiers MUST be unique within a validation dataset.

Example violation:

```text
D001
D001
```

Expected failure:

```text
FAIL: DUPLICATE_DIALOGUE_ID
```

### DA-003 — Unique Message Identifiers

Message identifiers MUST be unique within each dialogue.

Example violation:

```text
D001
 |
 +-- M001
 |
 +-- M001
```

Expected failure:

```text
FAIL: DUPLICATE_MESSAGE_ID
```

### DA-004 — Valid Message Structure

Every message MUST contain:

- A non-empty message identifier.
- A supported role.
- Non-empty content.

An unsupported role or missing required message field is invalid.

Expected failure:

```text
FAIL: INVALID_MESSAGE
```

### DA-005 — Local Question Reference Integrity

Every question link MUST reference an existing message within its containing dialogue.

Example violation:

```text
Registered messages:
M001
M002

Question link:
M999 -> Q001
```

Expected failure:

```text
FAIL: UNKNOWN_MESSAGE_REFERENCE
```

An unresolved external question identifier does not violate DA-005.

### DA-006 — Valid Visibility

The visibility field MUST equal:

```text
private
```

or:

```text
public
```

Expected failure:

```text
FAIL: INVALID_VISIBILITY
```

### DA-007 — Schema Conformance

Every record MUST conform to:

```text
schemas/dialogue-record.schema.json
```

This includes:

- Required fields.
- Field types.
- Permitted values.
- Timestamp format.
- Non-empty strings.
- Supported nested structures.
- Prohibited additional properties.

Expected failure:

```text
FAIL: SCHEMA_VALIDATION_ERROR
```

### 12.1 Failure Classification

The error codes above are reference validation categories.

The implementation SHOULD report the most specific applicable category.

A record MAY violate multiple invariants.

The validator MAY report multiple errors, or use a documented deterministic precedence rule.

Schema failures involving semantic categories such as invalid visibility MAY be reported using their specific error code.

The following additional categories MAY be used for clearer diagnostics:

```text
FAIL: INVALID_QUESTION_LINK
FAIL: INVALID_METADATA
FAIL: INVALID_ARCHIVE_VERSION
```

These categories do not create additional structural invariants.

---

## 13. Validation Dataset

A validation dataset is a collection of one or more Dialogue Archive records processed together.

A dataset MAY be supplied through multiple JSON files.

Each JSON file in the initial repository contains one dialogue record.

The reference JSON Schema validates individual records.

The reference validator is responsible for dataset-level checks.

### 13.1 Validation Responsibilities

A conforming validator MUST:

1. Parse the input records.
2. Validate record structure.
3. Check dialogue identifier uniqueness across the dataset.
4. Check message identifier uniqueness within each dialogue.
5. Validate supported message roles and content.
6. Check local message references in question links.
7. Validate visibility declarations.
8. Reject structurally invalid records.

The validator MUST NOT require external question registries.

### 13.2 Validation Result

Each processed record SHOULD produce a result equivalent to:

```text
PASS
```

or:

```text
FAIL: ERROR_CODE
```

The process MUST return a non-zero exit status when any supplied record violates a mandatory invariant.

A zero exit status indicates that all processed records passed structural validation.

It does not imply semantic or factual correctness.

---

## 14. Expected Validation Cases

The initial reference implementation SHOULD cover the following cases.

| Case | Expected |
|---|---|
| Valid dialogue record | PASS |
| Valid record with empty question links | PASS |
| Valid reference to an external question ID | PASS |
| Missing dialogue identifier | FAIL |
| Duplicate dialogue identifier in dataset | FAIL |
| Duplicate message identifier | FAIL |
| Unsupported message role | FAIL |
| Empty message content | FAIL |
| Unknown local message reference | FAIL |
| Invalid visibility value | FAIL |
| Unsupported archive version | FAIL |
| Missing required metadata | FAIL |
| Invalid timestamp format | FAIL |

An external question identifier that is not locally registered MUST NOT fail solely because it cannot be resolved.

### 14.1 Test Limitations

Passing structural tests does not establish:

- Authenticity of the source conversation.
- Correctness of conversation content.
- Participant identity.
- External question validity.
- Legitimate publication permission.
- Privacy compliance.

---

## 15. QuestionTube Integration Boundary

QuestionTube is an independent protocol for question registration and derivation validation.

Reference repository:

https://github.com/SamuraiWriter7/questiontube

### 15.1 Dialogue Archive Responsibility

Dialogue Archive records associations such as:

```text
D001 / M001 -> Q001
D001 / M003 -> Q002
```

### 15.2 QuestionTube Responsibility

QuestionTube may separately record:

```text
Q001 -> Q002
```

The second relationship indicates a question derivation.

It MUST NOT be inferred automatically from the first two associations.

### 15.3 Identifier Compatibility

Dialogue Archive v0.1 treats external question identifiers as opaque strings.

It does not require their format to match any specific question registry.

External systems are responsible for resolving identifiers within the appropriate registry scope.

### 15.4 Non-Normative Integration

QuestionTube integration is optional.

No normative cross-protocol interoperability contract is established in v0.1.

Future versions MAY define an external reference resolution mechanism if concrete interoperability problems are demonstrated.

---

## 16. Privacy and Provenance Limitations

Dialogue records may contain information that should not be publicly disclosed.

Therefore, preservation and publication MUST remain separate operations.

### 16.1 Preservation

The protocol preserves declared content and metadata.

It does not authenticate them.

### 16.2 Publication

Publication is controlled by external systems.

The presence of:

```json
{
  "visibility": "public"
}
```

MUST NOT be treated as proof of authorization.

### 16.3 Provenance

The source field provides a declared origin.

It does not establish cryptographically verifiable provenance.

### 16.4 Record Integrity

An archive system SHOULD avoid silently modifying stored conversations.

Transformation metadata can distinguish edited or redacted records.

However, independent integrity verification is outside v0.1.

### 16.5 Sensitive Information

Implementations SHOULD avoid placing private conversation exports directly into public Git repositories.

Public examples SHOULD use synthetic or explicitly authorized content.

---

## 17. Reference Implementation

The initial repository provides a Python reference validator.

Expected location:

```text
scripts/validate.py
```

The implementation is intended for Python 3.11 or later.

The intended local command is:

```bash
python scripts/validate.py
```

The validator is expected to process the included example record and report its validation result.

Implementation dependencies and exact command behavior are defined by the reference code.

The validator SHOULD maintain a small dependency footprint.

### 17.1 Schema Location

```text
schemas/dialogue-record.schema.json
```

The schema MUST represent the record structure specified in Sections 5 through 10.

The schema MUST reject unsupported record versions and unknown fields within the defined v0.1 objects.

### 17.2 Example Location

```text
examples/sample-dialogue.json
```

The example MUST conform to the v0.1 schema and structural invariants.

### 17.3 Automation

GitHub Actions integration MAY be introduced after implementation validation.

CI is not required as a separate component of the initial five-file repository.

---

## 18. Compatibility and Versioning

Dialogue Archive v0.1 uses the version identifier:

```text
0.1.0
```

Every conforming record MUST declare that exact value.

A v0.1 validator MUST reject unsupported archive versions rather than silently interpreting them as v0.1.

Future schema versions MAY introduce additional fields.

Implementations SHOULD NOT assume that all future versions will be backward-compatible.

Migration rules are outside the v0.1 scope.

---

## 19. Future Extensions

The following capabilities are reserved for possible future development.

### 19.1 Search Integration

Existing search tools may index dialogue titles, timestamps, tags, and message content.

### 19.2 Question Graph Visualization

External question graphs may be displayed alongside archived conversations.

### 19.3 Research Memory

Authorized archive records may be retrieved by research assistants.

### 19.4 Reasoning Recycling

Verified research findings may be associated with preserved dialogues and reused in future investigations.

### 19.5 Provenance Verification

External integrity and authenticity mechanisms may be introduced.

### 19.6 Cross-Archive References

Future versions may define globally scoped identifiers or repository-qualified references.

These extensions are proposals.

They MUST NOT be interpreted as mandatory v0.1 features.

---

## 20. Conformance

A Dialogue Archive v0.1 record is structurally conforming when:

1. It satisfies the v0.1 JSON Schema.
2. It satisfies all applicable local invariants.
3. Its dialogue identifier is unique within the validation dataset.
4. Its question links reference valid local messages.

A conforming validator MUST enforce these requirements.

Structural conformance does not guarantee that a record is truthful, authentic, useful, authorized for publication, or semantically meaningful.

---

## 21. Design Philosophy

Dialogue Archive begins with a deliberately limited responsibility.

It does not attempt to become:

- A universal AI memory system.
- A complete knowledge graph.
- A new conversational AI platform.
- A centralized research database.

Its purpose is to preserve the relationship between conversation records and identifiable questions.

A preserved dialogue can later support research, review, comparison, and knowledge reuse.

However, those activities belong to independent layers.

The guiding principle is:

> Preserve what was said. Record where questions appeared. Leave interpretation and validation to the appropriate systems.

---

## 22. Final Statement

Dialogue Archive v0.1 establishes a minimal, independently validatable structure for human–AI conversation records.

It preserves:

- Dialogue identity.
- Conversation metadata.
- Message sequence.
- Question references.
- Publication visibility declarations.

It deliberately excludes autonomous reasoning, semantic inference, and economic valuation.

The protocol is designed to grow only when concrete limitations become observable.

**Dialogue Archive v0.1 — Preserve the Dialogue. Trace the Question.**

*End of Specification.*

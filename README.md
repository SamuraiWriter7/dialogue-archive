# Dialogue Archive

**A Minimal Protocol for Preserving Human–AI Dialogues and Linking Question Evolution**

**Version:** v0.1.0  
**Status:** Draft Specification  
**License:** To be determined

---

## 1. Overview

Dialogue Archive is a minimal, open specification for preserving human–AI conversations as structured, reusable records.

Traditional chat archives primarily preserve conversation history.

Dialogue Archive focuses on an additional problem:

**How can a preserved conversation remain connected to the questions that emerged and evolved within it?**

The protocol separates two responsibilities:

- **Dialogue preservation:** Recording what was actually said.
- **Question evolution:** Referencing questions and their relationships through an external protocol.

Dialogue Archive does not attempt to replace existing chat applications, archive tools, or question-management systems.

Instead, it provides a lightweight structural layer connecting conversation records to identifiable questions.

### Core principle

> Preserve the dialogue. Trace the question. Enable future knowledge reuse.

---

## 2. Motivation

Human–AI conversations increasingly support research, learning, software design, and creative work.

However, important knowledge may remain scattered across individual conversation histories.

A conversation may contain:

- An original question.
- Several competing hypotheses.
- A correction or counterargument.
- A revised interpretation.
- A new question derived from the discussion.

When conversations are preserved only as chronological logs, these relationships can be difficult to follow.

For example:

```text
Dialogue A
    |
    +-- Q001: Can AI reasoning costs decrease?
    |
    +-- Q002: Could infrastructure become obsolete?
    |
    +-- Q003: How does human reasoning affect AI use?
```

The dialogue preserves the discussion.

An external question-evolution protocol can preserve relationships between Q001, Q002, and Q003.

Dialogue Archive connects these two forms of information without combining their responsibilities.

---

## 3. Design Principles

Dialogue Archive v0.1 follows six principles.

### 3.1 Preserve Original Content

A dialogue record should preserve the original sequence and meaning of the conversation.

Editorial summaries, interpretations, and derived questions must not silently replace the original dialogue.

If content is modified or redacted for publication, the resulting record must be distinguishable from its source.

### 3.2 Questions Remain Independent

A question is not identical to a conversation.

One conversation may contain multiple questions.

One question may also appear across multiple conversations.

Dialogue Archive records references between dialogues and questions without assuming that their relationships are one-to-one.

### 3.3 Reuse Existing Protocols

Dialogue Archive does not redefine question derivation or contribution verification.

Those responsibilities may be handled by external systems such as QuestionTube.

### 3.4 Privacy by Default

Conversation archives may contain confidential or personal information.

Records must distinguish between private and public visibility.

Public release must require an explicit publishing decision.

A visibility field alone does not provide access control or authorization.

### 3.5 Minimal Structure

Version 0.1 defines only the information necessary to:

1. Identify a dialogue.
2. Preserve its messages.
3. Record basic metadata.
4. Associate messages with question identifiers.
5. Validate local structural consistency.

### 3.6 Incremental Evolution

New functionality should be introduced only when a concrete requirement has been identified.

The initial protocol deliberately leaves advanced features outside its scope.

---

## 4. Core Architecture

```text
          Human
            |
            v
       AI Conversation
            |
            v
    +------------------+
    | Dialogue Archive |
    |                  |
    | Dialogue ID      |
    | Timestamp        |
    | Messages         |
    | Metadata         |
    | Question Links   |
    +--------+---------+
             |
             | Question References
             v
      +--------------+
      | QuestionTube |
      |              |
      | Questions    |
      | Derivations  |
      | Contributions|
      | Validation   |
      +--------------+
```

Dialogue Archive stores conversation records.

QuestionTube manages question identities, derivations, and contribution records.

The two systems remain logically independent.

Dialogue Archive v0.1 does not require QuestionTube to be installed or running.

---

## 5. Data Model

A Dialogue Archive v0.1 record contains five primary components.

| Component | Purpose |
|---|---|
| Dialogue ID | Unique conversation identifier |
| Metadata | Title, timestamp, source, and tags |
| Messages | Ordered human–AI exchanges |
| Question Links | References to identifiable questions |
| Visibility | Declared private or public status |

### 5.1 Dialogue Identifier

Each dialogue must have a non-empty identifier.

Example:

```json
{
  "dialogue_id": "D001"
}
```

Identifiers must be unique within the archive dataset.

Global uniqueness across independent archives is not required in v0.1.

### 5.2 Metadata

Metadata provides basic information for organizing and locating conversations.

Example:

```json
{
  "title": "AI Reasoning and Human Thinking",
  "created_at": "2026-11-21T10:00:00+09:00",
  "source": "manual-import",
  "tags": [
    "ai-reasoning",
    "human-ai-collaboration"
  ]
}
```

The timestamp uses ISO 8601 format with a timezone offset.

Tags are descriptive metadata and do not establish semantic relationships.

The source field identifies the declared origin of the record.

It does not independently authenticate that origin.

### 5.3 Messages

Messages preserve the ordered conversation.

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
      "content": "Costs may change with model efficiency and infrastructure."
    }
  ]
}
```

Messages must preserve their array order.

Each message must contain:

- `message_id`
- `role`
- `content`

The supported roles in v0.1 are:

- `human`
- `assistant`

Other message roles, attachments, and multimodal content are outside the initial scope.

### 5.4 Question Links

Question links associate a preserved message with an external question identifier.

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

A question link must reference a message that exists in the same dialogue.

The question identifier is an external reference.

Dialogue Archive v0.1 does not independently verify the existence or correctness of externally registered questions.

It also does not infer question derivations from chronological message order.

### 5.5 Visibility

Every dialogue record must declare its visibility.

Supported values:

```text
private
public
```

Visibility describes the intended publication status.

It does not enforce access restrictions.

A publishing system must independently verify authorization and check for sensitive content before releasing records.

---

## 6. Example Dialogue Record

The following is an illustrative record.

It is not an actual imported conversation.

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

- One dialogue.
- Three messages.
- Two question references.
- One visibility declaration.

The record does not claim that Q002 derives from Q001.

Such a relationship must be established separately.

---

## 7. Integration with QuestionTube

Dialogue Archive is designed to complement QuestionTube.

**QuestionTube: Git for Questions**

Repository:

https://github.com/SamuraiWriter7/questiontube

QuestionTube v0.1 defines:

- Question registration.
- Directed question derivation.
- Contribution records.
- Reference integrity.
- Cycle detection.
- Structural validation.

Dialogue Archive provides the conversation context in which questions were recorded.

### Example

```text
Dialogue Archive

D001
 |
 +-- M001 --> Q001
 |
 +-- M003 --> Q002


QuestionTube

Q001
 |
 | derived_from
 v
Q002
```

The dialogue association and the derivation relationship are separate records.

The arrow in the QuestionTube section represents a parent-to-child relationship.

### Integration Boundary

Dialogue Archive v0.1:

- Stores external question identifiers.
- Validates local message references.
- Does not validate external question existence.
- Does not duplicate question derivation graphs.
- Does not modify QuestionTube semantics.

Cross-protocol verification may be introduced in a later version if necessary.

No normative interoperability contract is established in v0.1.

---

## 8. Structural Validation

Dialogue Archive v0.1 defines the following minimum invariants.

| ID | Requirement |
|---|---|
| DA-001 | Every dialogue has a non-empty identifier. |
| DA-002 | Dialogue identifiers are unique within a validation dataset. |
| DA-003 | Message identifiers are unique within each dialogue. |
| DA-004 | Every message has a supported role and non-empty content. |
| DA-005 | Every question link references an existing local message. |
| DA-006 | Visibility is either `private` or `public`. |
| DA-007 | Every record conforms to the v0.1 data schema. |

The reference validator is expected to enforce these requirements.

### Validation Scope

Structural validation can determine whether a record follows the specified data format.

It cannot establish:

- Whether the conversation actually occurred.
- Whether its contents are factually correct.
- Whether the participants were authenticated.
- Whether a question is meaningful.
- Whether a question derivation is valid.
- Whether the record is safe to publish.

These concerns require separate verification or governance mechanisms.

---

## 9. Repository Structure

The proposed v0.1 repository contains five files.

```text
dialogue-archive/
├── README.md
├── specs/
│   └── dialogue-archive-v0.1.md
├── schemas/
│   └── dialogue-record.schema.json
├── examples/
│   └── sample-dialogue.json
└── scripts/
    └── validate.py
```

### File Responsibilities

**README.md**

Project overview, principles, architecture, and usage guidance.

**specs/dialogue-archive-v0.1.md**

Normative data model, requirements, invariants, and scope.

**schemas/dialogue-record.schema.json**

Machine-readable validation rules for dialogue records.

**examples/sample-dialogue.json**

A synthetic example demonstrating the v0.1 structure.

**scripts/validate.py**

Reference implementation for structural validation.

The repository does not need to contain actual private conversation archives.

---

## 10. Validation Workflow

The reference implementation is intended to support Python 3.11 or later.

After the validator has been implemented, the intended local command is:

```bash
python scripts/validate.py
```

The implementation should validate the included example and report structural errors.

A successful validation result means that the tested record satisfies the implemented structural rules.

It does not certify provenance, factual accuracy, or publication safety.

Automated CI validation may be added after the reference implementation and test expectations have been verified.

---

## 11. Privacy and Publication

Dialogue Archive distinguishes preservation from publication.

These are separate operations.

### Private Archive

A private archive may contain:

- Original conversations.
- Research notes.
- Unpublished ideas.
- Confidential information.
- Personally identifiable information.

Private archives should be stored in access-controlled environments.

### Public Archive

A public archive should contain only conversations explicitly selected for publication.

Before publication:

1. Confirm that publication is authorized.
2. Remove or redact sensitive information.
3. Review third-party privacy implications.
4. Distinguish edited content from original content.
5. Validate the resulting public record.

A `public` visibility value is not proof that these checks occurred.

### Recommended Principle

> Preserve privately by default. Publish selectively and explicitly.

---

## 12. Scope of v0.1

### Included

- Structured dialogue records.
- Dialogue identification.
- Basic metadata.
- Ordered text messages.
- Question references.
- Visibility declarations.
- JSON Schema definition.
- Local structural validation.
- Synthetic example data.

### Excluded

- ChatGPT or other platform API integration.
- Automatic import from conversation exports.
- Full-text search engines.
- Blog publishing interfaces.
- Automatic question extraction.
- Semantic question matching.
- Question derivation verification.
- AI long-term memory.
- Retrieval-augmented generation.
- Autonomous research agents.
- Contribution valuation.
- Royalty calculation.
- Distributed synchronization.
- Cryptographic provenance verification.

These exclusions are intentional.

Version 0.1 establishes a minimal data structure rather than a complete conversation-management platform.

---

## 13. Future Directions

Potential future extensions include:

### Dialogue Search

Connect existing search tools to preserved dialogue records.

### Question Evolution Visualization

Display question relationships through external graph structures such as QuestionTube.

### Research Memory

Allow AI systems to retrieve selected, authorized dialogue records as reference materials.

### Reasoning Recycling

Connect preserved dialogues to independently validated research findings, decisions, and reusable reasoning artifacts.

### Knowledge Provenance

Add verifiable references connecting published research outputs to their supporting dialogue records.

These are possible directions, not commitments.

Extensions should be introduced only after concrete requirements and validation results justify them.

---

## 14. Relationship to Other Projects

Dialogue Archive is intended to remain compatible in principle with complementary research specifications.

| Project | Responsibility |
|---|---|
| Dialogue Archive | Preserve conversation records |
| QuestionTube | Trace question evolution |
| Reasoning Recycling | Reuse validated reasoning artifacts |
| Structural DNA | Describe recurring structural patterns |
| Royalty OS | Explore attribution and value redistribution |

These relationships are conceptual.

Dialogue Archive v0.1 does not implement or require these external systems.

---

## 15. Project Philosophy

Human–AI conversations are more than temporary exchanges.

They may contain the beginnings of new research directions, conceptual frameworks, and reusable knowledge.

However, preserving a conversation is not the same as preserving verified knowledge.

Dialogue Archive begins with a more limited responsibility:

**Keep the original dialogue identifiable, structured, and connected to its associated questions.**

Other systems may later evaluate, verify, organize, or reuse the resulting information.

The protocol does not determine which conversations or questions are valuable.

It preserves the structure necessary for people and future tools to investigate them.

---

## 16. Long-Term Vision

A future research environment may connect:

```text
Human–AI Dialogue
        |
        v
Dialogue Preservation
        |
        v
Question Evolution
        |
        v
Research Verification
        |
        v
Reusable Knowledge
        |
        v
Future Research
```

Dialogue Archive addresses only the first two layers and their connection to question identifiers.

The remaining layers belong to independent systems.

This separation allows the architecture to evolve without requiring a single centralized application.

---

## 17. Guiding Statement

> Conversations preserve the past.
>
> Questions connect the past to the future.
>
> Reusable knowledge allows research to continue.

**Dialogue Archive — Preserve the Dialogue. Trace the Question.**

*An open foundation for human–AI dialogue preservation and question-linked research.*

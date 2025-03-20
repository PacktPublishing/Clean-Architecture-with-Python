# ADR-001: Use of Pydantic Models in Domain Layer

## Status
Accepted

## Context
Our API-first system requires extensive validation and serialization. Implementing these capabilities manually would require significant effort and potentially introduce bugs. Pydantic provides robust validation, serialization, and documentation through type annotations.

## Decision
We will allow Pydantic models in our domain layer, treating it as a stable extension to Python's type system rather than a volatile third-party dependency.

## Consequences
* Positive: Reduced boilerplate, improved validation, better documentation
* Positive: Consistent validation across system boundaries
* Negative: Creates dependency on external library in inner layers
* Negative: May complicate testing of domain entities

## Compliance
When using Pydantic in domain entities:
* Keep models focused on data structure, not behavior
* Avoid Pydantic-specific features that don't relate to validation
* Include comprehensive tests to verify domain rules still apply
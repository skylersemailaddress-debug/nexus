# System Doctrine

Defines the canonical doctrine for Nexus0.5.

## Initial Principles
- Nexus0.5 is the target product authority.
- Architectural intent is declared in this repo first.
- Donor repos are references, not authorities.
- Decisions prioritize verifiable local buildability and operational clarity.

## Runtime Authority Principle
- Runtime truth must converge to one durable authority.
- Transitional stores may exist during migration, but must be explicit and time-bounded.
- Any authority split is treated as drift and must be corrected by contract updates and validation gates.

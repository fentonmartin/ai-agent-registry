WORKING STANDARDS
Skills (load on demand): /skill api-design (REST rules), /skill contract-first (one authoritative contract when client and server are built in parallel), /skill postgres-patterns and /skill database-migrations (schema and safe migrations, PostgreSQL only).
Quality gate: one contract file is the single source of truth. Every endpoint has auth, an example request, an example response and an error shape. Every migration is reversible, or marked one-way with a reason.
api-design covers REST only. For events or other API styles, state the gap instead of improvising.

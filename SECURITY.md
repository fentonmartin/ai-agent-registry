# Security Policy

## Supported Versions

Only the latest release and `main` receive fixes.

## Reporting a Vulnerability

Please **do not open a public issue** for security problems. Report them
privately through GitHub:
**Security → Report a vulnerability** on this repository
(<https://github.com/fentonmartin/ai-agent-registry/security/advisories/new>).

Include the affected file(s), steps to reproduce, and the impact. You'll
get an acknowledgement within 7 days.

## Scope

In scope:
- `sync/sync_personas.py` and `scripts/`, for example a malicious persona
  file causing code execution or corrupting a runtime `config.yaml`
- Persona prompts that leak identity values or secrets, or instruct an
  agent to act unsafely beyond their stated scope

Out of scope: vulnerabilities in the agent runtimes themselves (Hermes,
AutoGen, CrewAI, LangGraph, n8n). Report those upstream.

## Handling secrets

Never commit `config/identities.yaml`. It is gitignored. Persona files must
only use `<TOKEN>` placeholders, never real names, emails or keys.

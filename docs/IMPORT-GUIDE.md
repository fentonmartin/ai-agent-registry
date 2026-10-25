# Import Guide

How to import the AI Agent Registry personas into various agent runtimes.

## Hermes Agent (Native Support)

The sync script (`sync/sync_personas.py`) was built for Hermes and handles
the full L0-L4 hierarchy import automatically.

### Prerequisites
- Hermes runtime installed
- `config.yaml` exists at `$HERMES_HOME/config.yaml`

### Steps
```bash
# 1. Configure identities
cp config/identities.example.yaml config/identities.yaml
# Edit with your values (user name, company, model, etc.)

# 2. Set environment
export HERMES_HOME=~/.hermes    # path to your Hermes config directory
export PERSONA_DIR=$(pwd)/personas  # optional: override persona source folder

# 3. Run sync
python sync/sync_personas.py

# 4. Verify
python sync/sync_personas.py --help
# Check config.yaml has agent.personalities block

# 5. Use in Hermes
/personality zan        # default voice
/personality ran-brand  # domain/trademark research
/personality ian-api    # API design
```

The sync script is idempotent — safe to run hourly via cron. It only writes
to `config.yaml` when personas actually change, and Hermes auto-reloads
on file mtime change.

### Hierarchy Integration

The sync script validates your `agent.hierarchy` block against the persona
set. Add this to your `config.yaml`:

```yaml
display:
  personality: zan    # default L0 voice (top-level key, not under agent:)

agent:
  hierarchy:
    L0:
      members: [zan, jan]
    L1:
      members: [ian, ban, ean, han, lan, pan, qan, ran, san, van, wan]
    L2:
      children:
        ian: [ian-api, ian-devops, ian-flutter, ian-plan, ian-alpha,
              ian-secred, ian-secblue, ian-ux, ian-ui]
        ran: [ran-people, ran-brand, ran-tech, ran-business, ran-web,
              ran-app, ran-general]
        lan: [lan-contract, lan-compliance, lan-ip]
    L3:
      members: []
    L4:
      members: []
    TEAM:
      members: []
```

The sync script places `agent.personalities` inside this same `agent:`
mapping, between `# >>> PERSONALITY SYNC` markers. Don't add a second
top-level `agent:` key. If you do, the sync refuses to write.

---

## AutoGen

AutoGen uses `AssistantAgent` with `system_message` parameters.

### Bulk Import Script
```python
import yaml, json, pathlib

# Load personas
persona_dir = pathlib.Path("personas")
agents = {}

for f in persona_dir.rglob("*.md"):
    src = f.read_text(encoding="utf-8")
    # Parse frontmatter + body
    if src.startswith("---"):
        parts = src.split("---\n", 2)
        if len(parts) >= 3:
            import yaml as y
            fm = y.safe_load(parts[1])
            body = parts[2].strip()
            if fm and fm.get("name"):
                agents[fm["name"]] = {
                    "name": fm["name"],
                    "system_message": body,
                    "title": fm.get("title", f.stem),
                }

# Create AutoGen agents
from autogen import AssistantAgent
agent_cache = {}
for key, cfg in agents.items():
    agent_cache[key] = AssistantAgent(
        name=cfg["name"],
        system_message=cfg["system_message"]
    )

# Now you can reference any persona:
# zan = agent_cache["zan"]
# ran_brand = agent_cache["ran-brand"]
```

### Single Persona
```python
from autogen import AssistantAgent

ran_brand = AssistantAgent(
    name="ran-brand",
    system_message=pathlib.Path("personas/l2/ran/ran-brand.md").read_text(encoding="utf-8").split("---\n", 2)[2].strip()
)
```

---

## CrewAI

CrewAI uses `Agent` objects with `role`, `goal`, and `backstory`.

### Converter
```python
from crewai import Agent
from pathlib import Path
import yaml as y

def import_persona(key: str, persona_dir="personas") -> Agent:
    """Import a single persona as a CrewAI Agent."""
    # Find the file
    for f in Path(persona_dir).rglob("*.md"):
        src = f.read_text(encoding="utf-8")
        if src.startswith("---"):
            parts = src.split("---\n", 2)
            if len(parts) >= 3:
                fm = y.safe_load(parts[1])
                body = parts[2].strip()
                if fm and fm.get("name") == key:
                    return Agent(
                        role=fm.get("title", fm["name"]),
                        goal=body,  # system prompt becomes the goal
                        backstory="",
                        verbose=False,
                    )
    raise ValueError(f"Persona '{key}' not found")

# Usage
ran_people = import_persona("ran-people")
```

**Note:** CrewAI's `Agent` model differs from prompt-based dispatch. The
persona's system prompt becomes the `goal` (or you can use `backstory`
for context and set `goal` to the persona's stated objective). The L0-L4
hierarchy is not natively supported in CrewAI — implement routing yourself
or use `CrewAI Hub` for agent orchestration.

---

## LangGraph

LangGraph uses `BaseStore` and prompt templates. Import persona prompts as
`ChatPromptTemplate` instances.

```python
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import yaml as y

def load_persona(key: str, persona_dir="personas"):
    """Load a persona prompt as a LangChain ChatPromptTemplate."""
    for f in Path(persona_dir).rglob("*.md"):
        src = f.read_text(encoding="utf-8")
        if src.startswith("---"):
            parts = src.split("---\n", 2)
            if len(parts) >= 3:
                fm = y.safe_load(parts[1])
                body = parts[2].strip()
                if fm and fm.get("name") == key:
                    return ChatPromptTemplate.from_messages([
                        ("system", body)
                    ])
    raise ValueError(f"Persona '{key}' not found")

# Usage in a LangGraph node
system_prompt = load_persona("ian-api")
result = llm.invoke(system_prompt.format())
```

---

## n8n

n8n's **AI Agent** node accepts a system prompt under
*Options → System Message*. You can load a persona into it at runtime:

1. **HTTP Request** node: `GET` the raw persona file, e.g.
   `https://raw.githubusercontent.com/fentonmartin/ai-agent-registry/main/personas/l2/ran/ran-brand.md`.
   Set *Response Format* to *Text*.
2. **Code** node: remove the frontmatter and substitute tokens:
   ```javascript
   const src = $input.first().json.data;
   const body = src.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim();
   const tokens = { USER: 'Alice', COMPANY: 'Acme' };   // your identities
   const prompt = body.replace(/<([A-Z_]+)>/g, (m, k) => tokens[k] ?? m);
   return [{ json: { prompt } }];
   ```
3. **AI Agent** node: set *System Message* to the expression
   `{{ $json.prompt }}`.

To pick the persona dynamically, put the persona path in the trigger
payload (for example a Webhook body field) and reference it in the HTTP
Request URL. Routing between L0, L1 and L2 is up to your workflow, for
example with a **Switch** node.

---

## Generic / Raw Import

If your runtime just needs the raw system prompt string:

```python
from pathlib import Path
import yaml as y

def get_persona_prompt(key: str, persona_dir="personas") -> str:
    """Return the raw system prompt for a persona key."""
    for f in Path(persona_dir).rglob("*.md"):
        src = f.read_text(encoding="utf-8")
        if src.startswith("---"):
            parts = src.split("---\n", 2)
            if len(parts) >= 3:
                fm = y.safe_load(parts[1])
                body = parts[2].strip()
                if fm and fm.get("name") == key:
                    return body
    raise ValueError(f"Persona '{key}' not found")

# Direct prompt use
prompt = get_persona_prompt("zan")
```

---

## Identity Token Substitution

Persona files contain tokens like `<USER>`, `<COMPANY>`, `<EMAIL>`, `<MODEL>`.
To resolve them for your environment:

```bash
cp config/identities.example.yaml config/identities.yaml
# Edit with your actual values

python sync/sync_personas.py  # auto-resolves tokens when syncing
```

For non-Hermes runtimes, substitute manually or write a simple token resolver:
```python
import yaml
config = yaml.safe_load(open("config/identities.yaml", encoding="utf-8"))
tokens = {k: v for section in config.values() if isinstance(section, dict)
          for k, v in section.items()}
for k, v in tokens.items():
    prompt = prompt.replace(f"<{k.upper()}>", str(v))
```

---

## Summary

| Runtime | Native Import | Hierarchy Support | Token Substitution |
|---------|--------------|-------------------|---------------------|
| Hermes | Yes (sync script) | Yes | Yes (built-in) |
| AutoGen | Manual script | No | Manual |
| CrewAI | Custom converter | No | Manual |
| LangGraph | Custom loader | No | Manual |
| n8n | HTTP Request + Code node | No (build with Switch) | Code node |
| Raw/Gateway | Direct prompt | No | Manual |

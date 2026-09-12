# Learnings — 01 LLM Playground

## New concepts

- **Stdout buffering**: `flush=True` forces immediate display. Without both, streaming looks broken.
- **Stateless model**: the LLM remembers nothing. `history` (resent every call) is
  the entire "memory". Same reason `todos` vanishes on quit — no persistence.
- **Streaming vs blocking**: `stream=True` yields chunks for live UX; blocking
  returns one object. Extraction uses blocking (need the whole JSON before parsing).
- **Structured output = 3 ingredients**: schema in the prompt + `format="json"` in
  the call + `json.loads` + validation. `format` guarantees *valid* JSON, only the
  prompt guarantees *your* JSON.
- **Defensive parsing layers**: `try/except JSONDecodeError` (is it JSON?) ->
  shape check with `isinstance` (is it *my* JSON?) -> per-item normalization.
- **Command-branch pattern**: `if prompt.startswith("/cmd"):` ... handle ...
  `continue`. The `continue` is the separator — without it the command leaks into
  `history`.

## Standard patterns (reuse in every LLM project)

**Blocking chat call:**
```python
response = ollama.chat(model=model, messages=history)
text = response.message.content
```

**Streaming chat loop:**
```python
response = ollama.chat(model=model, messages=history, stream=True)
full = ""
for chunk in response:
    token = chunk.message.content or ""
    full += token
    print(token, end="", flush=True)
print()
```

**Structured extraction call:**
```python
response = ollama.chat(
    model=model,
    messages=[{"role": "system", "content": SCHEMA_PROMPT},
              {"role": "user", "content": text}],
    format="json",
)
```

**Defensive parse:**
```python
try:
    reply = json.loads(response.message.content)
except json.JSONDecodeError:
    ...handle...
    continue
tasks = reply.get("tasks") if isinstance(reply, dict) else None
if not isinstance(tasks, list):
    ...handle...
    continue
for t in tasks:
    if not isinstance(t, dict):
        continue
    ...
```

**Command branch:**
```python
if prompt.startswith("/cmd"):
    ...handle with own messages, never touch history...
    continue
```

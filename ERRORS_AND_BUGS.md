# Errors & Bugs — 01 LLM Playground

Every error hit during this build, with cause and fix. Typos included — they cost real time.

## 1. Model name typos (404 / manifest errors)

- `ollama run qwen3-1.1.7b` -> `Error: pull model manifest: file does not exist`
- `model = 'qwen3-1.87b'` in code -> `ResponseError: model not found (404)`
- Cause: Ollama does exact matching; unknown names fall through to registry pull.
- Fix: `ollama list`, copy the name, never retype it.

## 2. `breal` instead of `break`

- Would-be `NameError` on quit. Caught by reading before running.

## 3. `response.messsage.content` instead of `response.message.content`

- Would-be `AttributeError` on first reply. Extra `s`.

## 4. Missing comma in dict literal

- `"role": "system" "content": ...` -> `SyntaxError`. Adjacent strings concatenate,
  so the parser chokes on the second colon. Hit twice (lines 14, 16 region).

## 5. Invalid role `"todo"`

- Roles are only `system` / `user` / `assistant`. Extraction needs two messages
  (system = schema, user = text), not one invented role.

## 6. Missing `messages=` in `ollama.chat` call

- Built the messages, never sent them. Built != sent.

## 7. Missing `import json`

- `json.loads` -> `NameError`. Import before use.

## 8. Branch fall-through / inverted `else: continue`

- First version: `/json` input fell through into `history`.
- Second version: `else: continue` killed normal chat instead.
- Fix: `continue` goes *inside* the command branch.

## 9. `else` paired with the wrong `if`

- `else:` after the `/todos` block paired with `startswith` (line 14), not the
  `len` check — so every normal message printed "No tasks yet".
- Fix: nest the empty/non-empty check fully inside the branch, then `continue`.

## 10. `streaming=True` instead of `stream=True`

- `TypeError` on every normal message. The ollama kwarg is `stream`.

## 11. `enum` instead of `enumerate`

- `NameError` on first `/todos` call.

## 12. `.get()` on a `json.dumps` string

- `result = json.dumps(reply)` is a `str` (display); `reply` is the `dict` (logic).
  `result.get("tasks")` -> `AttributeError`. Iterate the validated `tasks` list.

## 13. Untrusted chunk / item content

- Stream chunks can carry `None` content -> guard `chunk.message.content or ""`.
- Task list items can be non-dicts -> guard `isinstance(t, dict)`.

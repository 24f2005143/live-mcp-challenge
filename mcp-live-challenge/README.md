# Live MCP Challenge Server

A minimal Model Context Protocol (MCP) Streamable HTTP server exposing exactly one tool, `solve_challenge`.

The tool reads `X-Exam-Challenge` from the HTTP headers for each `tools/call` request and returns the first 16 lowercase hexadecimal characters of:

`SHA-256("<challenge>:24f2005143@ds.study.iitm.ac.in")`

## Deploy on Render

1. Upload the contents of this folder to the **root** of a new GitHub repository.
2. In Render, choose **New → Blueprint** and connect that repository.
3. The Blueprint file is `render.yaml` at the repository root.
4. Deploy. The MCP endpoint is `https://YOUR-SERVICE.onrender.com/mcp`.

For manual Web Service deployment instead, use:

- Build command: `pip install -r requirements.txt`
- Start command: `python server.py`

Render sets `PORT` automatically. Do not configure a fixed port.

## Local run

```bash
python -m pip install -r requirements.txt
python server.py
```

The endpoint will be `http://localhost:8000/mcp`.

## Important behavior

- `solve_challenge` takes no user-supplied arguments; `ctx` is injected by the MCP SDK and does not appear in the input schema.
- The challenge is read from the HTTP request headers on every tool call. It is not read from tool arguments and is not cached.
- Only the required tool is registered.

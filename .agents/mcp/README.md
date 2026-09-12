# MCP

Repository-scoped MCP server definitions.

## connected-workspace

External capabilities are provided by the [`connected-workspace-mcp`](https://www.npmjs.com/package/connected-workspace-mcp)
server, not by skills in this repo:

- **Gmail** — search, read, send, reply, modify labels
- **Google Calendar** — list, create, update, delete events, free/busy
- **LinkedIn** — read profile/posts/engagement, publish text/image, delete posts

Skills that need these capabilities (e.g. drafting a LinkedIn post to publish, or reading email
to summarize) call the MCP tools listed in `connected-workspace.json`.

Configure your MCP host to require confirmation for write tools (send email, modify calendar,
publish/delete posts).

Never commit API keys, access tokens, passwords, or private URLs containing credentials.

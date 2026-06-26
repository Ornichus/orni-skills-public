# Distribution

How to package and ship `web-pdf-compile` to a third party as a standalone skill.

## Build artifacts

Run from the skill folder :

```bash
# Universal ZIP (drag-and-drop install, anyone can extract)
powershell -Command "Compress-Archive -Path . -DestinationPath dist/web-pdf-compile-1.0.0.zip -Force"

# OR npm tarball (npm install ./web-pdf-compile-1.0.0.tgz works too)
npm pack --pack-destination dist
```

Both artifacts land in `dist/`. The folder is gitignored.

## What the recipient does

### Option A — universal ZIP

1. Extract `web-pdf-compile-1.0.0.zip` somewhere
2. Make sure Node.js 18+ and Google Chrome are installed
3. Run the bundled installer :
   - **Windows** : double-click `install.bat`
   - **macOS / Linux** : `bash install.sh` (or `./install.sh` after `chmod +x`)
4. Use it :
   ```bash
   npm run probe -- https://example.com/article
   npm run capture -- examples/smoke-test.json
   npm run compile -- examples/smoke-test.json
   ```

### Option B — npm tarball

```bash
mkdir my-project && cd my-project
npm init -y
npm install /path/to/web-pdf-compile-1.0.0.tgz
# now node_modules/web-pdf-compile/scripts/* are available
node node_modules/web-pdf-compile/scripts/probe-dom.js https://...
```

Or globally :
```bash
npm install -g /path/to/web-pdf-compile-1.0.0.tgz
# probes etc available via npx web-pdf-compile-* (no bin yet, see TODO below)
```

### Option C — drop-in skill folder

The recipient just copies the extracted folder into their AI agent's skill directory :
- Claude Code : `~/.claude/skills/web-pdf-compile/`
- Cursor / others : whatever skill path they use
- Then run `cd <path> && npm install` once.

The agent reads `SKILL.md` frontmatter and exposes the workflow to the LLM.

### Option D — Claude Desktop (MCP server, recommended for non-CLI users)

Best UX for non-developers. After `npm install`, the recipient adds one entry to their Claude Desktop config :

```json
{
  "mcpServers": {
    "web-pdf-compile": {
      "command": "node",
      "args": ["/absolute/path/to/scripts/mcp-server.js"]
    }
  }
}
```

Then restarts Claude Desktop. The model gains `web_pdf_probe` and `web_pdf_compile_dossier` tools.

Full step-by-step : `CLAUDE-DESKTOP-SETUP.md` (config file paths per OS, troubleshooting, usage examples).

## Embedded prerequisites

The skill is fully standalone EXCEPT for two system requirements that cannot be bundled :

| Requirement | Why | How to install |
|-------------|-----|----------------|
| **Node.js 18+** | Runtime | https://nodejs.org |
| **Google Chrome** (system install) | Puppeteer-core uses the system Chrome (lightweight, no Chromium bundle) | https://www.google.com/chrome/ |

If Chrome lives in a non-standard path, recipient sets `"chrome_path"` in their `sources.json`.

## Footprint after install

- Skill folder itself : ~50 KB
- `node_modules/` after `npm install` : ~150 MB (mostly puppeteer-core + sharp + adblocker)

## What's NOT in the package

- `node_modules/` (run `npm install` to fetch)
- `output/` (generated PDFs and per-source JPGs)
- `dist/` (build artifacts)
- `package-lock.json` (regenerated on `npm install`)

## Future work (not blocking distribution)

- Add a `bin` entry in `package.json` (`"bin": { "web-pdf-compile": "scripts/cli.js" }`) so a single `web-pdf-compile probe|capture|compile` CLI works after `npm install -g`
- Wrap as MCP server (stdio JSON-RPC) for plug-and-play in Claude Desktop / Claude Code MCP clients
- Publish to npm registry under a stable scope (`@your-org/web-pdf-compile`) so `npm install -g @your-org/web-pdf-compile` works without local file

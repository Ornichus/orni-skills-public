# Claude Desktop setup

Plug `web-pdf-compile` into Claude Desktop as an MCP server. Once configured, the LLM can call two tools directly :

- `web_pdf_probe` — suggest CSS selectors for a given article URL
- `web_pdf_compile_dossier` — capture a list of URLs and produce a PDF dossier

## Prerequisites

1. **Node.js 18+** ([nodejs.org](https://nodejs.org/))
2. **Google Chrome** (system install, used by Puppeteer)
3. **Claude Desktop** (latest version)

## Step 1 — install the skill

```bash
# From the extracted web-pdf-compile/ folder
cd /path/to/web-pdf-compile
```

Then either :
- **Windows** : double-click `install.bat`
- **macOS / Linux** : `bash install.sh`

This runs `npm install` (~150 MB of deps : puppeteer-core, sharp, pdf-lib, MCP SDK, ghostery adblocker).

## Step 2 — find the absolute path to `mcp-server.js`

```bash
# From inside web-pdf-compile/
# Windows (Powershell)
Resolve-Path scripts\mcp-server.js

# macOS / Linux
realpath scripts/mcp-server.js
```

Copy the absolute path printed. Example :
- Windows : `C:\Users\you\Tools\web-pdf-compile\scripts\mcp-server.js`
- macOS : `/Users/you/Tools/web-pdf-compile/scripts/mcp-server.js`
- Linux : `/home/you/tools/web-pdf-compile/scripts/mcp-server.js`

## Step 3 — edit `claude_desktop_config.json`

Location of the config file :
- **Windows** : `%APPDATA%\Claude\claude_desktop_config.json` (typically `C:\Users\<you>\AppData\Roaming\Claude\claude_desktop_config.json`)
- **macOS** : `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux** : `~/.config/Claude/claude_desktop_config.json`

Open the file in any text editor. If it doesn't exist yet, create it.

Add a `mcpServers` entry pointing at the absolute path :

```json
{
  "mcpServers": {
    "web-pdf-compile": {
      "command": "node",
      "args": [
        "C:\\Users\\you\\Tools\\web-pdf-compile\\scripts\\mcp-server.js"
      ]
    }
  }
}
```

If the file already has other servers, just add `web-pdf-compile` inside the existing `mcpServers` object :

```json
{
  "mcpServers": {
    "filesystem": { "command": "...", "args": [...] },
    "web-pdf-compile": {
      "command": "node",
      "args": ["/absolute/path/to/scripts/mcp-server.js"]
    }
  }
}
```

> **Windows users** : escape backslashes in JSON (`\\`) or use forward slashes (`/`). Both work.

## Step 4 — restart Claude Desktop

Quit Claude Desktop fully (system tray, not just close window) and relaunch it. The MCP server starts automatically.

## Step 5 — verify

In a Claude Desktop conversation, type :

> List the MCP tools you have access to.

Claude should mention `web_pdf_probe` and `web_pdf_compile_dossier`.

## Usage examples

### Quick — let Claude do everything

> Compile a PDF dossier titled "Research dossier" from these articles :
>
> - https://en.wikipedia.org/wiki/Photosynthesis
> - https://www.gnu.org/philosophy/free-sw.html
>
> Probe each URL first to find the right selectors, then capture and compile. Save the PDF to `~/Desktop/research-dossier`.

Claude will :
1. Call `web_pdf_probe` once per URL to discover selectors
2. Call `web_pdf_compile_dossier` with the assembled config
3. Report the resulting PDF path + page count

### Direct — provide selectors yourself

> Use `web_pdf_compile_dossier` with this config :
> - title : "Test"
> - sources : `[{ url: "https://en.wikipedia.org/wiki/Test", selectors: ["#content"], country: "WW" }]`
> - country_order : `[{ code: "WW", name: "Worldwide" }]`

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Tools don't appear after restart | Path in config not absolute or contains unescaped backslashes | Use forward slashes or `\\` — restart Claude Desktop |
| `Pipeline failed: Chrome not found` | Chrome not installed at standard location | Install Chrome OR add `"chrome_path": "/your/chrome"` inside each `sources[N]` entry — but the MCP server doesn't expose this yet, so easiest is to install Chrome at the default path |
| `npm install` fails on `sharp` | Native binary missing for your platform | Install Visual Studio build tools (Windows) or `apt install build-essential libvips-dev` (Debian/Ubuntu) |
| Server starts but tool calls hang | Adblock filter download is slow on first run | First call may take 30-60 s while Ghostery downloads EasyList — be patient or pre-warm with a CLI run |
| Output PDF goes to skill folder unexpectedly | `output_dir` was relative | Always pass an absolute path for production usage |

## Security note

The MCP server runs Puppeteer with full network access on your machine. Only feed it URLs you trust. The server does NOT bypass paywalls, captchas, or login walls. Output writes only to the `output_dir` you specify.

## Updating

When a new version ships :
1. Replace the skill folder with the new one
2. `cd web-pdf-compile && npm install`
3. Restart Claude Desktop (the config path doesn't change)

No need to edit `claude_desktop_config.json` again.

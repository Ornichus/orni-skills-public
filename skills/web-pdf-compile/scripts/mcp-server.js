#!/usr/bin/env node
/**
 * web-pdf-compile — MCP server (stdio transport)
 *
 * Exposes the skill as Model Context Protocol tools so it can be plugged
 * directly into Claude Desktop, Claude Code, Cursor, or any MCP-compatible
 * client.
 *
 * Tools exposed :
 *  - web_pdf_probe          : suggest CSS selectors for an article URL
 *  - web_pdf_compile_dossier: full pipeline (capture + PDF) from a list of URLs
 *
 * Setup (Claude Desktop) :
 *   1. Run `npm install` once in the skill folder.
 *   2. Add to claude_desktop_config.json :
 *      {
 *        "mcpServers": {
 *          "web-pdf-compile": {
 *            "command": "node",
 *            "args": ["/absolute/path/to/scripts/mcp-server.js"]
 *          }
 *        }
 *      }
 *   3. Restart Claude Desktop.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_ROOT = path.resolve(__dirname, '..');

/* --------------------------------------------------------------------- */
/* Helpers                                                               */
/* --------------------------------------------------------------------- */

function runNode(scriptName, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(SKILL_ROOT, 'scripts', scriptName);
    const child = spawn('node', [scriptPath, ...args], {
      cwd: opts.cwd || SKILL_ROOT,
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (b) => { stdout += b.toString(); });
    child.stderr.on('data', (b) => { stderr += b.toString(); });
    child.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`${scriptName} exited ${code}\n${stderr || stdout}`));
    });
  });
}

function writeTempConfig(config) {
  const tmpDir = path.join(os.tmpdir(), 'web-pdf-compile-mcp');
  fs.mkdirSync(tmpDir, { recursive: true });
  const file = path.join(
    tmpDir,
    `cfg-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.json`,
  );
  fs.writeFileSync(file, JSON.stringify(config, null, 2));
  return file;
}

function buildSourcesConfig(args) {
  const out = path.isAbsolute(args.output_dir || '')
    ? args.output_dir
    : path.join(args.output_dir || './output/dossier');
  return {
    title: args.title || 'Dossier',
    subtitle: args.subtitle || '',
    output_dir: out,
    country_order: args.country_order || [{ code: 'WW', name: 'Worldwide' }],
    sources: (args.sources || []).map((s, i) => ({
      id: s.id || String(i + 1).padStart(2, '0'),
      shortname: s.shortname || `source-${i + 1}`,
      country: s.country || 'WW',
      url: s.url,
      selectors: s.selectors && s.selectors.length
        ? s.selectors
        : ['main', 'article', '#content', '.post-content', '.article-body'],
      extraRemove: s.extraRemove || [
        'header', 'footer', 'nav', 'aside',
        '.sidebar', '.comments', '.related-posts',
        '.social-share', '.newsletter',
      ],
      longwait: s.longwait === true,
      useHeuristic: s.useHeuristic === true,
      source: s.source || null,
    })),
  };
}

/* --------------------------------------------------------------------- */
/* MCP server                                                            */
/* --------------------------------------------------------------------- */

const server = new Server(
  { name: 'web-pdf-compile', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'web_pdf_probe',
      description:
        'Probe a web article URL and return suggested CSS selectors for the article body and elements to remove (sidebars, ads, comments). Use this BEFORE compile_dossier when adding a new site to a dossier, to find the right selectors. Returns text output containing a JSON suggestion block.',
      inputSchema: {
        type: 'object',
        properties: {
          url: {
            type: 'string',
            description: 'Full URL of the article to probe',
          },
        },
        required: ['url'],
      },
    },
    {
      name: 'web_pdf_compile_dossier',
      description:
        'Full pipeline : capture a list of web articles cleanly (article-only, no ads/sidebar/comments) and compile them into a single PDF dossier organized by country or category. Returns the absolute path of the generated PDF.',
      inputSchema: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: 'Title shown on the PDF cover page',
          },
          subtitle: {
            type: 'string',
            description: 'Optional subtitle on the cover page',
          },
          output_dir: {
            type: 'string',
            description:
              'Where to write articles/, COMPILATION.pdf, results.json. Defaults to ./output/dossier (relative to skill root). Use absolute paths to write outside the skill folder.',
          },
          country_order: {
            type: 'array',
            description:
              'Order in which countries are grouped on the cover TOC. Each entry is { code: "FR", name: "France" }. If omitted, all sources go under "Worldwide".',
            items: {
              type: 'object',
              properties: {
                code: { type: 'string' },
                name: { type: 'string' },
              },
              required: ['code', 'name'],
            },
          },
          sources: {
            type: 'array',
            description:
              'List of articles to capture. Each source needs at least a url; selectors and extraRemove default to common patterns. Run web_pdf_probe first to get tight selectors per site.',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string', description: 'Optional 2-digit id, auto-generated if omitted' },
                shortname: { type: 'string', description: 'Short slug for filenames' },
                country: { type: 'string', description: 'Country code matching country_order, defaults to WW' },
                url: { type: 'string', description: 'Article URL' },
                selectors: {
                  type: 'array',
                  description: 'Ordered CSS selectors for the article body. First match wins.',
                  items: { type: 'string' },
                },
                extraRemove: {
                  type: 'array',
                  description: 'Extra CSS selectors to delete before capture (sidebars, ads).',
                  items: { type: 'string' },
                },
                longwait: {
                  type: 'boolean',
                  description: 'Wait 8s instead of 5s after page load (for SPA / JS-heavy sites).',
                },
                useHeuristic: {
                  type: 'boolean',
                  description: 'Fallback to text-density heuristic if no selector matches.',
                },
                source: {
                  type: 'string',
                  description: 'Set to "wayback" if the URL is a Wayback Machine snapshot.',
                },
              },
              required: ['url'],
            },
          },
        },
        required: ['title', 'sources'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'web_pdf_probe') {
    if (!args || !args.url) {
      return { content: [{ type: 'text', text: 'Missing required argument: url' }], isError: true };
    }
    try {
      const { stdout, stderr } = await runNode('probe-dom.js', [args.url]);
      return { content: [{ type: 'text', text: (stdout + (stderr ? '\n' + stderr : '')).trim() }] };
    } catch (e) {
      return { content: [{ type: 'text', text: `Probe failed: ${e.message}` }], isError: true };
    }
  }

  if (name === 'web_pdf_compile_dossier') {
    if (!args || !Array.isArray(args.sources) || !args.sources.length) {
      return {
        content: [{ type: 'text', text: 'Missing or empty sources[]' }],
        isError: true,
      };
    }
    if (!args.title) {
      return { content: [{ type: 'text', text: 'Missing required argument: title' }], isError: true };
    }

    const config = buildSourcesConfig(args);
    const cfgPath = writeTempConfig(config);

    try {
      const captureResult = await runNode('capture.js', [cfgPath]);
      const compileResult = await runNode('compile-pdf.js', [cfgPath]);

      const outDir = path.isAbsolute(config.output_dir)
        ? config.output_dir
        : path.resolve(SKILL_ROOT, config.output_dir);
      const pdfPath = path.join(outDir, 'COMPILATION.pdf');
      const pdfExists = fs.existsSync(pdfPath);
      const pdfSizeKB = pdfExists
        ? Math.round(fs.statSync(pdfPath).size / 1024)
        : 0;

      const summary = [
        '=== web_pdf_compile_dossier ===',
        '',
        '--- Capture ---',
        captureResult.stdout.trim(),
        '',
        '--- Compile ---',
        compileResult.stdout.trim(),
        '',
        `PDF : ${pdfPath} (${pdfExists ? pdfSizeKB + ' KB' : 'NOT FOUND'})`,
      ].join('\n');

      return { content: [{ type: 'text', text: summary }], isError: !pdfExists };
    } catch (e) {
      return {
        content: [{ type: 'text', text: `Pipeline failed: ${e.message}` }],
        isError: true,
      };
    } finally {
      try { fs.unlinkSync(cfgPath); } catch {}
    }
  }

  return {
    content: [{ type: 'text', text: `Unknown tool: ${name}` }],
    isError: true,
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);

// Stay alive on stdio
process.stdin.on('end', () => process.exit(0));

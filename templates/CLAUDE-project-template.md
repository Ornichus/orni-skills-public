# {{PROJECT_NAME}}

> **Project ID** `{{PROJECT_ID}}` · **Bootstrap** `/orni-init-claude-md` v2.0 (DENSE-POINTEURS) · **Sync** {{LAST_SYNC_DATE}}
> **Style/communication** : `~/.claude/CLAUDE.md` (pyramide inversée, vulgarisation, caveman INTERNE/EXTERNE, VPS inventory, browser policy)
> **Guide écosystème** : `{{ORNI_PATH}}/docs/GUIDE-UTILISATION.md` (catalogue §4 · décisionnaire §4.5 · architecture)

---

<!-- ORNI-CLAUDE-MD-START:framework -->
## Framework par cas (1 par session, mutuellement exclusifs)

| Cas | Framework | Pointeur |
|-----|-----------|----------|
| MVP exploratoire · side-project · requirements shift · outil interne · hackathon | **GSD** | `/orni-init-gsd` + `/gsd-new-project` · détails `{{ORNI_PATH}}/skills/gsd/SKILL.md` §1 |
| CRM client · SaaS B2B · community · migration legacy · e-commerce classique | **BMAD** | inclus `/orni-init-full` · `/bmad-help` |
| Paiement · IA agentique · pipeline data critique · API publique · refactor financier | **Superpowers** | skill `superpowers:using-superpowers` (plugin global) |
| Scripts utilitaires · pages statiques · features triviales | **aucun** | direct Claude Code |

> Mix possible entre sessions, pas dans la même.
<!-- ORNI-CLAUDE-MD-END:framework -->

---

<!-- ORNI-CLAUDE-MD-START:modules -->
## Modules Orni installés

Source : `.claude/orni-manifest.json` · regen via `/orni-init-claude-md --refresh-modules`

{{MODULES_TABLE_DENSE}}

**Catalogue complet** : `{{ORNI_PATH}}/docs/GUIDE-UTILISATION.md` §4 · `/orni-help`
<!-- ORNI-CLAUDE-MD-END:modules -->

---

<!-- ORNI-CLAUDE-MD-START:tooling -->
## Outil par besoin (use-case → tool · pointeur détail)

| Besoin | Outil | Détail |
|--------|-------|--------|
| Présentation client one-shot stylée | `/frontend-slides` | `{{ORNI_PATH}}/skills/frontend-slides/SKILL.md` |
| Deck reproductible versionné | `/marp-slides` | `{{ORNI_PATH}}/skills/marp-presentations/SKILL.md` |
| Brand book A4 + design system | `/design-system` | `{{ORNI_PATH}}/skills/design-system/SKILL.md` |
| Compiler articles web → PDF dossier | `/web-pdf-compile` | `{{ORNI_PATH}}/skills/web-pdf-compile/SKILL.md` |
| Génération image | MCP `fal-image-gen` | `{{ORNI_PATH}}/skills/fal-image-gen/SKILL.md` |
| Déploiement VPS+CF+HTTPS | `/deploy` | `{{ORNI_PATH}}/skills/deploy/SKILL.md` |
| DNS Cloudflare | `/cloudflare` | `{{ORNI_PATH}}/skills/cloudflare/SKILL.md` |
| Mailbox inter-projets async | `/mail-send` `/mail-read` `/mail-send-live` | `{{ORNI_PATH}}/skills/mailbox/SKILL.md` |
| Équipe agents délibérative | `/ateam-council` | `{{ORNI_PATH}}/skills/ateam/SKILL.md` |
| Brainstorm structuré avant code | skill `superpowers:brainstorming` | plugin global |
| Debug systématique état persistant | skill `superpowers:systematic-debugging` ou `/gsd-debug` | plugin / GSD |
| TDD edge cases | skill `superpowers:test-driven-development` | plugin global |
| Automation web vrai navigateur | MCP `claude-in-chrome` | `{{ORNI_PATH}}/skills/agent-browser/SKILL.md` |
| Diagrammes Excalidraw | `/excal-diagram` | `{{ORNI_PATH}}/skills/excal-diagram/SKILL.md` |
| Diagrammes Mermaid in-deck | section Mermaid dans `/marp-slides` ou `/frontend-slides` v1.4.0+ | docs des skills |
| Bootstrap CLAUDE.md projet | `/orni-init-claude-md` | ce fichier (auto-référent) |
| Orchestrer tâches en waves + routing framework + `/goal` autonome | `/orchestrate` | `{{ORNI_PATH}}/skills/task-orchestrator/SKILL.md` |
| Restructure prompt vague | `/structure` | `{{ORNI_PATH}}/commands/structure.md` |

**Décisionnaire par catégorie** : `{{ORNI_PATH}}/docs/GUIDE-UTILISATION.md` §4.5
<!-- ORNI-CLAUDE-MD-END:tooling -->

---

<!-- ORNI-CLAUDE-MD-START:reflexes -->
## Réflexes session

| Action | Commande |
|--------|----------|
| Reprise / nouvelle session | `/followup` |
| Finir bloc / avant `/compact` | `/update-all` |
| Audit conversation vs code | `/update-prd` |
| Diagnostic state.xml ↔ fichiers réels | `/followup-doctor` |
| Catalogue commandes | `/orni-help` |
| Snapshot projet | `/orni-status` |

**Protocole détaillé** : `{{ORNI_PATH}}/docs/GUIDE-UTILISATION.md` §1-3
<!-- ORNI-CLAUDE-MD-END:reflexes -->

---

## Tech stack
{{LANGUAGES}} · {{APP_FRAMEWORKS}} · {{DATABASES}} · {{INFRA}} · {{TESTS}}

## Conventions projet
*(libre — naming, branches, tests obligatoires, etc.)*

## Anti-patterns projet
*(libre — ce qu'il ne faut PAS faire ici)*

## Mémoire persistance
`project-state.xml` · `MEMORY.md` (auto-memory cross-session) · `~/.claude/mailbox/{{PROJECT_SLUG}}/` · `docs/_backup/audit-reports/`

## Notes projet
*(libre, préservé par `--augment`)*
{{USER_NOTES_PRESERVED}}

---
description: 'Initialise le module Multi-Backend Claude Code (cdsp/odsp + OpenRouter routing) globalement (PowerShell profile + ~/.claude/backend_keys.json)'
---

# /orni-init-mb - Initialiser Multi-Backend Claude Code

Installe les helpers PowerShell `cdsp` (Anthropic native) et `odsp` (OpenRouter, tout modele) plus les utilitaires `odsp-models`, `dsp-status`, `dsp-reset`. **Install GLOBAL** (modifie `$PROFILE`), pas par-projet.

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md` (logique commune Orni)
   - Charger `~/.claude/skills/multi-backend/INSTALL.md` (procedure detaillee multi-backend, IMPORTANT)
   - Charger `~/.claude/skills/multi-backend/SKILL.md` (reference fonctionnelle)

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` pour obtenir `source_path` -> `{ORNI}`
   - Si absent : demander le chemin a l'utilisateur et creer le fichier

3. **Pre-vol (cf. INSTALL.md section 1):**
   - Verifier OS = Windows. Sinon : abort avec message *"Multi-backend supporte uniquement Windows + PowerShell pour l'instant"*
   - Verifier `Get-Command claude` pas vide. Sinon : indiquer install via `npm install -g @anthropic-ai/claude-code`
   - Verifier `{ORNI}/skills/multi-backend/profile-snippet.ps1` existe

4. **Detecter le vrai $PROFILE (cf. INSTALL.md section 2):**

   **CRITIQUE — la redirection OneDrive Documents fait que `~/Documents/PowerShell/` et `~/OneDrive/Documents/PowerShell/` peuvent coexister avec des contenus differents.**

   Executer (via Bash tool) :
   ```bash
   pwsh -NoProfile -Command "Write-Output \$PROFILE"
   ```

   Recuperer le path retourne -> `$PROFILE_PATH`. Si pwsh 7 absent, fallback :
   ```bash
   powershell -NoProfile -Command "Write-Output \$PROFILE"
   ```

   Demander a l'utilisateur s'il utilise aussi Windows PowerShell 5.1. Si oui, recuperer aussi son `$PROFILE` et installer sur les deux.

5. **Injection idempotente du bloc (cf. INSTALL.md section 3a):**

   Le snippet est encadre par `# ORNI-MB-START vX.Y.Z` et `# ORNI-MB-END`.

   - Si `$PROFILE_PATH` n'existe pas : creer le fichier et son parent (`New-Item -ItemType File -Force`)
   - Si le fichier contient deja `# ORNI-MB-START` : ABORTER avec message *"deja installe — utiliser /orni-update-mb pour mettre a jour"*
   - Sinon : appendre une ligne vide + le contenu de `{ORNI}/skills/multi-backend/profile-snippet.ps1` a la fin du fichier
   - Verifier syntaxe :
     ```powershell
     $tokens = $null; $errors = $null
     [System.Management.Automation.Language.Parser]::ParseFile('$PROFILE_PATH', [ref]$tokens, [ref]$errors) | Out-Null
     if ($errors.Count -gt 0) { throw "Profile parse errors after injection" }
     ```

6. **Backend keys file (cf. INSTALL.md section 3b):**
   - Copier `{ORNI}/skills/multi-backend/backend_keys.json.template` vers `~/.claude/backend_keys.json.template` (toujours)
   - Si `~/.claude/backend_keys.json` absent : copier le template vers ce path
   - Si present : ne PAS toucher (preserve la cle reelle de l'utilisateur)

7. **Verification (cf. INSTALL.md section 4):**
   ```bash
   pwsh -NoProfile -Command ". '$PROFILE_PATH'; @('cdsp','odsp','odsp-models','dsp-status','dsp-reset') | ForEach-Object { if (-not (Get-Command \$_ -ErrorAction SilentlyContinue)) { Write-Error \"Missing: \$_\"; exit 1 } }; Write-Output OK"
   ```

   Si echec : restaurer le profile depuis le backup pre-injection (effectuer un backup `.bak` avant edit).

8. **Mettre a jour le manifeste de versioning:**
   - Lire `.claude/orni-manifest.json` (cf. orni-installer SKILL.md). Note : ce module est GLOBAL, donc le manifeste pertinent est dans `~/.claude/orni-manifest.json` ou similaire — verifier convention orni-installer.
   - Extraire la version depuis frontmatter de `{ORNI}/skills/multi-backend/SKILL.md` (pattern `version: X.Y.Z`)
   - Ajouter / mettre a jour entree :
     ```json
     {
       "modules": {
         "multi-backend": {
           "version": "X.Y.Z",
           "installed_at": "<ISO 8601>",
           "updated_at": "<ISO 8601>",
           "profile_path": "<PROFILE_PATH detecte>"
         }
       }
     }
     ```

9. **Rapport (format SKILL.md section 8):**
   ```
   ## Multi-Backend Claude Code — install

   | Composant | Statut |
   |---|---|
   | $PROFILE injecte | <PROFILE_PATH> (bloc ORNI-MB-START vX.Y.Z ajoute) |
   | backend_keys.json | <cree depuis template | deja present> |
   | Fonctions chargees | cdsp ✓ odsp ✓ odsp-models ✓ dsp-status ✓ dsp-reset ✓ |

   **Etapes suivantes (a faire par l'utilisateur):**
   1. Ouvrir un NOUVEAU terminal pwsh (ou `. $PROFILE` dans l'actuel)
   2. (Si keys file fraichement cree) Editer `~/.claude/backend_keys.json` et coller la cle OpenRouter (https://openrouter.ai/keys)
   3. Test : `odsp-models` doit lister les alias
   4. Test E2E : `odsp deepseek -p "hi"` doit reussir (cout ~$0.18)

   **Commandes disponibles:**
   - `cdsp` — Claude Code via Anthropic native (Max plan quota)
   - `odsp [alias|model-id]` — Claude Code via OpenRouter
   - `odsp-models` — liste des alias OR
   - `dsp-status` / `dsp-reset` — inspection / reset env
   ```

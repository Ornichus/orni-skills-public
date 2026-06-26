---
description: 'Met a jour le module Multi-Backend Claude Code dans le PowerShell profile (refresh aliases, fonctions)'
---

# /orni-update-mb - Mettre a jour Multi-Backend Claude Code

Met a jour le bloc `# ORNI-MB-START` ... `# ORNI-MB-END` dans `$PROFILE` avec la version courante du snippet (refresh alias OR, corrections de bugs, nouvelles fonctions).

## Instructions

1. **Lire le skill d'installation:**
   - Charger `~/.claude/skills/orni-installer/SKILL.md`
   - Charger `~/.claude/skills/multi-backend/INSTALL.md` (sections 2, 3a, 4 surtout)
   - Charger `~/.claude/skills/multi-backend/SKILL.md`

2. **Resoudre le chemin source:**
   - Lire `~/.claude/orni-skills.json` -> `{ORNI}`

3. **Pre-vol:**
   - Verifier OS = Windows
   - Verifier `{ORNI}/skills/multi-backend/profile-snippet.ps1` existe
   - Detecter `$PROFILE_PATH` via `pwsh -NoProfile -Command "Write-Output \$PROFILE"` (fallback PS 5.1 si besoin)
   - Verifier que `$PROFILE_PATH` contient `# ORNI-MB-START`. Si ABSENT : suggerer `/orni-init-mb` puis abandonner.
   - Si l'utilisateur a installe sur pwsh 7 ET PS 5.1, traiter les deux profiles.

4. **Backup pre-update:**
   ```powershell
   Copy-Item '$PROFILE_PATH' '$PROFILE_PATH.orni-mb.bak' -Force
   ```

5. **Remplacer le bloc:**

   - Lire le contenu courant de `$PROFILE_PATH`
   - Localiser `# ORNI-MB-START` (debut du bloc)
   - Localiser `# ORNI-MB-END` (fin du bloc)
   - Si `# ORNI-MB-END` absent : ABORTER avec *"profile corrompu — backup .orni-mb.bak preserve, intervention manuelle requise"*
   - Remplacer toute la sous-chaine entre START et END inclus par le contenu de `{ORNI}/skills/multi-backend/profile-snippet.ps1`
   - **NE PAS TOUCHER** au reste du fichier (autres fonctions PS, custom user code)

6. **Verification syntaxe:**
   ```powershell
   $tokens = $null; $errors = $null
   [System.Management.Automation.Language.Parser]::ParseFile('$PROFILE_PATH', [ref]$tokens, [ref]$errors) | Out-Null
   if ($errors.Count -gt 0) { Restore-Backup; throw "Parse errors after update" }
   ```

7. **Verification fonctionnelle:**
   ```bash
   pwsh -NoProfile -Command ". '$PROFILE_PATH'; @('cdsp','odsp','odsp-models','dsp-status','dsp-reset','_orResolveModel','_ccGetKey') | ForEach-Object { if (-not (Get-Command \$_ -ErrorAction SilentlyContinue)) { Write-Error \"Missing: \$_\"; exit 1 } }; Write-Output OK"
   ```

   Si echec : restaurer depuis `.orni-mb.bak`.

8. **Backend keys file:**
   - **NE PAS TOUCHER** `~/.claude/backend_keys.json` (preserve la cle utilisateur)
   - Mettre a jour `~/.claude/backend_keys.json.template` (refresh structure si elle a change)

9. **Mettre a jour le manifeste:**
   - Lire le manifeste (ou `~/.claude/orni-manifest.json` si convention global)
   - Extraire nouvelle version depuis frontmatter `{ORNI}/skills/multi-backend/SKILL.md`
   - Mettre a jour `version` et `updated_at` (conserver `installed_at`)

10. **Rapport:**
    ```
    ## Multi-Backend Claude Code — update

    | Composant | Statut |
    |---|---|
    | $PROFILE | <PROFILE_PATH> (bloc remplace : vX.Y.Z -> vN.M.P) |
    | Backup | <PROFILE_PATH>.orni-mb.bak (a conserver 24h) |
    | backend_keys.json | preserve (intact) |
    | Fonctions verifiees | cdsp ✓ odsp ✓ odsp-models ✓ dsp-status ✓ dsp-reset ✓ |

    **Recharger les fonctions:**
    - `. $PROFILE` dans le shell courant
    - OU fermer + rouvrir pwsh

    **Changements vs version precedente:** voir CHANGELOG dans `{ORNI}/skills/multi-backend/SKILL.md`
    ```

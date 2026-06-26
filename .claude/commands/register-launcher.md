---
name: register-launcher
description: Enregistre le projet courant dans orni-dashboard (systray launcher)
---

# Register Launcher

Tu dois enregistrer le projet courant dans le systray launcher orni-dashboard.

## Étapes

1. **Scanne** le dossier courant pour trouver les scripts de lancement :
   - Cherche : `start*.bat`, `stop*.bat`, `launcher*.bat`, `run*.bat`, `start*.ps1`, `start*.sh`
   - Utilise Glob pour les trouver

2. **Analyse** le contenu des scripts trouvés :
   - Extrais les numéros de port (regex : `port\s*[=:]\s*(\d+)`, `localhost:(\d+)`, `--port\s+(\d+)`)
   - Extrais les URLs frontend (regex : `http://localhost:\d+`)
   - Identifie le start_cmd principal et le stop_cmd

3. **Propose** la configuration au user :
   ```
   Projet détecté : [nom du dossier]
   Chemin : [chemin absolu]
   Start : [fichier détecté]
   Stop : [fichier détecté ou "non détecté"]
   Ports : [liste des ports]
   URL frontend : [URL détectée ou "non détectée"]
   ```

4. **Demande validation** au user avec AskUserQuestion

5. **Écris** dans `~/.orni/projects.json` :
   ```bash
   python -c "
   import json
   from pathlib import Path
   f = Path.home() / '.orni' / 'projects.json'
   data = json.loads(f.read_text()) if f.exists() else {'projects': []}
   project = {
       'name': '[NOM]',
       'path': '[CHEMIN]',
       'start_cmd': '[START_CMD]',
       'stop_cmd': '[STOP_CMD]',
       'ports': [PORTS],
       'frontend_url': '[URL]',
       'auto_open': False,
       'category': 'dev'
   }
   data['projects'] = [p for p in data['projects'] if p['name'] != project['name']]
   data['projects'].append(project)
   f.write_text(json.dumps(data, indent=2))
   print('Projet enregistre dans orni-dashboard!')
   "
   ```

6. **Confirme** l'enregistrement au user.

---
description: 'Met à jour Archon MCP et project-state.xml avec les changements récents'
---

# /update - Mise à jour Archon et Project State

Met à jour le suivi du projet dans Archon MCP et le fichier project-state.xml du projet courant.

## Instructions

1. **Identifier le projet courant:**
   - Lire `CLAUDE.md` à la racine du projet pour trouver l'**Archon Project ID**
   - Pattern à chercher: `**Archon Project ID:** \`xxx-xxx-xxx\``
   - Si non trouvé, demander à l'utilisateur

2. **Demander un résumé** à l'utilisateur de ce qui a été accompli (si pas déjà clair du contexte)

3. **Mettre à jour Archon MCP:**
   - Utiliser `find_tasks(project_id="<ID trouvé dans CLAUDE.md>")` pour voir les tâches actuelles
   - Mettre à jour les tâches avec `manage_task("update", task_id="...", status="done", description="...")`
   - Créer de nouvelles tâches si nécessaire avec `manage_task("create", ...)`

4. **Backup project-state.xml AVANT modification:**
   - Si `{project-root}/project-state.xml` existe:
     - Créer `_backup/project-state/archive/` et `_backup/project-state/current/` si absents (mkdir -p)
     - Copier vers `_backup/project-state/archive/project-state_{YYYY-MM-DD}_{HH-MM-SS}.xml` (horodatage UTC)
     - Copier vers `_backup/project-state/current/project-state_latest.xml` (écrase le précédent)

5. **Mettre à jour project-state.xml:**
   - Chemin: `{project-root}/project-state.xml` (fichier local au projet)
   - Si le fichier n'existe pas, le créer avec la structure de base
   - Mettre à jour:
     - `<last-updated>` avec la date/heure actuelle (format ISO 8601)
     - `<session-id>` si nouvelle session
     - `<current-objective>` si l'objectif a changé
     - `<tasks>` statuts des sous-tâches
     - `<history>` ajouter les événements récents
     - `<completed-milestone>` si un milestone est terminé
     - `<last-conversation>` avec les 3 derniers messages échangés (voir ci-dessous)
   - Sauvegarder les modifications

5b. **Mettre a jour project-status.json (si PSS installe):**
   - Verifier si `{project-root}/project-status.json` existe
   - Si NON : passer cette etape silencieusement (PSS non installe)
   - Si OUI :
     a. Lire le fichier existant
     b. Si `current.snapshot_date` n'est PAS null (snapshot precedent existe) :
        - Condenser `current` en objet historique : garder `snapshot_date`, `session`, `phase`, `summary`, et extraire `key_decisions` depuis `decisions[].topic + ": " + decisions[].result`
        - Inserer cet objet en position 0 de `history`
        - Si `history` depasse 3 entrees, supprimer la derniere (la plus ancienne)
     c. Remplir `current` :
        - `snapshot_date` : date/heure courante ISO 8601
        - `session` : depuis `<session-id>` de project-state.xml (ou "unknown")
        - `phase` : depuis `<phase>` ou `<current-objective><status>` de project-state.xml
        - `question` : synthetiser l'objectif principal depuis `<current-objective>` ou contexte conversation
        - `summary` : synthese en 1 phrase de ce qui a ete accompli (depuis le resume de l'etape 2)
        - `decisions` : decisions/choix significatifs identifies dans la session (topic, analysis, result, status)
        - `next_actions` : taches Archon avec status=todo (top 3-5)
        - `blockers` : depuis le contexte (vide si aucun)
        - `metrics.progress_percent` : depuis `<progress-percent>` de project-state.xml si disponible
     d. Ecrire le fichier mis a jour
   - Ne PAS ajouter de confirmation separee (le rapport final mentionne le fichier)

6. **Capturer les 3 derniers messages de la conversation:**
   - Remonter dans le contexte de conversation actuel
   - Identifier les 3 derniers messages échangés entre l'utilisateur et l'agent (AVANT l'appel à /update)
   - Ne PAS inclure le message /update lui-même
   - Écrire ces messages dans la section `<last-conversation>` du XML
   - Format:
     ```xml
     <last-conversation updated="[ISO 8601 datetime]">
       <message role="user|assistant" index="1">[Résumé concis du message - max 200 chars]</message>
       <message role="user|assistant" index="2">[Résumé concis du message - max 200 chars]</message>
       <message role="user|assistant" index="3">[Résumé concis du message - max 200 chars]</message>
     </last-conversation>
     ```
   - Les messages sont ordonnés chronologiquement (1 = le plus ancien des 3, 3 = le plus récent)
   - Résumer chaque message de façon concise mais fidèle (max 200 caractères)
   - Si un message contient du code ou des résultats d'outils, résumer l'action et le résultat

7. **Confirmer** les mises à jour effectuées à l'utilisateur

## Structure project-state.xml (si création nécessaire)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project-state>
  <metadata>
    <project-name>NOM DU PROJET</project-name>
    <project-id>ARCHON PROJECT ID</project-id>
    <created>DATE ISO 8601</created>
    <last-updated>DATE ISO 8601</last-updated>
    <session-id>session-001</session-id>
  </metadata>

  <current-objective>
    <name>Objectif actuel</name>
    <status>in-progress</status>
    <description>Description de l'objectif</description>
  </current-objective>

  <tasks>
    <!-- Tâches locales de la session -->
  </tasks>

  <history>
    <!-- Événements chronologiques -->
  </history>

  <completed-milestones>
    <!-- Jalons atteints -->
  </completed-milestones>

  <last-conversation updated="">
    <!-- Les 3 derniers messages échangés avant le dernier /update -->
  </last-conversation>

  <notes>
    <!-- Notes importantes -->
  </notes>
</project-state>
```

## Format de sortie

```
## Mise à jour effectuée

### Projet détecté
- Nom: ...
- Archon ID: ...

### Archon MCP
- [x] Tâche XXX marquée comme terminée
- [x] Nouvelle tâche YYY créée

### project-state.xml
- [x] Objectif actuel: ...
- [x] Événements ajoutés: ...
- [x] Statuts mis à jour: ...
- [x] Dernière conversation capturée (3 messages)

### project-status.json
- [x] Snapshot mis a jour (session: {session}, phase: {phase})
OU si non installe :
- [-] Non installe (disponible via /orni-init-pss)

### Prochaines étapes
- ...
```

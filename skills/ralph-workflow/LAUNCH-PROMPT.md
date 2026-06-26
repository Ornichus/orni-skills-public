# Prompt de Lancement: Ralph Workflow

**Usage:** Copier ce prompt et le donner à Claude Code dans un nouveau projet pour initialiser le workflow Ralph.

---

## PROMPT À COPIER

```
# Mission: Initialiser Ralph Workflow

Tu vas mettre en place le workflow Ralph pour ce projet. Ce workflow permet de valider un PRD existant via des tests, puis de lancer une boucle autonome pour implémenter les features.

## Contexte

Le workflow Ralph suit ces phases:
1. Setup - Vérifier PRD + configurer agent-browser
2. Test Manuel - Tester chaque Epic avec l'utilisateur
3. Analyse Écarts - Comparer PRD vs réalité
4. Révision PRD - Corriger et mettre à jour
5. Ralph Loop - Exécution autonome

## Actions à Effectuer

### Phase 0: Setup

1. **Localiser le PRD existant**
   - Chercher `docs/PRD.md`, `PRD.md`, ou fichier similaire
   - Si absent, demander à l'utilisateur

2. **Créer la structure Ralph**
   ```
   mkdir -p .ralph
   mkdir -p test/agent-browser
   ```

3. **Créer les fichiers Ralph** (adapter au projet):
   - `.ralph/PRD-ralph.md` - Convertir PRD en format Ralph
   - `.ralph/prompt.md` - Contexte pour chaque loop
   - `.ralph/activity.md` - Log des activités
   - `.ralph/settings.json` - Permissions sécurité
   - `.ralph/ralph.sh` - Script de boucle

4. **Créer la checklist de validation**
   - `test/prd-validation-checklist.md`
   - Lister tous les Epics/User Stories du PRD
   - Format: ID | Description | Priorité | Statut | Commentaire

### Agent-Browser Commands (Windows + WSL)

```bash
# TOUJOURS utiliser bash -c
wsl -d Ubuntu -- bash -c "npx agent-browser open 'http://IP:PORT'"
wsl -d Ubuntu -- bash -c "npx agent-browser snapshot -i"
wsl -d Ubuntu -- bash -c "npx agent-browser click e1"
wsl -d Ubuntu -- bash -c "npx agent-browser close"
```

## Livrables Attendus

1. [ ] Structure `.ralph/` créée
2. [ ] PRD converti en format Ralph
3. [ ] Checklist de validation créée
4. [ ] Agent-browser configuré (si applicable)
5. [ ] Prêt pour Phase 1 (Test Manuel)

## Ressources

- Skill complet: skills/ralph-workflow
- Agent-browser: skills/agent-browser

---

Commence par localiser le PRD existant et me montrer sa structure (Epics, User Stories). Ensuite, propose la conversion en format Ralph.
```

---

## Instructions d'Utilisation

1. **Ouvrir Claude Code** dans le nouveau projet
2. **Copier le prompt** ci-dessus
3. **Coller** et envoyer à Claude
4. **Suivre** les étapes proposées par l'agent
5. **Tester** avec l'utilisateur en Phase 1

## Adaptation par Projet

L'agent adaptera automatiquement:
- Le format du PRD selon ce qui existe
- Les commandes selon le stack technique
- Les ports selon la configuration
- Les Epics/User Stories selon le contenu

---

*Prompt créé le 2026-01-24*

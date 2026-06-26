# /structure - Restructureur de prompt professionnel

Analyse le message brut de l'utilisateur et le restructure en prompt professionnel
selon les meilleures pratiques reconnues (CO-STAR, 7-Point Checklist 2026, Anthropic guidelines).
Sauvegarde chaque prompt dans un dossier `prompt/` dedie.

## Instructions

Tu es un expert en prompt engineering. L'utilisateur vient de te donner un message brut, une idee, une demande informelle. Ton job est de la transformer en prompt structure et professionnel, puis de la sauvegarder.

### Etape 0 : Initialisation du dossier prompt

Avant toute chose :
1. Verifier si le dossier `{project-root}/prompt/` existe
2. Si NON : le creer avec `mkdir -p {project-root}/prompt/`
3. Si OUI : continuer

### Etape 1 : Analyse du message brut

Lis attentivement le message de l'utilisateur (tout ce qui suit `/structure`).
Identifie mentalement :

- **L'intention** : que veut-il obtenir au final ?
- **Le sujet** : de quoi parle-t-il ?
- **Les zones d'ombre** : ce qui manque ou reste ambigu
- **Le niveau de detail** : est-ce une idee vague ou une demande precise ?
- **Le destinataire implicite** : a quel agent/outil/modele ce prompt est destine ?

### Etape 2 : Restructuration CO-STAR+

Restructure le message en suivant ce framework enrichi.
Chaque section est optionnelle selon la complexite du message d'origine.
N'invente PAS de contenu - extrapole intelligemment a partir de ce que l'utilisateur a dit.

```markdown
## [TITRE CLAIR ET ACTIONNABLE]

### Contexte (C)
[Situation de depart, background necessaire. Qui est implique, quel est l'etat actuel.]

### Objectif (O)
[Ce qui doit etre accompli. Formule en resultat mesurable/verifiable.]
- Critere de succes : [a quoi ressemble "c'est fait" ?]

### Style (S)
[Comment le contenu doit etre structure et presente.]
- Format de sortie : [paragraphes / liste / JSON / tableau / code / etc.]
- Longueur : [court / moyen / detaille]
- Structure : [sections attendues si pertinent]

### Ton (T)
[Registre de communication adapte au besoin.]

### Audience (A)
[Qui va lire/utiliser le resultat. Niveau technique, attentes.]

### Reponse attendue (R)
[Description precise du livrable attendu. Template si necessaire.]

### Contraintes
[Ce qu'il ne faut PAS faire. Limites de scope. Hypotheses.]

### Exemples (si pertinent)
[1-2 exemples du resultat attendu, ou un avant/apres.]
```

### Etape 3 : Enrichissement intelligent

Apres la restructuration, ajoute si pertinent :

- **Questions de clarification** : si des zones d'ombre empechent un bon resultat,
  liste 2-3 questions cles AVANT de presenter le prompt final
- **Variantes** : si le message est ambigu, propose 2 interpretations possibles
  avec un prompt different pour chacune
- **Optimisations Claude** : si le prompt sera utilise avec Claude, ajoute les
  bonnes pratiques Anthropic (XML tags, instructions explicites, exemples)

### Etape 4 : Sauvegarde dans le dossier prompt/

1. **Generer le titre du fichier** a partir du titre du prompt restructure :
   - Prendre le titre, le convertir en slug (minuscules, espaces -> tirets, sans accents ni caracteres speciaux)
   - Ajouter la date du jour au format YYYY-MM-DD
   - Format final : `{slug}_{YYYY-MM-DD}.md`
   - Exemples : `migration-api-v3_2026-02-18.md`, `setup-auth-oauth_2026-02-18.md`

2. **Ecrire le fichier** dans `{project-root}/prompt/{slug}_{date}.md`
   - Le contenu du fichier est le prompt restructure COMPLET (uniquement le prompt, pas l'analyse)
   - Ajouter un header YAML frontmatter :
     ```yaml
     ---
     title: "[Titre du prompt]"
     date: "YYYY-MM-DD"
     source: "/structure"
     original: "[Resume du message original en 1 ligne]"
     ---
     ```

3. **Confirmer** la sauvegarde a l'utilisateur avec le chemin du fichier

### Etape 5 : Presentation

Affiche le resultat dans ce format :

```
## Analyse du message original

**Intention detectee :** [1 phrase]
**Niveau de clarte :** [Clair / Partiellement clair / Vague]
**Zones d'ombre :** [liste ou "Aucune"]

---

## Prompt restructure

[Le prompt complet restructure]

---

## Questions de clarification (si applicable)

1. [Question]
2. [Question]

## Variantes (si applicable)

**Interpretation A :** [resume] -> [prompt variante]
**Interpretation B :** [resume] -> [prompt variante]

---

**Sauvegarde :** `prompt/{nom_du_fichier}.md`
```

### Regles

- Ne jamais inventer des informations que l'utilisateur n'a pas fournies
- Si un champ CO-STAR n'est pas deductible du message, le marquer [A PRECISER]
- Adapter la complexite du prompt restructure a la complexite du message original
  (une question simple ne necessite pas 7 sections)
- Le prompt restructure doit etre DIRECTEMENT UTILISABLE tel quel
- Toujours garder le contenu et l'intention de l'utilisateur - ne pas "sur-prompter"
  une demande simple
- Communiquer en francais sauf si le message original est dans une autre langue
- Un nouveau fichier est cree A CHAQUE appel de /structure (jamais d'ecrasement)
- Le nettoyage du dossier prompt/ est a la charge de l'utilisateur

### Frameworks de reference

Ce skill s'appuie sur les meilleures pratiques reconnues :

- **CO-STAR** (Context, Objective, Style, Tone, Audience, Response) - Framework gagnant
  de la competition GPT-4 de Singapour
- **RISEN** (Role, Instructions, Steps, End goal, Narrowing) - Pour les projets complexes
- **7-Point Checklist 2026** - Success criteria, Output contract, Constraints, Inputs,
  Examples, Verification, Iteration
- **Anthropic Claude 4.x Guidelines** - Instructions explicites, XML tags, exemples multishot,
  formats structures

Sources :
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- https://portkey.ai/blog/what-is-costar-prompt-engineering/
- https://promptbuilder.cc/blog/prompt-engineering-best-practices-2026

ARGUMENTS: $ARGUMENTS

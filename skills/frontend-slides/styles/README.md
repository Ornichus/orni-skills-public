# Frontend Slides — Catalogue des styles

Styles maison pour les générations de présentations HTML one-shot. Chaque sous-dossier = un style complet (preset CSS + composants + références « golden »).

## Styles disponibles

| Style | Status | Vibe | Mode | Usage |
|-------|--------|------|------|-------|
| **nimbe** | **v2.0.0** | Verre dépoli + halos de lumière, premium corporate, composants à règle métier | Light défaut · dual dark/light | `/frontend-slides --style nimbe` |
| _autre_ | À venir | — | — | — |

> ### ★ Style maison — « Nimbe » (v2.0.0)
>
> **Nimbe** = des halos de lumière colorée (bleu / rouge / cyan) qui flottent derrière une surface en **verre dépoli** (`.lg`) qui les réfracte. Au-delà du look, c'est un **système** :
> - **Lisibilité bi-thème** : tokens texte `--c-*` (foncés en clair, clairs en sombre) — jamais de couleur d'accent brute en texte.
> - **Code couleur sémantique** : cyan `#16b6c9` **réservé aux éléments « Équipe »**.
> - **Composants à règle métier** : configurateur interactif qui passe en état « invalide » (cadre rouge + bandeau + correctif 1-clic) quand une invariante est violée.
>
> Socle : `golden/LIQUID-GLASS-STANDARD-v2.html` (standard du verre) + `preset.css` (couche injectable) + `components/SHOWCASE.html` (démo). Le `.lg` reste le nom technique de la surface ; **Nimbe** est le nom du style.

## Architecture commune

Chaque style suit la structure :

```
styles/{nom}/
├── preset.css            # CSS injectable
├── README.md             # Doc du style
├── golden/               # Références « standard » à imiter
└── components/           # Composants signature spécifiques
```

## Workflow d'utilisation

### Générer un deck

```
# Style maison
/frontend-slides --style nimbe "Sujet du deck"

# Style par défaut (presets natifs upstream)
/frontend-slides "Sujet du deck"
```

### Créer un nouveau style

1. **Définir l'identité** : nom, vibe, mode dark/light, audience
2. **Lire `nimbe/preset.css`** comme template de référence
3. **Créer `styles/{nom}/`** avec la structure standard
4. **Écrire `preset.css`** avec variables CSS et classes signature
5. **Ajouter une référence « golden »** (page HTML autoportante qui sert de standard du style)
6. **Tester sur un deck pilote** : avant/après comparatif vs preset générique
7. **Itérer visuellement** jusqu'à validation

## Méthode RoboNuggets (3 niveaux)

D'après la vidéo YouTube tutoriel :

1. **Niveau 1** — Installer le skill frontend-slides (fait via `/orni-init-fs`)
2. **Niveau 2** — Créer/utiliser un style via `styles/{nom}/`
3. **Niveau 3** — Bibliothèque de composants spécifiques au style dans `styles/{nom}/components/`

## Quand créer un nouveau style ?

- **Nouvelle identité visuelle** distincte
- **Cas d'usage différent** d'un style existant (ex: pitch investor vs internal training)
- **Audience différente** (corporate B2B vs créatif startup)

## Quand garder un style existant ?

- Variation de tonalité légère → utiliser des overrides CSS dans le deck individuel
- Changement de couleurs ponctuel → CSS variables dans le frontmatter du deck
- Ajustement temporaire → ne pas créer de style permanent

---

**Référence visuelle** : ouvrir `nimbe/components/SHOWCASE.html` pour voir la bibliothèque complète du style.

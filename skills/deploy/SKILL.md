# Deploy & Publish Skill

> **Version**: 1.0.0 | **Dernière mise à jour**: 14 mars 2026

Skill pour déployer une application sur le VPS avec HTTPS via Cloudflare DNS.
Orchestre le **VPS Skill** (SSH) et le **Cloudflare Skill** (DNS API) pour offrir un workflow complet : transfert, lancement, DNS, Nginx, certificat SSL.

---

## Prérequis

### Skills requis

| Skill | Fichier | Rôle dans ce workflow |
|-------|---------|----------------------|
| VPS Management | `~/.claude/skills/vps/SKILL.md` | Connexion SSH, exécution de commandes sur le VPS |
| Cloudflare Management | `~/.claude/skills/cloudflare/SKILL.md` | Gestion DNS via API v4 |

### Fichiers de configuration

| Fichier | Contenu attendu |
|---------|----------------|
| `~/.claude/vps-config.json` | `vps.ip`, `vps.ssh.user`, `vps.ssh.key_path` |
| `~/.claude/cloudflare.json` | `api_token`, `account_id`, `default_zone` |

### Sur le VPS

- Docker + Docker Compose installés
- Nginx installé et actif
- Certbot installé (avec plugin nginx)
- Répertoire `/opt/claude-deploy/` existant (créé au premier déploiement si absent)

---

## Workflow overview

| Étape | Action | Checkpoint utilisateur |
|-------|--------|----------------------|
| 1 | Résoudre le contexte (slug, type, source, domaine) | Non |
| 2 | Transférer les fichiers sur le VPS | Non |
| 3 | Lancer le service (Docker ou rien pour static) | Non |
| 4 | Créer le record DNS | **Oui — confirmation requise** |
| 5 | Configurer Nginx + HTTPS + activer le proxy Cloudflare | Non |

---

## Étape 1 — Résoudre le contexte

Avant toute action, déterminer les 4 paramètres du déploiement.

### 1.1 Slug

Nom sanitisé du projet. Règles :
- Prendre le nom du dossier du projet
- Convertir en minuscules
- Remplacer espaces et underscores par des tirets
- Retirer les caractères spéciaux (garder uniquement `[a-z0-9-]`)
- Tronquer à 50 caractères maximum
- Exemple : `My_Cool App!` → `my-cool-app`

### 1.2 Type de déploiement

| Condition | Type |
|-----------|------|
| `docker-compose.yml` ou `Dockerfile` présent à la racine | `docker` |
| Sinon | `static` |

### 1.3 Source de transfert

| Condition | Mode |
|-----------|------|
| Le projet a un remote GitHub (`git remote -v` retourne une URL github.com) | `git` |
| Sinon | `scp` |

> **Note v1 :** Le mode `git` ne supporte que les repos publics. Pour les repos privés, utiliser `scp`.

### 1.4 Domaine

- Domaine par défaut : `{slug}.{default_zone}` (où `default_zone` vient de `~/.claude/cloudflare.json`)
- Exemple : `my-cool-app.votre-domaine.com`

**Validation :** Vérifier que le domaine de base est géré dans Cloudflare en listant les zones :

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')

curl -s "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[].name'
```

Si le domaine de base n'apparaît pas dans la liste → **erreur**, afficher les zones disponibles et demander à l'utilisateur de choisir.

### 1.5 Résumé

Afficher un résumé avant de continuer :

```
Déploiement prévu :
  Slug     : my-cool-app
  Type     : docker
  Source   : scp
  Domaine  : my-cool-app.votre-domaine.com
  Port     : 3017 (attribué automatiquement)
```

Puis continuer sans attendre de confirmation (sauf si l'utilisateur a demandé un mode interactif).

---

## Étape 2 — Transférer sur le VPS

Lire la configuration VPS en suivant le workflow du **VPS Skill** :
- Lire `~/.claude/vps-config.json` avec l'outil Read
- Extraire `ip`, `ssh.user`, `ssh.key_path`
- Construire les commandes SSH avec : `ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip}`

### Mode Git (repos publics uniquement en v1)

```bash
# Récupérer l'URL du remote
REPO_URL=$(git remote get-url origin)

# Sur le VPS : clone ou pull
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  mkdir -p /opt/claude-deploy/apps/{slug}
  if [ -d /opt/claude-deploy/apps/{slug}/.git ]; then
    cd /opt/claude-deploy/apps/{slug} && git pull
  else
    git clone $REPO_URL /opt/claude-deploy/apps/{slug}
  fi
"
```

### Mode SCP

Transférer via rsync (ou tar+scp en fallback). Exclure les répertoires non nécessaires :

```bash
rsync -avz --delete \
  --exclude '.git/' \
  --exclude 'node_modules/' \
  --exclude '__pycache__/' \
  --exclude '.venv/' \
  --exclude '.env' \
  -e "ssh -i {key_path} -o ConnectTimeout=10" \
  ./ {user}@{ip}:{destination}/
```

**Destination selon le type :**

| Type | Destination |
|------|-------------|
| `docker` | `/opt/claude-deploy/apps/{slug}/` |
| `static` | Détecter `dist/` ou `build/` dans le projet. Si présent, transférer ce sous-dossier vers `/var/www/{slug}/`. Sinon, transférer la racine vers `/var/www/{slug}/`. |

---

## Étape 3 — Lancer le service

### Type Docker

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  cd /opt/claude-deploy/apps/{slug} && \
  docker compose down && \
  docker compose up -d --build
"
```

Vérifier que les containers sont up :

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "docker ps --filter name={slug} --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
```

### Type Static

Rien à faire — les fichiers sont déjà en place dans `/var/www/{slug}/`.

---

## Étape 4 — DNS (checkpoint utilisateur)

**Cette étape requiert une confirmation explicite de l'utilisateur.**

### 4.1 Afficher l'action prévue

```
DNS à créer :
  Type    : A
  Nom     : {slug}.{domain}
  Contenu : {vps_ip}
  Proxy   : DNS only (sera activé après HTTPS)

Confirmer ? (oui/non)
```

**Attendre la réponse de l'utilisateur.** Ne pas continuer sans confirmation.

### 4.2 Résoudre le zone_id

Suivre le workflow du **Cloudflare Skill** :

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_NAME="votre-domaine.com"

ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=$ZONE_NAME" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')
```

### 4.3 Créer le record A

```bash
RECORD=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "{slug}",
    "content": "{vps_ip}",
    "proxied": false,
    "ttl": 1
  }')

echo $RECORD | jq '{success, id: .result.id, name: .result.name}'
```

> **Important :** `proxied: false` ici. Le proxy sera activé à l'étape 5d après la mise en place du certificat SSL.

Stocker le `record_id` retourné — il sera nécessaire à l'étape 5d.

### 4.4 Vérifier la propagation DNS

Retry 3 fois avec 10 secondes d'intervalle :

```bash
for i in 1 2 3; do
  echo "Tentative $i/3..."
  nslookup {slug}.{domain} 1.1.1.1
  if [ $? -eq 0 ]; then
    echo "DNS propagé."
    break
  fi
  sleep 10
done
```

---

## Étape 5 — Nginx + HTTPS + Cloudflare proxy

### 5a — Générer la configuration Nginx

Créer le fichier sur le VPS : `/etc/nginx/sites-available/{slug}`

**Template Docker :**

```nginx
server {
    server_name {slug}.{domain};

    location / {
        proxy_pass http://127.0.0.1:{port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    listen 80;
}
```

**Template Static :**

```nginx
server {
    server_name {slug}.{domain};

    root /var/www/{slug};
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    listen 80;
}
```

**Écriture sur le VPS :**

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  # Backup si le fichier existe déjà
  [ -f /etc/nginx/sites-available/{slug} ] && \
    cp /etc/nginx/sites-available/{slug} /etc/nginx/sites-available/{slug}.bak.\$(date +%Y%m%d%H%M%S)

  cat > /etc/nginx/sites-available/{slug} << 'NGINX_CONF'
{contenu du template ci-dessus avec les valeurs remplacées}
NGINX_CONF
"
```

### 5b — Activer le site et recharger Nginx

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  ln -sf /etc/nginx/sites-available/{slug} /etc/nginx/sites-enabled/{slug} && \
  nginx -t && \
  systemctl reload nginx
"
```

Si `nginx -t` échoue → **rollback** : restaurer le backup et ne pas recharger.

### 5c — Obtenir le certificat SSL

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  certbot --nginx -d {slug}.{domain} --non-interactive --agree-tos -m admin@{domain}
"
```

Si certbot échoue → **laisser le site en HTTP**, avertir l'utilisateur, ne pas activer le proxy Cloudflare.

### 5d — Activer le proxy Cloudflare

Une fois le certificat SSL en place, activer le proxy pour bénéficier de la protection DDoS et du cache :

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="{zone_id}"        # Résolu à l'étape 4.2
RECORD_ID="{record_id}"    # Obtenu à l'étape 4.3

curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"proxied": true}' | jq '{success, proxied: .result.proxied}'
```

---

## Redéploiement

Quand une application existe déjà dans le registre (`/opt/claude-deploy/registry.json`), le workflow est simplifié.

**Ce qui est réutilisé :** port, domaine, configuration Nginx, certificat SSL, record DNS.

**Ce qui est exécuté :**

1. Transférer les fichiers (étape 2 — identique)
2. Pour Docker : `docker compose down && docker compose up -d --build`
3. Vérifier que le service répond

**Ce qui est ignoré :** Nginx, certbot, DNS — tout est déjà en place.

---

## Registre

### Fichier

`/opt/claude-deploy/registry.json` sur le VPS.

### Format

```json
{
  "port_range": [3000, 4000],
  "default_domain": "votre-domaine.com",
  "apps": {
    "my-cool-app": {
      "slug": "my-cool-app",
      "type": "docker",
      "source": "git",
      "domain": "my-cool-app.votre-domaine.com",
      "port": 3017,
      "path": "/opt/claude-deploy/apps/my-cool-app",
      "dns_record_id": "abc123...",
      "deployed_at": "2026-03-14T10:30:00Z"
    },
    "portfolio": {
      "slug": "portfolio",
      "type": "static",
      "source": "scp",
      "domain": "portfolio.votre-domaine.com",
      "port": null,
      "path": "/var/www/portfolio",
      "dns_record_id": "def456...",
      "deployed_at": "2026-03-14T11:00:00Z"
    }
  }
}
```

### Attribution de port

Si l'app existe déjà dans le registre → réutiliser son port existant (redéploiement). Sinon → chercher le plus petit port libre dans la plage configurée :

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  cat /opt/claude-deploy/registry.json | \
  jq '[range(.port_range[0]; .port_range[1]+1)] - [.apps[].port] | sort | first'
"
```

### Mise à jour du registre

Après un déploiement réussi, mettre à jour le registre via jq :

```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "
  cat /opt/claude-deploy/registry.json | jq '.apps.\"{slug}\" = {
    \"slug\": \"{slug}\",
    \"type\": \"{type}\",
    \"source\": \"{source}\",
    \"domain\": \"{slug}.{domain}\",
    \"port\": {port},
    \"path\": \"{path}\",
    \"dns_record_id\": \"{record_id}\",
    \"deployed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }' > /tmp/registry-updated.json && \
  mv /tmp/registry-updated.json /opt/claude-deploy/registry.json
"
```

### Initialisation

Si le fichier n'existe pas, le créer :

```json
{
  "port_range": [3000, 4000],
  "default_domain": "votre-domaine.com",
  "apps": {}
}
```

**Enregistrement rétroactif :** Au premier deploy, si des apps sont déjà présentes sur le VPS (containers Docker actifs, sites Nginx configurés), les enregistrer rétroactivement dans le registre.

### Chemins par type

| Type | Chemin sur le VPS |
|------|-------------------|
| `docker` | `/opt/claude-deploy/apps/{slug}/` |
| `static` | `/var/www/{slug}/` |

---

## Gestion des erreurs

| Étape | Erreur | Action |
|-------|--------|--------|
| Transfert | SSH échoue (timeout, auth) | **Stop.** Afficher l'erreur, ne rien modifier |
| Docker build | Build ou up échoue | Afficher les logs (`docker compose logs`). **Ne pas toucher** à Nginx/DNS |
| Nginx | `nginx -t` échoue | **Rollback** : restaurer le fichier `.bak`, recharger Nginx |
| Certbot | Échec de certification | Laisser le site en **HTTP uniquement**, avertir l'utilisateur. Ne pas activer `proxied: true` |
| DNS | Création du record échoue | Afficher l'erreur API Cloudflare, ne pas continuer vers Nginx |
| Domaine invalide | Zone non trouvée dans Cloudflare | Afficher une erreur et lister les zones disponibles |

**Principe fondamental : ne jamais casser ce qui fonctionnait.**

Si une étape échoue, les étapes précédentes déjà réussies restent en place (sauf Nginx qui est rollback automatiquement).

---

## Règles de sécurité

1. **Ne JAMAIS** hardcoder l'IP du VPS, les tokens ou les clés SSH — toujours lire depuis les fichiers de config
2. **TOUJOURS** sauvegarder la configuration Nginx existante avant de la modifier (`*.bak.{timestamp}`)
3. **TOUJOURS** demander confirmation à l'utilisateur avant de créer/modifier un record DNS (étape 4)
4. **Ne JAMAIS** transférer de fichiers `.env` vers le VPS via SCP — les secrets doivent être gérés séparément
5. **TOUJOURS** vérifier `nginx -t` avant de recharger — ne jamais faire `systemctl reload nginx` à l'aveugle

---

## Fichiers de configuration (référence)

| Fichier | Rôle | Versionné ? |
|---------|------|-------------|
| `~/.claude/vps-config.json` | IP, hostname, clé SSH du VPS | **NON** |
| `~/.claude/cloudflare.json` | Token API Cloudflare, account_id, zone par défaut | **NON** |
| `/opt/claude-deploy/registry.json` | Registre des apps déployées (sur le VPS) | **NON** |

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-03-14 | 1.0.0 | Version initiale — déploiement Docker/Static, DNS Cloudflare, Nginx + HTTPS |

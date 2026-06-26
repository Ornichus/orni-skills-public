# Cloudflare Management - Skill partagé

> **Version**: 1.0.0 | Gestion Cloudflare via API v4 (DNS, Zones, et plus)

Skill pour interagir avec l'API Cloudflare depuis Claude Code.
Les agents lisent ce skill et exécutent les appels curl documentés ci-dessous.

---

## 1. Configuration

### Prérequis

Fichier : `~/.claude/cloudflare.json`

```json
{
  "api_token": "<cloudflare-api-token>",
  "account_id": "<cloudflare-account-id>",
  "default_zone": "votre-domaine.com"
}
```

| Champ | Description | Comment l'obtenir |
|-------|-------------|-------------------|
| `api_token` | Token API scoped | Cloudflare Dashboard → My Profile → API Tokens → Create Token |
| `account_id` | ID du compte | Cloudflare Dashboard → vue d'ensemble d'un domaine → colonne droite |
| `default_zone` | Domaine par défaut | Nom du domaine principal (ex: votre-domaine.com) |

**Permissions du token :** Au minimum "Zone:DNS:Edit" + "Zone:Zone:Read". Ajouter d'autres permissions selon les sections utilisées (Workers, SSL...).

### Lecture de la configuration

**TOUJOURS suivre ces étapes dans cet ordre :**

#### Étape 1 — Lire la configuration

```bash
# Lire le fichier de config avec l'outil Read
# Extraire les valeurs avec jq :
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
CF_ACCOUNT=$(cat ~/.claude/cloudflare.json | jq -r '.account_id')
CF_DEFAULT_ZONE=$(cat ~/.claude/cloudflare.json | jq -r '.default_zone')
```

Ne JAMAIS hardcoder le token ou l'account_id. Toujours lire depuis le fichier de config.

#### Étape 2 — Headers standard

Tous les appels API utilisent ces headers :

```bash
-H "Authorization: Bearer $CF_TOKEN" \
-H "Content-Type: application/json"
```

#### Étape 3 — Vérifier le résultat

Toujours vérifier `.success` dans la réponse :

```bash
# La réponse contient toujours :
# { "success": true|false, "errors": [...], "messages": [...], "result": ... }
# Vérifier : | jq '.success'
```

---

## 2. Helpers communs

### Résoudre un zone_id à partir du nom de domaine

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')

ZONE_NAME="votre-domaine.com"  # ou $CF_DEFAULT_ZONE
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=$ZONE_NAME" \
  -H "Authorization: Bearer $CF_TOKEN" | jq -r '.result[0].id')

echo "Zone ID: $ZONE_ID"
```

### Gestion des erreurs API

| Code erreur | Signification | Action |
|-------------|--------------|--------|
| `6003` | Token invalide ou expiré | Vérifier/renouveler le token dans cloudflare.json |
| `9106` | Zone non trouvée | Vérifier le nom de domaine |
| `81057` | Record DNS déjà existant | Utiliser PATCH au lieu de POST pour modifier |
| `10000` | Authentication error | Vérifier api_token et ses permissions |
| `7003` | Pas de permission | Le token n'a pas les droits nécessaires |

### Pagination

Les réponses avec plus de 20 résultats sont paginées :

```bash
# Page 1 (défaut)
curl -s "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?page=1&per_page=100" \
  -H "Authorization: Bearer $CF_TOKEN"

# Vérifier result_info pour savoir s'il y a d'autres pages :
# "result_info": { "page": 1, "per_page": 100, "total_pages": 3, "count": 100, "total_count": 250 }
```

---

## 3. DNS Management

### 3.1 Lister tous les records DNS

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"  # Résolu via section 2

curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?per_page=100" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {id, type, name, content, proxied, ttl}'
```

**Filtrer par type :**
```bash
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=A&per_page=100" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {id, name, content, proxied}'
```

**Filtrer par nom :**
```bash
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=app.votre-domaine.com" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result'
```

### 3.2 Créer un record DNS

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"

curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "mwc",
    "content": "203.0.113.10",
    "proxied": true,
    "ttl": 1
  }' | jq '{success, id: .result.id, name: .result.name}'
```

**Types de records courants :**

| Type | name | content | Cas d'usage |
|------|------|---------|-------------|
| `A` | sous-domaine | IP v4 | Pointer vers un serveur |
| `AAAA` | sous-domaine | IP v6 | Pointer vers un serveur (IPv6) |
| `CNAME` | alias | domaine cible | Alias vers un autre domaine |
| `TXT` | @ ou sous-domaine | texte libre | Vérification, SPF, DKIM |
| `MX` | @ | serveur mail | Configuration email |
| `NS` | @ ou sous-domaine | nameserver | Délégation DNS |
| `SRV` | _service._proto | target | Services spécifiques |

**Notes :**
- `ttl: 1` = auto (géré par Cloudflare quand `proxied: true`)
- `proxied: true` = trafic passe par Cloudflare (protection DDoS, cache)
- `proxied: false` = DNS only (pas de proxy Cloudflare)
- Pour `CNAME`, `content` est un nom de domaine (pas une IP)

### 3.3 Modifier un record DNS

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"
RECORD_ID="<record_id>"  # Obtenu via 3.1

curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "nouvelle-ip-ou-valeur",
    "proxied": true
  }' | jq '{success, name: .result.name, content: .result.content}'
```

On peut modifier un ou plusieurs champs : `content`, `name`, `proxied`, `ttl`, `type`.

### 3.4 Supprimer un record DNS

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"
RECORD_ID="<record_id>"

curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '{success, id: .result.id}'
```

**ATTENTION :** Cette opération est irréversible. Toujours confirmer avec l'utilisateur avant de supprimer.

### 3.5 Vérifier la propagation DNS

```bash
# Via DNS direct Cloudflare (1.1.1.1)
nslookup app.votre-domaine.com 1.1.1.1

# Via dig (plus détaillé, si disponible)
dig app.votre-domaine.com @1.1.1.1

# Via Google DNS (propagation externe)
nslookup app.votre-domaine.com 8.8.8.8
```

---

## 4. Zone Management

### 4.1 Lister toutes les zones du compte

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')

curl -s "https://api.cloudflare.com/client/v4/zones?per_page=50" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '.result[] | {id, name, status, plan: .plan.name}'
```

### 4.2 Détail d'une zone

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"

curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
  -H "Authorization: Bearer $CF_TOKEN" | jq '{name: .result.name, status: .result.status, nameservers: .result.name_servers, plan: .result.plan.name}'
```

### 4.3 Purger le cache d'une zone

```bash
CF_TOKEN=$(cat ~/.claude/cloudflare.json | jq -r '.api_token')
ZONE_ID="<zone_id>"

# Purger tout le cache
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything": true}' | jq '.success'

# Purger des URLs spécifiques
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"files": ["https://app.votre-domaine.com/style.css"]}' | jq '.success'
```

---

## 5. (Futur) Workers & Pages

_Section réservée. À documenter quand le besoin se présente._

## 6. (Futur) SSL/TLS

_Section réservée. À documenter quand le besoin se présente._

## 7. (Futur) Page Rules & Redirects

_Section réservée. À documenter quand le besoin se présente._

---

## Fichiers de configuration (référence)

| Fichier | Rôle | Versionné ? |
|---------|------|-------------|
| `~/.claude/cloudflare.json` | Token API, account_id, zone par défaut | **NON** (local uniquement) |

---

## Règles de sécurité

1. **Ne JAMAIS** stocker le token API dans un fichier versionné (git)
2. **TOUJOURS** lire `~/.claude/cloudflare.json` pour les credentials — ne jamais hardcoder
3. **TOUJOURS** vérifier `.success == true` dans chaque réponse API avant de considérer l'opération réussie
4. **TOUJOURS** confirmer avec l'utilisateur avant de supprimer un record DNS
5. **Préférer** `proxied: true` sauf besoin spécifique (protection DDoS, cache)
6. **Logger** les actions DNS importantes dans le project-state.xml via `/update`

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-03-02 | 1.0.0 | Version initiale — DNS Management + Zone Management |

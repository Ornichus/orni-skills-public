# VPS Management Skill

> **Version**: 1.1.0 | **Dernière mise à jour**: 21 février 2026

Skill pour interagir avec le VPS Hostinger depuis Claude Code.
Deux canaux d'accès : **SSH direct** (tout) et **MCP Hostinger** (deploy, DNS, billing).

---

## Workflow de connexion SSH

**TOUJOURS suivre ces étapes dans cet ordre :**

### Étape 1 — Lire la configuration

```
Lire le fichier ~/.claude/vps-config.json avec l'outil Read
```

Ce fichier contient :
```json
{
  "vps": {
    "ip": "<IP du VPS>",
    "hostname": "<hostname>",
    "os": "<OS>",
    "ssh": {
      "user": "<utilisateur SSH>",
      "port": 22,
      "key_path": "<chemin absolu vers la clé privée>"
    }
  }
}
```

Extraire : `ip`, `ssh.user`, `ssh.key_path`.

### Étape 2 — Construire la commande SSH

Template (ne JAMAIS hardcoder les valeurs) :

```bash
ssh -i {key_path} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 {user}@{ip} "{commande}"
```

Remplacer `{key_path}`, `{user}`, `{ip}` par les valeurs lues à l'étape 1.

### Étape 3 — Exécuter via l'outil Bash

Utiliser l'outil **Bash** de Claude Code pour exécuter la commande SSH construite à l'étape 2.

**Exemple complet :**
```bash
ssh -i /chemin/vers/claude-vps -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 root@X.X.X.X "hostname && uptime"
```

### Gestion des erreurs

| Erreur | Cause probable | Action |
|--------|---------------|--------|
| `Connection timed out` | VPS éteint ou IP incorrecte | Vérifier l'IP dans vps-config.json, vérifier via MCP Hostinger |
| `Permission denied` | Clé SSH non déployée ou invalide | Vérifier que la clé publique est dans `~/.ssh/authorized_keys` sur le VPS |
| `Host key verification failed` | Première connexion ou clé changée | Ajouter `-o StrictHostKeyChecking=accept-new` |
| `Command not found` (côté VPS) | Package non installé | `apt install <package>` |

---

## Opérations courantes via SSH

**IMPORTANT** : Toutes les commandes ci-dessous doivent être exécutées **via SSH** en suivant le workflow ci-dessus. Ne PAS les exécuter localement.

Pour chaque commande, construire :
```bash
ssh -i {key_path} -o ConnectTimeout=10 {user}@{ip} "<commande ci-dessous>"
```

### Diagnostic rapide

```bash
# Vue d'ensemble en une commande
echo '=== HOSTNAME ===' && hostname && echo '=== UPTIME ===' && uptime && echo '=== CPU ===' && top -bn1 | head -5 && echo '=== RAM ===' && free -h && echo '=== DISK ===' && df -h / && echo '=== PORTS ===' && ss -tlnp
```

### Services

```bash
# Lister les services actifs
systemctl list-units --type=service --state=running

# Status d'un service
systemctl status <service>

# Restart / Reload (préférer reload quand possible)
systemctl reload <service>
systemctl restart <service>

# Logs récents d'un service
journalctl -u <service> --no-pager -n 50
```

### Nginx

```bash
# Tester la config avant reload
nginx -t && systemctl reload nginx

# Sites actifs
ls -la /etc/nginx/sites-enabled/

# Logs d'accès / erreur
tail -50 /var/log/nginx/access.log
tail -50 /var/log/nginx/error.log
```

### Docker (si installé)

```bash
# Containers actifs
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Tous les containers
docker ps -a

# Logs d'un container
docker logs --tail 50 <container>

# Redémarrer via compose
cd /chemin/projet && docker compose down && docker compose up -d
```

### Fichiers distants

```bash
# Lire un fichier
cat /chemin/fichier

# Sauvegarder PUIS modifier
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d) && cat > /etc/nginx/nginx.conf << 'HEREDOC'
<nouveau contenu>
HEREDOC

# Lister un répertoire
ls -la /chemin/
```

### Sécurité & Maintenance

```bash
# Firewall
ufw status verbose
ufw allow 80/tcp
ufw allow 443/tcp

# Mises à jour
apt update && apt list --upgradable

# Appliquer les mises à jour de sécurité uniquement
apt upgrade -y

# Vérifier les connexions SSH actives
who
last -10
```

---

## Utilisation du MCP Hostinger

Le MCP Hostinger gère : **déploiement d'apps**, **DNS**, **billing**.

### Étape 1 — Charger les outils

Les outils MCP Hostinger sont des **deferred tools**. Avant de les utiliser :

```
Utiliser ToolSearch avec query: "+hostinger" pour charger les outils disponibles
```

### Étape 2 — Appeler les outils

Une fois chargés, les outils sont disponibles directement.

### Outils disponibles

#### Deployment

| Outil MCP | Usage |
|-----------|-------|
| `hosting_deployStaticWebsite` | Déployer un site statique (HTML/CSS/JS) |
| `hosting_deployJsApplication` | Déployer une app Node.js (source uniquement, build côté serveur) |
| `hosting_deployWordpressPlugin` | Déployer un plugin WordPress |
| `hosting_deployWordpressTheme` | Déployer un thème WordPress |
| `hosting_importWordpressWebsite` | Importer un site WordPress complet (archive + dump DB) |
| `hosting_listJsDeployments` | Lister les déploiements et leur statut |
| `hosting_showJsDeploymentLogs` | Logs de build/déploiement pour debug |

#### DNS

| Outil MCP | Usage |
|-----------|-------|
| `DNS_getDNSRecordsV1` | Lire tous les records DNS d'un domaine |
| `DNS_updateDNSRecordsV1` | Modifier des records DNS |
| `DNS_deleteDNSRecordsV1` | Supprimer des records |
| `DNS_resetDNSRecordsV1` | Remettre les DNS par défaut |
| `DNS_validateDNSRecordsV1` | Vérifier la validité des records |
| `DNS_getDNSSnapshotListV1` | Lister les snapshots (points de restauration) |
| `DNS_restoreDNSSnapshotV1` | Restaurer un snapshot DNS |

#### Billing

| Outil MCP | Usage |
|-----------|-------|
| `billing_getCatalogItemListV1` | Catalogue des services et prix (en centimes) |
| `billing_getSubscriptionListV1` | Abonnements actifs |
| `billing_enableAutoRenewalV1` | Activer le renouvellement automatique |
| `billing_disableAutoRenewalV1` | Désactiver le renouvellement automatique |

---

## Fichiers de configuration (référence)

| Fichier | Rôle | Versionné ? |
|---------|------|-------------|
| `~/.claude/vps-config.json` | IP, hostname, clé SSH, specs VPS | **NON** (local uniquement) |
| `~/.claude/mcp.json` | Config MCP Hostinger (API token) | **NON** |
| `~/.claude/settings.json` | `sshConfigs` pour accès SSH intégré | **NON** |
| `~/.ssh/claude-vps` | Clé SSH privée dédiée | **NON** |
| `~/.ssh/claude-vps.pub` | Clé SSH publique (déployée sur le VPS) | **NON** |

---

## Règles de sécurité

1. **Ne JAMAIS** stocker l'IP, les clés SSH ou l'API token dans un fichier versionné (git)
2. **TOUJOURS** lire `~/.claude/vps-config.json` pour les infos de connexion — ne jamais hardcoder
3. **TOUJOURS** faire un backup avant de modifier un fichier de config critique sur le VPS
4. **Ne JAMAIS** exécuter de commandes destructives (`rm -rf`, `dd`, `mkfs`) sans confirmation explicite de l'utilisateur
5. **Préférer** `systemctl reload` à `systemctl restart` quand possible (évite le downtime)
6. **Logger** les actions importantes (install, config changes, deploys) dans le project-state.xml via `/update`
7. **Timeout** : toujours utiliser `-o ConnectTimeout=10` pour éviter les blocages

---

## Changelog

| Date | Version | Changements |
|------|---------|-------------|
| 2026-02-21 | 1.1.0 | Refonte : workflow step-by-step, commandes SSH-wrapped, ToolSearch MCP, gestion erreurs |
| 2026-02-21 | 1.0.0 | Version initiale |

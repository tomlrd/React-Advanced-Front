# React Advanced Front - Setup Script

Un script Python pour initialiser rapidement un projet Vite + React TypeScript avec toutes les dépendances nécessaires (Tailwind CSS, TanStack Query, Vitest, etc.).

## 📋 Prérequis

- **Node.js** v20+
- **Python** 3.8+
- Un gestionnaire de paquets: **npm**, **yarn**, **pnpm**, ou **bun**

## 🚀 Utilisation sur Cursor

### Méthode 1: Via la Palette de Commandes (recommandé)
1. Appuyez sur `Ctrl+Shift+P` (ou `Cmd+Shift+P` sur Mac)
2. Tapez `React_advanced_front`
3. Appuyez sur `Entrée`

### Méthode 2: Via le Terminal
```bash
python D:\.cursor\scripts\React_advanced_front.py
```

### Méthode 3: Créer une Task Globale (pour tous les projets)

Pour avoir accès au script depuis n'importe quel projet Cursor, créez une task globale:

1. **Ouvrez le fichier de configuration globale:**
   - Windows: `C:\Users\[VotreNom]\AppData\Roaming\Cursor\User\tasks.json`
   - Mac: `~/Library/Application Support/Cursor/User/tasks.json`
   - Linux: `~/.config/Cursor/User/tasks.json`

2. **Ajoutez cette configuration dans le tableau `tasks`:**

```json
{
    "label": "React Advanced Front",
    "type": "shell",
    "command": "python",
    "args": [
        "D:\\.cursor\\scripts\\React_advanced_front.py"
    ],
    "presentation": {
        "reveal": "always",
        "panel": "new",
        "focus": true
    },
    "windows": {
        "command": "python"
    },
    "linux": {
        "command": "python3"
    },
    "osx": {
        "command": "python3"
    }
}
```

3. **Sauvegardez le fichier**

4. **Relancez Cursor** ou rechargez les tâches avec `Ctrl+Shift+P` → `Tasks: Reload Tasks`

5. **Utilisez la task depuis n'importe quel projet:**
   - `Ctrl+Shift+P` → `Tasks: Run Task` → `React Advanced Front`

## 🎯 Utilisation sur VS Code

### Méthode 1: Via le Terminal Intégré (le plus simple)
1. Ouvrez le Terminal intégré (`Ctrl+`` `)
2. Naviguez vers le dossier où créer le projet
3. Exécutez:
```bash
python D:\.cursor\scripts\React_advanced_front.py
```

### Méthode 2: Via les Tasks
1. Créez un fichier `.vscode/tasks.json` à la racine du workspace
2. Collez le contenu suivant:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "React Advanced Front",
            "type": "shell",
            "command": "python",
            "args": [
                "D:\\.cursor\\scripts\\React_advanced_front.py"
            ],
            "presentation": {
                "reveal": "always",
                "panel": "new",
                "focus": true
            }
        }
    ]
}
```

3. Lancez avec `Ctrl+Shift+P` → `Tasks: Run Task` → `React Advanced Front`

## ⚙️ Configuration du Script

Le script vous posera les questions suivantes:

1. **Utiliser Corepack?** (y/n)
   - Permet de gérer les versions des gestionnaires de paquets

2. **Quel gestionnaire de paquets?** (1/2/3/4)
   - 1 = npm
   - 2 = yarn
   - 3 = pnpm
   - 4 = bun

3. **Nom du projet?**
   - Entrez un nom ou `.` pour le dossier courant

4. **⚠️ IMPORTANT - Deux questions de Vite vont apparaître:**
   - `Use rolldown-vite (Experimental)?` → **Répondez: n**
   - `Install with [package] and start now?` → **Répondez: n**
   - ⚠️ **SI VOUS REPONDEZ 'yes', LE SCRIPT VA PLANTER!**

5. **Installer Zustand + Immer?** (y/n)

## 📦 Qu'est-ce qui sera installé?

✅ **Vite** - Build tool ultra-rapide  
✅ **React 19** + TypeScript  
✅ **Tailwind CSS** - Framework CSS utilitaire  
✅ **TanStack Query** - Gestion d'état asynchrone  
✅ **Vitest** - Framework de test  
✅ **React Testing Library** - Tests de composants  
✅ **MSW** - Mock Service Worker  
✅ **ESLint** + **Prettier** (optionnel)  
✅ **Zustand + Immer** (optionnel)  

## 🎨 Fonctionnalités du Projet

- Configuration Tailwind CSS complète
- Setup Vitest avec jsdom et globals
- Fichier de setup pour les tests
- Structure de projet moderne et organisée
- Page d'accueil stylisée avec les versions des dépendances

## 📖 Commandes Utiles

Une fois le projet créé:

```bash
# Démarrer le serveur de développement
npm run dev        # ou yarn dev, pnpm dev, bun dev

# Lancer les tests
npm run test       # ou yarn test, pnpm test, bun test

# Tests avec interface UI
npm run test:ui    # ou yarn test:ui, pnpm test:ui, bun test:ui

# Build pour la production
npm run build      # ou yarn build, pnpm build, bun build
```

## ❓ FAQ

**Q: Pourquoi dois-je répondre 'n' aux questions de Vite?**  
R: Le script automatise la configuration complète du projet. Répondre 'yes' installerait les dépendances deux fois et démarrerait le serveur, ce qui casserait le flux du script.

**Q: Puis-je utiliser le script avec bun?**  
R: Oui! Bun est supporté et fonctionne sur tous les OS (Windows, Mac, Linux).

**Q: Le script utilise-t-il corepack?**  
R: Uniquement si vous répondez 'yes' à la première question. Corepack permet de gérer les versions exactes des gestionnaires.

## 👨‍💻 Auteur

Créé par [@tomlrd](https://github.com/tomlrd) pour [Le Reacteur](https://www.lereacteur.io/)

---

**v0.1** - React Advanced Front Setup Script

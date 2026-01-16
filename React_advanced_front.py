# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import json

def run_command(cmd, capture_output=False):
    """Exécute une commande shell"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")
        return None

def get_yes_no(prompt):
    """Demande une réponse oui/non"""
    while True:
        response = input(f"{prompt} (y/n): ").lower().strip()
        if response in ['y', 'n']:
            return response == 'y'
        print("Veuillez entrer 'y' ou 'n'")

def get_package_manager():
    """Demande quel gestionnaire de paquets utiliser"""
    print("\nQuel gestionnaire de paquets souhaitez-vous utiliser?")
    print("1. npm")
    print("2. yarn")
    print("3. pnpm")
    print("4. bun")
    
    while True:
        choice = input("Choisissez (1/2/3/4): ").strip()
        if choice in ['1', '2', '3', '4']:
            managers = {'1': 'npm', '2': 'yarn', '3': 'pnpm', '4': 'bun'}
            return managers[choice]
        print("Veuillez entrer 1, 2, 3 ou 4")

def main():
    print("========================================")
    print("  Configuration Vite + React TypeScript")
    print("========================================\n")
    
    # 1. Demander si l'utilisateur veut utiliser corepack
    use_corepack = get_yes_no("Souhaitez-vous utiliser corepack?")
    
    if use_corepack:
        print("Activation de corepack...")
        run_command("corepack enable")
    
    # 2. Demander le gestionnaire de paquets
    package_manager = get_package_manager()
    print(f"\nGestionnaire de paquets sélectionné: {package_manager}")
    
    # 3. Demander le nom du projet
    while True:
        project_name = input("\nNom du projet (ou '.' pour le dossier actuel): ").strip()
        if project_name:
            break
        print("Veuillez entrer un nom de projet")
    
    # 4. Créer le projet Vite
    print(f"\nCréation du projet Vite avec {package_manager}...")
    print("\n" + "="*80)
    print("\033[91m" + "⚠️  IMPORTANT - LISEZ ATTENTIVEMENT ⚠️".center(80) + "\033[0m")
    print("="*80)
    print("\033[91m\033[1m")
    print("VOUS DEVEZ REPONDRE 'NO' (n) AUX DEUX DERNIERES QUESTIONS DE VITE:".center(80))
    print("1. Use rolldown-vite (Experimental)? → REPONDEZ: n".center(80))
    print("2. Install with " + package_manager + " and start now? → REPONDEZ: n".center(80))
    print("\nSI VOUS REPONDEZ 'YES', LE SCRIPT VA PLANTER !".center(80))
    print("\033[0m" + "="*80 + "\n")
    
    # Préfixe corepack si activé
    corepack_prefix = "corepack " if use_corepack else ""
    
    if package_manager == 'npm':
        cmd = f"{corepack_prefix}npm create vite@latest {project_name} -- --template react-ts"
    elif package_manager == 'yarn':
        cmd = f"{corepack_prefix}yarn create vite {project_name} --template react-ts"
    elif package_manager == 'pnpm':
        cmd = f"{corepack_prefix}pnpm create vite {project_name} --template react-ts"
    elif package_manager == 'bun':
        cmd = f"{corepack_prefix}bun create vite {project_name} --template react-ts"
    
    # Exécuter la commande de façon interactive
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("\n❌ Erreur lors de la création du projet")
        return
    
    # Changer de répertoire si nécessaire
    if project_name != '.':
        os.chdir(project_name)
    
    # Vérifier que les fichiers essentiels existent
    if not os.path.exists('package.json'):
        print("\n❌ Le projet Vite n'a pas été créé correctement (package.json manquant).")
        return
    
    print("\n✅ Projet Vite créé avec succès!")
    
    # 5. Installer Tailwind CSS automatiquement
    print("\n📦 Installation de Tailwind CSS...")
    if package_manager == 'npm':
        install_cmd = f"{corepack_prefix}{package_manager} install tailwindcss @tailwindcss/vite"
    elif package_manager == 'yarn':
        install_cmd = f"{corepack_prefix}{package_manager} add tailwindcss @tailwindcss/vite"
    elif package_manager == 'pnpm':
        install_cmd = f"{corepack_prefix}{package_manager} add tailwindcss @tailwindcss/vite"
    elif package_manager == 'bun':
        install_cmd = f"{corepack_prefix}{package_manager} add tailwindcss @tailwindcss/vite"
    
    run_command(install_cmd)
    
    # Modifier vite.config.ts - Lire d'abord le fichier existant
    print("Configuration de vite.config.ts...")
    vite_config_content = """import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/__tests__/setup.ts',
  },
})
"""
    with open('vite.config.ts', 'w', encoding='utf-8') as f:
        f.write(vite_config_content)
    
    # Ajouter import Tailwind au CSS principal (src/index.css)
    print("Configuration du CSS...")
    css_path = os.path.join('src', 'index.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        if '@import "tailwindcss"' not in existing:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write('@import "tailwindcss";\n\n' + existing)
    
    # Modifier index.html
    print("Configuration du HTML...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'src/style.css' not in html_content:
        html_content = html_content.replace(
            '</head>',
            '    <link href="/src/style.css" rel="stylesheet">\n  </head>'
        )
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    # 6. Installer TanStack Query
    print("\n📦 Installation de TanStack Query...")
    if package_manager == 'npm':
        run_command(f"{corepack_prefix}{package_manager} add @tanstack/react-query")
    elif package_manager == 'yarn':
        run_command(f"{corepack_prefix}{package_manager} add @tanstack/react-query")
    elif package_manager == 'pnpm':
        run_command(f"{corepack_prefix}{package_manager} add @tanstack/react-query")
    elif package_manager == 'bun':
        run_command(f"{corepack_prefix}{package_manager} add @tanstack/react-query")
    
    # 7. Demander si l'utilisateur veut Zustand
    use_zustand = get_yes_no("Souhaitez-vous installer Zustand (avec Immer)?")
    
    if use_zustand:
        print("📦 Installation de Zustand et Immer...")
        if package_manager == 'npm':
            run_command(f"{corepack_prefix}{package_manager} add zustand immer")
        elif package_manager == 'yarn':
            run_command(f"{corepack_prefix}{package_manager} add zustand immer")
        elif package_manager == 'pnpm':
            run_command(f"{corepack_prefix}{package_manager} add zustand immer")
        elif package_manager == 'bun':
            run_command(f"{corepack_prefix}{package_manager} add zustand immer")
    
    # 8. Installer les dépendances de test
    print("\n📦 Installation des outils de test...")
    test_deps = "vitest jsdom @testing-library/jest-dom @testing-library/react @testing-library/user-event @testing-library/dom msw @vitest/ui"
    
    if package_manager == 'npm':
        run_command(f"{corepack_prefix}{package_manager} install --save-dev {test_deps}")
    elif package_manager == 'yarn':
        run_command(f"{corepack_prefix}{package_manager} add --dev {test_deps}")
    elif package_manager == 'pnpm':
        run_command(f"{corepack_prefix}{package_manager} add -D {test_deps}")
    elif package_manager == 'bun':
        run_command(f"{corepack_prefix}{package_manager} add --dev {test_deps}")
    
    # 9. Installer le plugin ESLint pour Vitest
    print("📦 Installation du plugin ESLint pour Vitest...")
    if package_manager == 'npm':
        run_command(f"{corepack_prefix}{package_manager} install --save-dev eslint-plugin-vitest-globals")
    elif package_manager == 'yarn':
        run_command(f"{corepack_prefix}{package_manager} add --dev eslint-plugin-vitest-globals")
    elif package_manager == 'pnpm':
        run_command(f"{corepack_prefix}{package_manager} add -D eslint-plugin-vitest-globals")
    elif package_manager == 'bun':
        run_command(f"{corepack_prefix}{package_manager} add --dev eslint-plugin-vitest-globals")
    
    # 10. Modifier package.json pour ajouter les scripts de test
    print("✏️ Ajout des scripts de test...")
    with open('package.json', 'r', encoding='utf-8') as f:
        package_json = json.load(f)
    
    package_json['scripts']['test'] = 'vitest'
    package_json['scripts']['test:ui'] = 'vitest --ui'
    
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package_json, f, indent=2)
    
    # 11. Créer le fichier de setup
    print("✏️ Création du fichier de setup...")
    os.makedirs('src/__tests__', exist_ok=True)
    setup_content = """import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'

afterEach(() => {
  cleanup();
})
"""
    with open('src/__tests__/setup.ts', 'w', encoding='utf-8') as f:
        f.write(setup_content)
    
    # 11.5 Mettre à jour App.tsx avec Tailwind et informations de versions
    print("✏️ Mise à jour de App.tsx...")
    
    # Lire les versions du package.json
    with open('package.json', 'r', encoding='utf-8') as f:
        pkg_data = json.load(f)
    
    # Extraire les versions
    vite_version = pkg_data.get('devDependencies', {}).get('vite', '7.2.4').replace('^', '').replace('~', '')
    react_version = pkg_data.get('dependencies', {}).get('react', '19.2.0').replace('^', '').replace('~', '')
    tailwind_version = pkg_data.get('dependencies', {}).get('tailwindcss', '4.1.18').replace('^', '').replace('~', '')
    tanstack_version = pkg_data.get('dependencies', {}).get('@tanstack/react-query', '5.90.18').replace('^', '').replace('~', '')
    vitest_version = pkg_data.get('devDependencies', {}).get('vitest', '4.0.17').replace('^', '').replace('~', '')
    jsdom_version = pkg_data.get('devDependencies', {}).get('jsdom', '27.4.0').replace('^', '').replace('~', '')
    msw_version = pkg_data.get('devDependencies', {}).get('msw', '2.12.7').replace('^', '').replace('~', '')
    typescript_version = pkg_data.get('devDependencies', {}).get('typescript', '5.9.3').replace('^', '').replace('~', '').replace('~', '')
    zustand_version = pkg_data.get('dependencies', {}).get('zustand', '')
    
    # Construire les lignes de version
    versions_lines = f"""    vite: '{vite_version}',
    nodejs: 'v20+',
    react: '{react_version}',
    tailwind: '{tailwind_version}',
    tanstackQuery: '{tanstack_version}',
    vitest: '{vitest_version}',
    jsdom: '{jsdom_version}',
    msw: '{msw_version}',
    typescript: '{typescript_version}',"""
    
    if zustand_version:
        versions_lines += f"\n    zustand: '{zustand_version}',"
    
    zustand_card = f"""
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-rose-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">Zustand</p>
            <p className="text-2xl font-bold text-rose-400">{{versions.zustand}}</p>
          </div>""" if zustand_version else ""
    
    app_tsx_content = f"""import './App.css'

export function App() {{
  const versions = {{
{versions_lines}
  }}

  const technologies = [
    {{
      name: 'Vite',
      description: 'Un outil de build ultra-rapide et un serveur de développement pour les applications modernes.',
    }},
    {{
      name: 'React',
      description: 'Bibliothèque JavaScript pour construire des interfaces utilisateur avec des composants réutilisables.',
    }},
    {{
      name: 'Tailwind CSS',
      description: 'Framework CSS utilitaire pour créer rapidement des designs modernes et responsifs.',
    }},
    {{
      name: 'TanStack Query',
      description: 'Gestionnaire d\\'état puissant pour synchroniser, mettre en cache et mettre à jour les données asynchrones.',
    }},
    {{
      name: 'Vitest',
      description: 'Framework de test unitaire ultra-rapide alimenté par Vite.',
    }},
    {{
      name: 'jsdom',
      description: 'Implémentation JavaScript du DOM pour tester les composants dans un environnement isolé.',
    }},
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {{/* Header */}}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
            React Advanced Front <span className="text-2xl text-slate-400">v0.1</span>
          </h1>
          <p className="text-xl text-slate-400">Stack moderne pour des applications React performantes</p>
        </div>

        {{/* Versions */}}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 mb-12 max-w-6xl mx-auto">
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-blue-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">Vite</p>
            <p className="text-2xl font-bold text-blue-400">{{versions.vite}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-green-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">Node.js</p>
            <p className="text-2xl font-bold text-green-400">{{versions.nodejs}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-cyan-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">React</p>
            <p className="text-2xl font-bold text-cyan-400">{{versions.react}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-purple-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">Tailwind</p>
            <p className="text-2xl font-bold text-purple-400">{{versions.tailwind}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-orange-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">TanStack</p>
            <p className="text-2xl font-bold text-orange-400">{{versions.tanstackQuery}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-red-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">Vitest</p>
            <p className="text-2xl font-bold text-red-400">{{versions.vitest}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-yellow-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">jsdom</p>
            <p className="text-2xl font-bold text-yellow-400">{{versions.jsdom}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-indigo-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">TypeScript</p>
            <p className="text-2xl font-bold text-indigo-400">{{versions.typescript}}</p>
          </div>
          <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg p-4 border border-slate-600/50 hover:border-pink-500/50 transition">
            <p className="text-slate-400 text-sm uppercase tracking-wider">MSW</p>
            <p className="text-2xl font-bold text-pink-400">{{versions.msw}}</p>
          </div>{zustand_card}
        </div>

        {{/* Technologies Description */}}
        <div className="max-w-4xl mx-auto mb-12">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">À Propos des Technologies</h2>
          <div className="grid gap-6 md:grid-cols-2">
            {{technologies.map((tech) => (
              <div
                key={{tech.name}}
                className="bg-slate-700/30 backdrop-blur-sm rounded-lg p-6 border border-slate-600/50 hover:border-slate-500/50 transition group"
              >
                <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-blue-400 transition">
                  {{tech.name}}
                </h3>
                <p className="text-slate-300 leading-relaxed">{{tech.description}}</p>
              </div>
            ))}}
          </div>
        </div>

        {{/* Footer */}}
        <div className="text-center pt-12 border-t border-slate-700/50">
          <p className="text-slate-400 text-lg">
            Créé par <a href="https://github.com/tomlrd" target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-400 hover:underline">@tomlrd</a> pour{{' '}}
            <a href="https://www.lereacteur.io/" target="_blank" rel="noopener noreferrer" className="font-semibold text-purple-400 hover:underline">Le Reacteur</a>
          </p>
        </div>
      </div>
    </div>
  )
}}

export default App
"""
    
    with open('src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_tsx_content)
    
    # Mettre à jour App.css pour être minimaliste avec Tailwind
    print("✏️ Mise à jour de App.css...")
    app_css_content = """#root {
  width: 100%;
  margin: 0 auto;
}
"""
    with open('src/App.css', 'w', encoding='utf-8') as f:
        f.write(app_css_content)
    
    print("\n========================================")
    print("  Configuration terminée!")
    print("========================================")
    print(f"\nVotre projet est prêt dans le dossier: {project_name if project_name != '.' else 'courant'}")
    print(f"Gestionnaire de paquets utilisé: {package_manager}")
    print(f"Tailwind CSS: ✓ Installé")
    print(f"Zustand: {'✓ Installé' if use_zustand else '✗ Non installé'}")
    print(f"Testing Library: ✓ Installé")
    print(f"\nCommandes utiles:")
    print(f"  - Démarrer le serveur: {package_manager} run dev")
    print(f"  - Lancer les tests: {package_manager} run test")
    print(f"  - Tests avec UI: {package_manager} run test:ui")
    print(f"  - Build: {package_manager} run build")

if __name__ == '__main__':
    main()

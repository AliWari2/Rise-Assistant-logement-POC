🏠 Assistant Logement – PoC Rise
Prototype d’assistant conversationnel utilisant un modèle LLM pour analyser et guider les locataires face aux problèmes courants dans un logement.
PoC réalisé par Ali Wari
Dans le cadre du processus de recrutement – Alternance Développeur d’applications IA & LLM chez Rise.

🚀 Objectif du PoC
Ce prototype a été conçu pour démontrer :
La capacité à concevoir un produit IA complet (UX + logique métier + intégration LLM)
L’utilisation d’un modèle de langage (LLM) pour analyser des descriptions en langage naturel
La génération de conseils actionnables, structurés et compréhensibles pour un locataire
L’intégration d’une base de connaissances métier (logement)
La mise en place d’une interface utilisateur claire, moderne et agréable (Streamlit)
La gestion d’un système d’historique de conversations, pouvant alimenter un futur back-office Rise
🧠 Fonctionnement général
L’utilisateur décrit un problème rencontré dans son logement (ex. "je n’ai plus d’eau chaude", "j'ai une fuite au plafond", etc.).
Le modèle LLM :
Analyse le problème
Croise avec une base de connaissances (fuite, eau chaude, serrure, bruit, moisissures…)
Produit une réponse structurée selon 4 sections :
Analyse du problème
Actions immédiates
Qui prévenir ?
Niveau d'urgence
Le résultat est affiché sous forme d’assistant conversationnel.
🛠️ Stack technique
Composant	Description
Python 3.10+	Langage principal
Streamlit	Interface utilisateur (front-end moderne et rapide)
Groq LLM – modèle llama-3.1-8b-instant	Modèle IA utilisé pour l’analyse et la génération
python-dotenv	Gestion sécurisée des clés API
JSON	Sauvegarde des conversations
📁 Structure du projet
Rise_Poc/
│
├── app.py                      # Application principale Streamlit
├── connaissances_logement.txt  # Base de connaissances métier
├── requirements.txt            # Dépendances Python
├── .env                        # Clé API GROQ (non inclus dans l'envoi)
├── conversations/              # Historique enregistré au format JSON
└── README.md                   # Documentation du projet
🔧 Installation & Lancement
1️⃣ Accéder au dossier du projet
cd Rise_Poc
2️⃣ Créer un environnement virtuel (optionnel mais recommandé)
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
3️⃣ Installer les dépendances
pip install -r requirements.txt
4️⃣ Créer le fichier .env
Créer un fichier .env à la racine du projet :
GROQ_API_KEY=votre_cle_ici
5️⃣ Lancer l’application
streamlit run app.py
L'application sera accessible à l’adresse :
➡️ http://localhost:8501

🎨 Design & Expérience Utilisateur
L'interface a été pensée pour être :
Sobre et élégante, inspirée des interfaces SaaS modernes
Facile à utiliser, même pour un locataire non technique
Responsive, adaptée à différents écrans
Organisée avec une séparation claire entre :
le chat (zone principale)
les informations complémentaires & exemples
l’historique des conversations
Un thème CSS personnalisé est utilisé pour dépasser l’apparence classique de Streamlit.
📈 Axes d’amélioration possibles pour Rise
Ce PoC ouvre la voie à une version plus complète :
🔹 1. Back-office gestionnaire
Consultation des tickets créés par les locataires
Suivi des interventions
Analyse statistique des incidents (bruit, fuite, serrure…)
🔹 2. Classification automatique des problèmes
L’IA pourrait identifier automatiquement :
la catégorie du problème
le niveau d’urgence
le service à alerter
🔹 3. Multicanal
Déploiement possible sur :
WhatsApp
Email interactif
Espace locataire Rise
🔹 4. Connexion à une base de données
Pour un suivi en temps réel des logements, demandes et SLA.
🔹 5. Enrichissement progressif de la base de connaissances
Avec les incidents réels rencontrés par Rise.
👤 Auteur
Ali Wari
Étudiant en Master – Futur alternant Développeur IA / Full-Stack.
Passionné par la PropTech, l’IA appliquée et le développement de produits utiles.
🙏 Remerciements
Merci à l’équipe Rise pour l’opportunité et l’intérêt porté à ce PoC.
Ce prototype est une première étape : il illustre une vision concrète, rapide et ambitieuse
de ce qu’un assistant IA peut apporter à la gestion locative moderne.

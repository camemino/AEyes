# Presentation d'avancement - A-Eyes

## Objectif du document

Ce document sert de base de travail pour une presentation d'avancement du projet A-Eyes.
Il est construit pour 10 slides et 10 minutes de presentation, avec un angle jury / encadrants.

Tous les visuels mentionnes dans ce document sont a concevoir sous forme de schemas Excalidraw integres a la presentation.
Il n'y a pas de visuels Marp ni Mermaid dans cette version de travail.

Structure imposee par le jury :

1. **Bloc 1 — Contexte (1 min, slide 1)** : breve presentation du projet, probleme vise, produit attendu en juin
2. **Bloc 2 — Avancement (7 min, slides 2 a 7)** : avancement concret fonctionnalite par fonctionnalite, justification de l'effort (3 reunions de 7h)
3. **Bloc 3 — Planning rectifie (2 min, slides 8 a 10)** : estimation de l'effort, planning detaille semaine par semaine, synthese

---

# BLOC 1 — CONTEXTE (1 minute)

---

## Slide 1 - Titre, contexte et perimetre V0

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Titre principal centre avec visuel de l'oeil issu du PDF. En dessous, deux blocs cote a cote : a gauche le probleme vise, a droite le perimetre V0. Simple et rapide a lire.</td>
		<td>
			<ul>
				<li>A-Eyes — Presentation d'avancement V0</li>
				<li>Avril 2026 — Equipe de 5 eleves</li>
				<li>Probleme : les personnes malvoyantes manquent d'outils simples pour percevoir leur environnement</li>
				<li>Produit attendu en juin : application mobile avec IA de description de scene et guidage vocal</li>
				<li>Perimetre V0 : interface accessible, camera, synthese vocale, commandes vocales de base (pas d'IA)</li>
			</ul>
		</td>
		<td>Bonjour. A-Eyes aide les personnes malvoyantes a percevoir leur environnement grace a une application mobile qui decrit ce que voit la camera. Aujourd'hui on presente le prototype V0 : on a mis en place l'interface, la camera, le guidage vocal et les commandes vocales. L'intelligence artificielle arrivera dans la version suivante. On va vous montrer ce qu'on a fait, puis le planning pour la suite.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

Reference visuelle issue du PDF a reutiliser dans le slide 1 :

![Visuel de couverture extrait du PDF](pdf_cover_asset_X5.png)

<div align="center">
<svg viewBox="0 0 820 280" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="260" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<text x="410" y="42" text-anchor="middle" font-size="28" fill="#173b36" font-family="Segoe UI">A-Eyes</text>
	<text x="410" y="64" text-anchor="middle" font-size="14" fill="#5a6d68" font-family="Segoe UI">Avancement du prototype V0 — Avril 2026 — 5 eleves</text>
	<ellipse cx="410" cy="100" rx="58" ry="28" fill="#fff7d1" stroke="#173b36" stroke-width="2"/>
	<circle cx="410" cy="100" r="10" fill="#173b36"/>
	<rect x="56" y="146" width="320" height="100" rx="18" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<rect x="444" y="146" width="320" height="100" rx="18" fill="#fff7d1" stroke="#a88723" stroke-width="2"/>
	<text x="216" y="174" text-anchor="middle" font-size="18" fill="#173b36" font-family="Segoe UI">Probleme vise</text>
	<text x="604" y="174" text-anchor="middle" font-size="18" fill="#5a480e" font-family="Segoe UI">Perimetre V0</text>
	<g font-size="13" font-family="Segoe UI">
		<text x="82" y="200" fill="#173b36">Accessibilite pour malvoyants</text>
		<text x="82" y="220" fill="#173b36">Interface simple + guidage vocal</text>
		<text x="82" y="240" fill="#173b36">Produit final avec IA en juin</text>
		<text x="470" y="200" fill="#5a480e">Interface accessible</text>
		<text x="470" y="220" fill="#5a480e">Camera + TTS + commandes vocales</text>
		<text x="470" y="240" fill="#5a480e">Pas d'IA a ce stade</text>
	</g>
</svg>
</div>

Elements a faire apparaitre :

- reprendre le visuel de l'oeil extrait de la couverture du PDF comme ancrage visuel principal
- titre A-Eyes centre, sous-titre avec date et taille de l'equipe
- deux blocs en bas : probleme vise a gauche, perimetre V0 a droite
- garder la composition sobre et lisible en moins de 10 secondes

Objectif du visuel : poser le projet, le besoin et le perimetre V0 en une seule slide rapide.

---

# BLOC 2 — AVANCEMENT CONCRET (7 minutes)

---

## Slide 2 - Vue d'ensemble de l'avancement

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Deux zones bien distinctes avec code couleur vert/orange. Une mention de l'effort global en bas de slide.</td>
		<td>
			<ul>
				<li>Deja operationnel</li>
				<li>Camera active avec flux en direct</li>
				<li>Interface accessible (4 boutons, fort contraste)</li>
				<li>Navigation entre ecrans (principal + reglages)</li>
				<li>Guidage vocal a chaque action</li>
				<li>Commandes vocales de base (6 commandes)</li>
				<li>Encore simule</li>
				<li>Fonction Describe (placeholder V0, IA prevue en V1)</li>
				<li>Effort V0 : 3 reunions de 7h par eleve</li>
			</ul>
		</td>
		<td>Voici ou on en est. Cinq choses fonctionnent deja : la camera, l'interface avec de gros boutons bien visibles, la navigation entre ecrans, le guidage vocal et les commandes a la voix. La seule chose qui manque c'est la description intelligente de l'image, prevue pour la V1. Tout ca a ete fait en trois reunions de sept heures. On va maintenant detailler chaque partie.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 260" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="240" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<text x="410" y="38" text-anchor="middle" font-size="16" fill="#5a6d68" font-family="Segoe UI">Prototype V0 — Etat d'avancement</text>
	<rect x="56" y="56" width="360" height="156" rx="18" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<rect x="444" y="56" width="320" height="100" rx="18" fill="#fbefef" stroke="#b56b6b" stroke-width="2"/>
	<text x="236" y="84" text-anchor="middle" font-size="20" fill="#173b36" font-family="Segoe UI">Deja operationnel</text>
	<text x="604" y="84" text-anchor="middle" font-size="20" fill="#7a3030" font-family="Segoe UI">Encore simule</text>
	<g font-size="14" font-family="Segoe UI">
		<text x="82" y="112" fill="#173b36">✓ Camera en temps reel</text>
		<text x="82" y="134" fill="#173b36">✓ Interface accessible (4 boutons)</text>
		<text x="82" y="156" fill="#173b36">✓ Navigation entre ecrans</text>
		<text x="82" y="178" fill="#173b36">✓ Guidage vocal</text>
		<text x="82" y="200" fill="#173b36">✓ Commandes vocales (6 commandes)</text>
		<text x="470" y="122" fill="#7a3030">○ Describe (placeholder)</text>
		<text x="470" y="146" fill="#7a3030">○ Analyse IA → V1</text>
	</g>
	<rect x="444" y="176" width="320" height="36" rx="14" fill="#fff7d1" stroke="#a88723"/>
	<text x="604" y="200" text-anchor="middle" font-size="14" fill="#5a480e" font-family="Segoe UI">Effort V0 : 3 reunions de 7h / eleve</text>
</svg>
</div>

Elements a faire apparaitre :

- deux zones : operationnel (vert) et simule (orange/rouge)
- liste des 5 fonctionnalites livrees avec coches
- liste des elements simules avec cercles vides
- encart en bas rappelant l'effort global de l'equipe
- lecture immediate en un coup d'oeil

Objectif du visuel : donner une vue d'ensemble rapide avant d'entrer dans le detail.

---

## Slide 3 - Avancement : interface accessible

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Slide en deux parties : a gauche une capture d'ecran stylisee du prototype (ou schema de l'ecran), a droite les points cles fonctionnels.</td>
		<td>
			<ul>
				<li>4 boutons principaux : SCAN (jaune), DESCRIBE (vert), REPEAT (bleu), SETTINGS (gris)</li>
				<li>Fond noir, fort contraste, gros boutons</li>
				<li>Sortie camera affichee pour verification — absente de la solution finale</li>
				<li>Navigation entre 2 ecrans : principal et reglages</li>
				<li>Layout Kivy declaratif (.kv) pour separation logique/presentation</li>
			</ul>
		</td>
		<td>L'interface est pensee pour des personnes malvoyantes : fond noir, gros boutons de couleurs vives, tres facile a lire. Le bouton Scan est le plus grand car c'est l'action principale. La camera s'affiche ici pour verifier qu'elle marche, mais elle disparaitra dans la version finale. Il y a aussi un ecran de reglages pour ajuster la vitesse de la voix. L'interface et le code sont separes dans deux fichiers distincts, ce qui facilite les modifications.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 360" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="340" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<!-- Ecran principal stylise -->
	<rect x="56" y="36" width="240" height="260" rx="22" fill="#000000" stroke="#173b36" stroke-width="3"/>
	<rect x="76" y="60" width="200" height="100" rx="10" fill="#1a1a1a" stroke="#333"/>
	<text x="176" y="110" text-anchor="middle" font-size="12" fill="#666" font-family="Segoe UI">Camera preview</text>
	<text x="176" y="128" text-anchor="middle" font-size="9" fill="#994444" font-family="Segoe UI">(debug uniquement — absent en version finale)</text>
	<rect x="76" y="172" width="200" height="28" rx="8" fill="rgb(255,204,0)" stroke="none"/>
	<text x="176" y="192" text-anchor="middle" font-size="14" fill="#000" font-family="Segoe UI" font-weight="bold">SCAN</text>
	<rect x="76" y="206" width="200" height="22" rx="8" fill="rgb(26,179,77)" stroke="none"/>
	<text x="176" y="222" text-anchor="middle" font-size="12" fill="#fff" font-family="Segoe UI" font-weight="bold">DESCRIBE</text>
	<rect x="76" y="234" width="200" height="20" rx="8" fill="rgb(51,153,255)" stroke="none"/>
	<text x="176" y="248" text-anchor="middle" font-size="12" fill="#fff" font-family="Segoe UI" font-weight="bold">REPEAT</text>
	<rect x="76" y="260" width="200" height="18" rx="8" fill="rgb(77,77,77)" stroke="none"/>
	<text x="176" y="274" text-anchor="middle" font-size="11" fill="#fff" font-family="Segoe UI" font-weight="bold">SETTINGS</text>
	<!-- Extrait de code KV a droite -->
	<text x="340" y="52" fill="#173b36" font-size="18" font-weight="bold" font-family="Segoe UI">Extrait du fichier a_eyes.kv</text>
	<rect x="340" y="62" width="430" height="228" rx="12" fill="#1e1e1e" stroke="#333" stroke-width="2"/>
	<g font-family="Consolas, monospace" font-size="12" fill="#d4d4d4">
		<text x="358" y="86" fill="#569cd6">&lt;MainScreen&gt;:</text>
		<text x="358" y="106" fill="#6a9955">    canvas.before:</text>
		<text x="358" y="122" fill="#d4d4d4">        Color:</text>
		<text x="358" y="138" fill="#b5cea8">            rgba: 0, 0, 0, 1</text>
		<text x="358" y="162" fill="#6a9955">    BoxLayout:</text>
		<text x="358" y="178" fill="#d4d4d4">        orientation: "vertical"</text>
		<text x="358" y="198" fill="#569cd6">        Button:</text>
		<text x="358" y="214" fill="#ce9178">            text: "SCAN"</text>
		<text x="358" y="230" fill="#b5cea8">            height: "110dp"</text>
		<text x="358" y="246" fill="#b5cea8">            background_color: 1, 0.8, 0, 1</text>
		<text x="358" y="266" fill="#569cd6">        Button:</text>
		<text x="358" y="282" fill="#ce9178">            text: "DESCRIBE"</text>
	</g>
	<!-- Label -->
	<rect x="340" y="300" width="430" height="36" rx="10" fill="#fff7d1" stroke="#a88723"/>
	<text x="555" y="324" text-anchor="middle" font-size="13" fill="#5a480e" font-family="Segoe UI">Separation code/UI → layout declaratif sans toucher au Python</text>
</svg>
</div>

Elements a faire apparaitre :

- a gauche : representation stylisee de l'ecran du prototype avec les 4 boutons colores empiles sur fond noir
- a droite : extrait reel du fichier a_eyes.kv montrant le code declaratif (fond sombre style editeur de code)
- si une capture d'ecran reelle du prototype est disponible, la placer a la place du schema de gauche

Objectif du visuel : montrer concretement l'interface ET le code declaratif qui la definit.

---

## Slide 4 - Avancement : architecture inputs / outputs et threads

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Schema d'architecture centree sur les flux d'entree et de sortie. Le thread principal (UI Kivy) est au centre, avec les threads d'ecoute (camera, micro) a gauche et les threads de sortie (affichage, voix) a droite. Les threads sont visuellement distincts du thread principal.</td>
		<td>
			<ul>
				<li>Thread principal : interface Kivy (boucle UI)</li>
				<li>Thread camera : capture video OpenCV en continu</li>
				<li>Thread ecoute vocale : micro en ecoute permanente</li>
				<li>Thread synthese vocale : file de messages lus a la suite</li>
				<li>Inputs : camera + micro + boutons tactiles</li>
				<li>Outputs : ecran (texture) + haut-parleur (voix)</li>
			</ul>
		</td>
		<td>Ici on voit comment l'application fait plusieurs choses en meme temps. L'interface tourne en continu, et a cote, trois taches paralleles fonctionnent sans la bloquer : une pour la camera, une pour ecouter le micro, et une pour parler a l'utilisateur. Sans cette separation, l'ecran se figerait a chaque fois que l'appli prend une photo ou lit un message. A gauche les entrees — camera, micro, boutons — et a droite les sorties — ecran et haut-parleur.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 360" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="340" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<!-- Titre -->
	<text x="410" y="38" text-anchor="middle" font-size="16" fill="#5a6d68" font-family="Segoe UI">Architecture threads — Inputs / Outputs</text>
	<!-- INPUTS a gauche -->
	<text x="80" y="68" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI" font-weight="bold">INPUTS</text>
	<!-- Camera input -->
	<rect x="30" y="82" width="100" height="50" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="80" y="104" text-anchor="middle" font-size="13" fill="#173b36" font-family="Segoe UI">Camera</text>
	<text x="80" y="122" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">OpenCV</text>
	<!-- Boutons input -->
	<rect x="30" y="148" width="100" height="50" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="80" y="170" text-anchor="middle" font-size="13" fill="#173b36" font-family="Segoe UI">Boutons</text>
	<text x="80" y="188" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Tactile (on_press)</text>
	<!-- Micro input -->
	<rect x="30" y="214" width="100" height="50" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="80" y="236" text-anchor="middle" font-size="13" fill="#173b36" font-family="Segoe UI">Micro</text>
	<text x="80" y="254" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">SpeechRecognition</text>
	<!-- THREAD CAMERA (ecoute) -->
	<rect x="170" y="74" width="160" height="66" rx="16" fill="#fce8e8" stroke="#b56b6b" stroke-width="2" stroke-dasharray="6 4"/>
	<text x="250" y="98" text-anchor="middle" font-size="13" fill="#7a3030" font-family="Segoe UI" font-weight="bold">Thread Camera</text>
	<text x="250" y="116" text-anchor="middle" font-size="11" fill="#7a3030" font-family="Segoe UI">capture en continu</text>
	<text x="250" y="132" text-anchor="middle" font-size="10" fill="#b56b6b" font-family="Segoe UI">→ envoie les frames</text>
	<!-- THREAD ECOUTE VOCALE (ecoute) -->
	<rect x="170" y="206" width="160" height="66" rx="16" fill="#fce8e8" stroke="#b56b6b" stroke-width="2" stroke-dasharray="6 4"/>
	<text x="250" y="230" text-anchor="middle" font-size="13" fill="#7a3030" font-family="Segoe UI" font-weight="bold">Thread Ecoute</text>
	<text x="250" y="248" text-anchor="middle" font-size="11" fill="#7a3030" font-family="Segoe UI">micro en permanence</text>
	<text x="250" y="264" text-anchor="middle" font-size="10" fill="#b56b6b" font-family="Segoe UI">→ envoie les commandes</text>
	<!-- THREAD PRINCIPAL (centre) -->
	<rect x="370" y="110" width="160" height="110" rx="20" fill="#fff7d1" stroke="#a88723" stroke-width="3"/>
	<text x="450" y="140" text-anchor="middle" font-size="16" fill="#5a480e" font-family="Segoe UI" font-weight="bold">Thread Principal</text>
	<text x="450" y="162" text-anchor="middle" font-size="13" fill="#5a480e" font-family="Segoe UI">Boucle UI Kivy</text>
	<text x="450" y="182" text-anchor="middle" font-size="11" fill="#5a480e" font-family="Segoe UI">orchestre tout</text>
	<text x="450" y="200" text-anchor="middle" font-size="11" fill="#5a480e" font-family="Segoe UI">ne doit jamais bloquer</text>
	<!-- THREAD TTS (sortie) -->
	<rect x="570" y="192" width="160" height="66" rx="16" fill="#fce8e8" stroke="#b56b6b" stroke-width="2" stroke-dasharray="6 4"/>
	<text x="650" y="216" text-anchor="middle" font-size="13" fill="#7a3030" font-family="Segoe UI" font-weight="bold">Thread TTS</text>
	<text x="650" y="234" text-anchor="middle" font-size="11" fill="#7a3030" font-family="Segoe UI">file de messages</text>
	<text x="650" y="250" text-anchor="middle" font-size="10" fill="#b56b6b" font-family="Segoe UI">lit un par un</text>
	<!-- OUTPUTS a droite -->
	<text x="740" y="68" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI" font-weight="bold">OUTPUTS</text>
	<!-- Ecran output -->
	<rect x="690" y="82" width="100" height="50" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="740" y="104" text-anchor="middle" font-size="13" fill="#173b36" font-family="Segoe UI">Ecran</text>
	<text x="740" y="122" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Kivy Texture</text>
	<!-- Haut-parleur output -->
	<rect x="690" y="268" width="100" height="50" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="740" y="290" text-anchor="middle" font-size="13" fill="#173b36" font-family="Segoe UI">Haut-parleur</text>
	<text x="740" y="308" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Voix synthetisee</text>
	<!-- Fleches INPUT → THREADS ECOUTE -->
	<path d="M130 107 H168" stroke="#4e8c82" stroke-width="2.5"/>
	<polygon points="164,101 178,107 164,113" fill="#4e8c82"/>
	<!-- Fleche Boutons → Thread Principal (directement, pas de thread) -->
	<path d="M130 173 H370" stroke="#4e8c82" stroke-width="2.5"/>
	<polygon points="364,167 378,173 364,179" fill="#4e8c82"/>
	<!-- Fleche Micro → Thread Ecoute -->
	<path d="M130 239 H168" stroke="#4e8c82" stroke-width="2.5"/>
	<polygon points="164,233 178,239 164,245" fill="#4e8c82"/>
	<!-- Fleches THREADS ECOUTE → THREAD PRINCIPAL -->
	<path d="M330 107 Q350 130 370 145" stroke="#b56b6b" stroke-width="2.5"/>
	<polygon points="364,140 376,148 368,152" fill="#b56b6b"/>
	<path d="M330 239 Q350 210 370 190" stroke="#b56b6b" stroke-width="2.5"/>
	<polygon points="364,186 376,188 368,196" fill="#b56b6b"/>
	<!-- Fleche THREAD PRINCIPAL → ECRAN -->
	<path d="M530 145 Q610 120 688 107" stroke="#4e8c82" stroke-width="2.5"/>
	<polygon points="682,101 696,107 684,113" fill="#4e8c82"/>
	<!-- Fleche THREAD PRINCIPAL → THREAD TTS -->
	<path d="M530 190 Q550 210 568 220" stroke="#b56b6b" stroke-width="2.5"/>
	<polygon points="562,214 576,222 566,228" fill="#b56b6b"/>
	<!-- Fleche THREAD TTS → HAUT-PARLEUR -->
	<path d="M730 258 V266" stroke="#4e8c82" stroke-width="2.5"/>
	<polygon points="724,262 740,270 756,262" fill="#4e8c82"/>
	<!-- Legende threads -->
	<rect x="200" y="310" width="420" height="30" rx="10" fill="#ffffff" stroke="#b56b6b" stroke-dasharray="6 4"/>
	<text x="410" y="330" text-anchor="middle" font-size="12" fill="#7a3030" font-family="Segoe UI">Bordure pointillee = thread separe (ne bloque pas l'UI)</text>
</svg>
</div>

Elements a faire apparaitre :

- inputs a gauche : camera (OpenCV), boutons tactiles (on_press) et micro (SpeechRecognition)
- les boutons vont directement au thread principal (pas de thread intermediaire)
- thread principal au centre : boucle UI Kivy qui orchestre tout
- threads separes clairement identifies : camera (capture), ecoute vocale (micro), TTS (sortie)
- outputs a droite : ecran (texture Kivy) et haut-parleur (voix)
- fleches montrant les flux de donnees entre les threads
- legende en bas : bordure pointillee = thread separe

Objectif du visuel : montrer que l'application utilise des threads pour ne jamais bloquer l'interface, avec des inputs et outputs clairement identifies.

---

## Slide 5 - Architecture modulaire, guidage vocal et choix techniques

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Slide en deux parties : schema d'architecture radial en haut avec les modules et les details vocaux integres, tableau des choix techniques en bas.</td>
		<td>
			<ul>
				<li>Architecture : 5 modules autour d'un orchestrateur central</li>
				<li>UI (main_screen.py) → Camera (capture.py) → TTS (speaker.py) → STT (listener.py) → Config</li>
				<li>TTS : moteurs natifs par plateforme (SAPI Windows, AVSpeech Apple, Google TTS Android)</li>
				<li>TTS : thread asynchrone, file de messages, repeat, vitesse reglable</li>
				<li>STT : 6 commandes (scan, describe, repeat, settings, help, stop)</li>
				<li>Kivy : interface multi-plateforme</li>
				<li>OpenCV : capture camera</li>
				<li>Modularite : chaque module est independant → facilite l'integration IA en V1</li>
				<li>Choix de Python : ecosysteme riche en bibliotheques pretes a l'emploi, assemblage rapide en tres peu de code</li>
			</ul>
		</td>
		<td>L'application est decoupee en cinq modules independants. On a choisi Python car il existe beaucoup de bibliotheques pretes a l'emploi et en tres peu de code on peut les assembler entre elles. Kivy gere l'interface sur toutes les plateformes. OpenCV gere la camera. La voix utilise le moteur natif de chaque systeme : Windows, Apple ou Android. Chaque action de l'utilisateur declenche une annonce vocale, et il peut repeter le dernier message ou ajuster la vitesse. Six commandes vocales sont reconnues. Si le micro n'est pas disponible, les boutons restent utilisables. L'avantage de ce decoupage, c'est que chaque module est remplacable. Ces choix techniques ont ete faits pour mettre en place rapidement un V0 fonctionnel, ils ne sont pas definitifs. En V1, on pourra changer de technologie sur n'importe quel module sans impacter les autres, et on ajoutera le module IA sans toucher au reste.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 380" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="360" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<!-- Schema architecture radial -->
	<rect x="300" y="46" width="220" height="64" rx="18" fill="#fff7d1" stroke="#a88723" stroke-width="2"/>
	<text x="410" y="74" text-anchor="middle" font-size="18" fill="#5a480e" font-family="Segoe UI">Ecran principal</text>
	<text x="410" y="96" text-anchor="middle" font-size="12" fill="#5a480e" font-family="Segoe UI">main_screen.py — orchestration</text>
	<!-- UI -->
	<rect x="46" y="36" width="180" height="48" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="136" y="58" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI">UI (a_eyes.kv)</text>
	<text x="136" y="74" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Kivy</text>
	<!-- Camera -->
	<rect x="594" y="36" width="180" height="48" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="684" y="58" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI">Camera (capture.py)</text>
	<text x="684" y="74" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">OpenCV</text>
	<!-- STT avec details -->
	<rect x="46" y="104" width="180" height="72" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="136" y="126" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI">STT (listener.py)</text>
	<text x="136" y="142" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">SpeechRecognition</text>
	<text x="136" y="156" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">6 commandes vocales</text>
	<!-- TTS avec details -->
	<rect x="594" y="104" width="180" height="72" rx="14" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="684" y="126" text-anchor="middle" font-size="14" fill="#173b36" font-family="Segoe UI">TTS (speaker.py)</text>
	<text x="684" y="142" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">SAPI / AVSpeech / Google TTS</text>
	<text x="684" y="156" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Thread async + file de messages</text>
	<text x="684" y="170" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Repeat | Vitesse reglable</text>
	<!-- Fleches -->
	<path d="M226 60 C270 60 280 66 300 72" fill="none" stroke="#8a9e98" stroke-width="2.5"/>
	<path d="M594 60 C548 60 540 66 520 72" fill="none" stroke="#8a9e98" stroke-width="2.5"/>
	<path d="M226 136 C270 126 290 116 310 110" fill="none" stroke="#8a9e98" stroke-width="2.5"/>
	<path d="M594 136 C548 126 530 116 510 110" fill="none" stroke="#8a9e98" stroke-width="2.5"/>
	<!-- Module IA fantome pour V1 -->
	<rect x="330" y="130" width="160" height="36" rx="14" fill="#ffffff" stroke="#b56b6b" stroke-dasharray="6 4"/>
	<text x="410" y="154" text-anchor="middle" font-size="13" fill="#b56b6b" font-family="Segoe UI">Module IA → V1</text>
	<!-- Tableau choix techniques en bas -->
	<line x1="40" y1="200" x2="780" y2="200" stroke="#d7d1c2" stroke-width="1"/>
	<text x="410" y="224" text-anchor="middle" font-size="16" fill="#173b36" font-family="Segoe UI" font-weight="bold">Choix techniques</text>
	<g font-size="13" font-family="Segoe UI">
		<rect x="46" y="240" width="170" height="56" rx="14" fill="#eef6f5" stroke="#4e8c82"/>
		<text x="131" y="264" text-anchor="middle" fill="#173b36" font-size="16">Kivy</text>
		<text x="131" y="284" text-anchor="middle" fill="#5a6d68">Multi-plateforme</text>
		<rect x="232" y="240" width="170" height="56" rx="14" fill="#eef6f5" stroke="#4e8c82"/>
		<text x="317" y="264" text-anchor="middle" fill="#173b36" font-size="16">OpenCV</text>
		<text x="317" y="284" text-anchor="middle" fill="#5a6d68">Camera robuste</text>
		<rect x="418" y="240" width="170" height="56" rx="14" fill="#fff7d1" stroke="#a88723"/>
		<text x="503" y="264" text-anchor="middle" fill="#5a480e" font-size="16">TTS</text>
		<text x="503" y="284" text-anchor="middle" fill="#5a480e">Moteurs natifs par plateforme</text>
		<rect x="604" y="240" width="170" height="56" rx="14" fill="#eef6f5" stroke="#4e8c82"/>
		<text x="689" y="264" text-anchor="middle" fill="#173b36" font-size="14">SpeechRecognition</text>
		<text x="689" y="284" text-anchor="middle" fill="#5a6d68">Mains libres</text>
	</g>
	<!-- Phrase choix Python + decoupage -->
	<rect x="46" y="310" width="728" height="40" rx="12" fill="#fff7d1" stroke="#a88723"/>
	<text x="410" y="328" text-anchor="middle" font-size="12" fill="#5a480e" font-family="Segoe UI">Python : ecosysteme riche, bibliotheques pretes a l'emploi, assemblage rapide en peu de code</text>
	<text x="410" y="344" text-anchor="middle" font-size="12" fill="#5a480e" font-family="Segoe UI">Architecture : une classe par module → independance, testabilite, evolution facile vers V1</text>
</svg>
</div>

Elements a faire apparaitre :

- schema radial avec l'orchestrateur au centre et les 4 modules autour
- modules TTS et STT enrichis avec leurs details (file de messages, 6 commandes)
- module IA en pointille (prevu V1)
- tableau des 4 technologies en bas avec justification 1 ligne

Objectif du visuel : montrer l'architecture complete avec les details vocaux et les choix techniques en une seule slide.

---

## Slide 6 - Limites actuelles et points ouverts

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Trois cartes de limites avec un code couleur progressif (vert/orange/rouge). Pour chaque limite, un contournement ou une perspective est indique en dessous.</td>
		<td>
			<ul>
				<li>IA de description non integree → prevue en V1</li>
				<li>Commandes vocales dependantes du reseau (Google STT) → boutons tactiles en secours</li>
				<li>Accessibilite native incomplete : Kivy est tres bien pour un prototype mais tres limite pour une application native sur telephone → plan V1 : migration vers Flutter ou React Native</li>
				<li>Contraintes deja respectees : fort contraste, gros boutons, retour vocal, pas de stockage local (RGPD)</li>
			</ul>
		</td>
		<td>On a identifie trois limites. Premierement, l'IA n'est pas encore connectee, c'est prevu pour la V1. Deuxiemement, les commandes vocales ont besoin d'internet. Si le reseau n'est pas la, l'appli reste utilisable avec les boutons. Troisiemement, Kivy est tres bien pour monter un prototype rapidement, mais c'est tres limite pour une vraie application sur telephone. Par exemple, les lecteurs d'ecran du telephone ne peuvent pas lire nos boutons. Pour compenser, on a mis un retour vocal a chaque action. En V1, on prevoit de migrer vers une technologie plus adaptee au mobile. En revanche, plusieurs points sont deja bons : fort contraste, gros boutons, retour vocal permanent, et aucune donnee stockee sur le telephone.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 280" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="260" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<text x="410" y="38" text-anchor="middle" font-size="18" fill="#173b36" font-family="Segoe UI">Limites identifiees et contournements</text>
	<!-- Carte 1 : IA -->
	<rect x="40" y="56" width="220" height="90" rx="18" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="150" y="82" text-anchor="middle" font-size="16" fill="#173b36" font-family="Segoe UI">IA non integree</text>
	<text x="150" y="106" text-anchor="middle" font-size="12" fill="#5a6d68" font-family="Segoe UI">Placeholder en V0</text>
	<text x="150" y="126" text-anchor="middle" font-size="12" fill="#4e8c82" font-family="Segoe UI">→ Prevue en V1</text>
	<!-- Carte 2 : Reseau -->
	<rect x="300" y="56" width="220" height="90" rx="18" fill="#fff7d1" stroke="#a88723" stroke-width="2"/>
	<text x="410" y="82" text-anchor="middle" font-size="16" fill="#5a480e" font-family="Segoe UI">Dependance reseau</text>
	<text x="410" y="106" text-anchor="middle" font-size="12" fill="#5a480e" font-family="Segoe UI">Google STT requiert internet</text>
	<text x="410" y="126" text-anchor="middle" font-size="12" fill="#a88723" font-family="Segoe UI">→ Boutons tactiles en secours</text>
	<!-- Carte 3 : Accessibilite -->
	<rect x="560" y="46" width="220" height="110" rx="18" fill="#fce8e8" stroke="#b56b6b" stroke-width="2.5"/>
	<text x="670" y="72" text-anchor="middle" font-size="16" fill="#7a3030" font-family="Segoe UI">Kivy : limite sur mobile</text>
	<text x="670" y="96" text-anchor="middle" font-size="12" fill="#7a3030" font-family="Segoe UI">Tres bien pour un prototype</text>
	<text x="670" y="112" text-anchor="middle" font-size="12" fill="#7a3030" font-family="Segoe UI">mais limite en natif telephone</text>
	<text x="670" y="136" text-anchor="middle" font-size="12" fill="#b56b6b" font-family="Segoe UI">→ TTS interne + plan V1</text>
	<!-- Contraintes respectees en bas -->
	<rect x="40" y="180" width="740" height="70" rx="18" fill="#eef6f5" stroke="#4e8c82" stroke-width="2"/>
	<text x="410" y="206" text-anchor="middle" font-size="16" fill="#173b36" font-family="Segoe UI">Contraintes deja respectees</text>
	<g font-size="13" font-family="Segoe UI" text-anchor="middle">
		<text x="150" y="234" fill="#173b36">Fort contraste</text>
		<text x="320" y="234" fill="#173b36">Gros boutons</text>
		<text x="490" y="234" fill="#173b36">Retour vocal</text>
		<text x="670" y="234" fill="#173b36">Pas de stockage (RGPD)</text>
	</g>
</svg>
</div>

Elements a faire apparaitre :

- 3 cartes de limites avec degradation de couleur (vert → jaune → rouge)
- sous chaque carte, le contournement choisi
- en bas, un bandeau rappelant les contraintes deja respectees

Objectif du visuel : montrer les risques de maniere maitrisee, avec des solutions identifiees.

---

## Slide 7 - Demo du prototype V0

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Slide sobre avec le titre "Demo V0" et une capture d'ecran ou une demo live du prototype. Si demo live impossible, montrer 2-3 captures d'ecran annotees.</td>
		<td>
			<ul>
				<li>Bouton Scan : appui tactile → la camera se lance</li>
				<li>Commande vocale : dire "scan" → meme resultat, sans toucher l'ecran</li>
				<li>Settings : changement d'ecran vers les reglages (volume, vitesse vocale)</li>
				<li>Describe (V1) : l'IA decrira la scene capturee → prochaine etape</li>
			</ul>
		</td>
		<td>On va vous montrer le prototype en quatre etapes. D'abord, on appuie sur le bouton Scan : la camera se lance. Ensuite, on fait la meme chose par la voix : on dit "scan" et ca marche sans toucher l'ecran. Puis on appuie sur Settings : on change d'ecran et on peut regler le volume et la vitesse de la voix. Derniere etape, le bouton Describe : pour l'instant il est en place mais l'IA n'est pas encore branchee. C'est la prochaine priorite en V1.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 180" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="160" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<text x="410" y="36" text-anchor="middle" font-size="18" fill="#173b36" font-family="Segoe UI">Etapes de la demo</text>
	<!-- Fleche horizontale -->
	<path d="M60 100 H760" stroke="#8a9e98" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
	<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#8a9e98"/></marker></defs>
	<!-- Etape 1 : Bouton -->
	<circle cx="140" cy="100" r="18" fill="#4e8c82"/>
	<text x="140" y="105" text-anchor="middle" font-size="13" fill="#fff" font-family="Segoe UI" font-weight="bold">1</text>
	<text x="140" y="75" text-anchor="middle" font-size="12" fill="#4e8c82" font-family="Segoe UI">Bouton Scan</text>
	<text x="140" y="138" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Appui tactile →</text>
	<text x="140" y="152" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">camera se lance</text>
	<!-- Etape 2 : Commande vocale -->
	<circle cx="290" cy="100" r="18" fill="#4e8c82"/>
	<text x="290" y="105" text-anchor="middle" font-size="13" fill="#fff" font-family="Segoe UI" font-weight="bold">2</text>
	<text x="290" y="75" text-anchor="middle" font-size="12" fill="#4e8c82" font-family="Segoe UI">Commande vocale</text>
	<text x="290" y="138" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Dire "scan" →</text>
	<text x="290" y="152" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">sans toucher l'ecran</text>
	<!-- Etape 3 : Settings -->
	<circle cx="480" cy="100" r="18" fill="#4e8c82"/>
	<text x="480" y="105" text-anchor="middle" font-size="13" fill="#fff" font-family="Segoe UI" font-weight="bold">3</text>
	<text x="480" y="75" text-anchor="middle" font-size="12" fill="#4e8c82" font-family="Segoe UI">Settings</text>
	<text x="480" y="138" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">Changement d'ecran</text>
	<text x="480" y="152" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">volume, vitesse vocale</text>
	<!-- Etape 4 : Describe (V1) -->
	<circle cx="670" cy="100" r="18" fill="#a88723" stroke="#a88723" stroke-dasharray="4,3"/>
	<text x="670" y="105" text-anchor="middle" font-size="13" fill="#fff" font-family="Segoe UI" font-weight="bold">4</text>
	<text x="670" y="75" text-anchor="middle" font-size="12" fill="#a88723" font-family="Segoe UI">Describe (V1)</text>
	<text x="670" y="138" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">IA decrit la scene</text>
	<text x="670" y="152" text-anchor="middle" font-size="10" fill="#5a6d68" font-family="Segoe UI">→ prochaine etape</text>
</svg>
</div>

Elements a faire apparaitre :

- frise en 4 etapes : bouton tactile, commande vocale, settings, Describe (V1)
- montrer les deux modes d'interaction (tactile et vocal)
- montrer le changement d'ecran vers les reglages
- Describe en pointille pour indiquer que c'est la suite

Objectif du visuel : prouver au jury que le V0 fonctionne concretement, en montrant le deroulement de la demo.

---

# BLOC 3 — PLANNING RECTIFIE (2 minutes)

---

## Slide 8 - Estimation de l'effort realise

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Tableau clair avec une ligne par semaine et les taches realisees. Progression visible semaine par semaine.</td>
		<td>
			<table>
				<tr><th>Semaine</th><th>Taches realisees</th><th>Charge estimee</th></tr>
				<tr><td>Semaine 1 — Etudes</td><td>Architecture, choix technos, debut interface (layout, ecrans, boutons)</td><td>Architecture 2h (2 pers.), Interface 3h (2 pers.), Mise en place GitHub 2h (1 pers.)</td></tr>
				<tr><td>Semaine 2 — Code</td><td>Module camera, synthese vocale, commandes vocales</td><td>Camera 2h (1 pers.), TTS 2h (2 pers.), STT 2h (1 pers.), Integration 1h (1 pers.)</td></tr>
				<tr><td>Semaine 3 — Integration</td><td>Integration des modules, ecran reglages, tests, documentation</td><td>Integration 2h (2 pers.), Reglages 1h (1 pers.), Tests 2h (3 pers.), Docs 2h (2 pers.)</td></tr>
			</table>
		</td>
		<td>Voici comment on a reparti le travail entre les cinq membres de l'equipe. La premiere semaine etait consacree aux etudes : architecture, choix des technologies, deux personnes sur l'architecture, deux sur l'interface et une sur la mise en place du depot GitHub. La deuxieme semaine etait du code : une personne sur la camera, deux sur la synthese vocale, une sur les commandes vocales et une sur l'integration. La troisieme semaine etait dediee a l'integration : deux personnes pour assembler les modules, une sur les reglages, trois sur les tests et deux sur la documentation. Certains ont travaille sur plusieurs taches dans la meme semaine.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<table>
<tr>
<th style="background:#4e8c82;color:#fff" colspan="4">Semaine 1 — Etudes</th>
</tr>
<tr><th>Tache</th><th>Heures</th><th>Personnes</th><th>Homme-heures</th></tr>
<tr><td>Reunion de lancement (repartition du travail)</td><td>2h</td><td>5</td><td>10h</td></tr>
<tr><td>Architecture</td><td>3h</td><td>2</td><td>6h</td></tr>
<tr><td>Interface (layout, ecrans, boutons)</td><td>3h</td><td>2</td><td>6h</td></tr>
<tr><td>Mise en place GitHub</td><td>2h</td><td>1</td><td>2h</td></tr>
<tr><td align="right"><strong>Sous-total</strong></td><td><strong>10h</strong></td><td></td><td><strong>24h</strong></td></tr>
</table>

<table>
<tr>
<th style="background:#a88723;color:#fff" colspan="4">Semaine 2 — Code</th>
</tr>
<tr><th>Tache</th><th>Heures</th><th>Personnes</th><th>Homme-heures</th></tr>
<tr><td>Camera</td><td>6h</td><td>1</td><td>6h</td></tr>
<tr><td>TTS (synthese vocale)</td><td>6h</td><td>2</td><td>12h</td></tr>
<tr><td>STT (commandes vocales)</td><td>6h</td><td>1</td><td>6h</td></tr>
<tr><td>Ecrans GUI (principal + reglages)</td><td>6h</td><td>2</td><td>12h</td></tr>
<tr><td align="right"><strong>Sous-total</strong></td><td><strong>24h</strong></td><td></td><td><strong>36h</strong></td></tr>
</table>

<table>
<tr>
<th style="background:#b56b6b;color:#fff" colspan="4">Semaine 3 — Integration</th>
</tr>
<tr><th>Tache</th><th>Heures</th><th>Personnes</th><th>Homme-heures</th></tr>
<tr><td>Integration des modules</td><td>7h</td><td>2</td><td>14h</td></tr>
<tr><td>Ecran reglages</td><td>2h</td><td>1</td><td>2h</td></tr>
<tr><td>Tests et debug</td><td>2h</td><td>3</td><td>6h</td></tr>
<tr><td>Documentation</td><td>7h</td><td>3</td><td>21h</td></tr>
<tr><td align="right"><strong>Sous-total</strong></td><td><strong>18h</strong></td><td></td><td><strong>43h</strong></td></tr>
</table>

> **Total V0 : 3 semaines — 103 homme-heures cumulees (equipe de 5)**

Elements a faire apparaitre :

- trois tableaux colores, un par semaine (vert etudes, jaune code, rouge integration)
- colonnes : tache, heures, personnes, homme-heures
- sous-total par semaine + total global en bas
- lecture rapide de la charge et de la repartition

Objectif du visuel : montrer une repartition detaillee et chiffree de l'effort V0.

---

## Slide 9 - Synthese et prochaines priorites

<table>
	<tr>
		<th width="28%">Structure visuelle du slide</th>
		<th width="28%">Texte affiche sur le slide</th>
		<th width="44%">Texte a dire a l'oral</th>
	</tr>
	<tr>
		<td>Slide de conclusion sobre avec 3 points cles et un message de cloture.</td>
		<td>
			<ul>
				<li>V0 valide : le socle technique et l'experience utilisateur de base sont operationnels</li>
				<li>Prochaine priorite : integration de l'IA de description de scene (V1)</li>
				<li>A traiter ensuite : accessibilite native (TalkBack/VoiceOver) et tests utilisateurs</li>
				<li>Objectif : V1 livrable en juin pour la soutenance</li>
			</ul>
		</td>
		<td>Pour conclure, le V0 fonctionne : l'interface, la camera, la voix et les commandes sont en place. Prochaine etape : brancher l'IA pour que le bouton Describe donne un vrai resultat. Ensuite, accessibilite et tests utilisateurs. L'objectif est d'avoir une version stable pour la soutenance de juin. Merci, on est disponibles pour vos questions.</td>
	</tr>
</table>

### Schema Excalidraw a integrer

<div align="center">
<svg viewBox="0 0 820 230" width="100%" xmlns="http://www.w3.org/2000/svg">
	<rect x="10" y="10" width="800" height="210" rx="22" fill="#f8f6ef" stroke="#d7d1c2"/>
	<path d="M90 120 H730" stroke="#8a9e98" stroke-width="4" stroke-linecap="round"/>
	<circle cx="170" cy="120" r="22" fill="#4e8c82"/>
	<circle cx="410" cy="120" r="22" fill="#a88723"/>
	<circle cx="650" cy="120" r="22" fill="#173b36"/>
	<text x="170" y="126" text-anchor="middle" font-size="14" fill="#fff" font-family="Segoe UI">V0</text>
	<text x="410" y="126" text-anchor="middle" font-size="14" fill="#fff" font-family="Segoe UI">V1</text>
	<text x="650" y="126" text-anchor="middle" font-size="11" fill="#fff" font-family="Segoe UI">Soutenance</text>
	<text x="170" y="84" text-anchor="middle" font-size="16" fill="#4e8c82" font-family="Segoe UI" font-weight="bold">✓ Valide</text>
	<text x="410" y="84" text-anchor="middle" font-size="16" fill="#a88723" font-family="Segoe UI" font-weight="bold">A venir</text>
	<text x="650" y="84" text-anchor="middle" font-size="16" fill="#173b36" font-family="Segoe UI" font-weight="bold">Juin 2026</text>
	<text x="170" y="156" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Interface + Camera + Voix</text>
	<text x="170" y="172" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Avril 2026</text>
	<text x="410" y="156" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">IA description de scene</text>
	<text x="410" y="172" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Accessibilite (TalkBack)</text>
	<text x="410" y="188" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Tests utilisateurs — Mai 2026</text>
	<text x="650" y="156" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Rapport + Soutenance</text>
	<text x="650" y="172" text-anchor="middle" font-size="11" fill="#5a6d68" font-family="Segoe UI">Juin 2026</text>
</svg>
</div>

Elements a faire apparaitre :

- frise simple en 3 jalons : V0 (valide), V1 (a venir), Soutenance (juin)
- V0 coche comme valide
- V1 avec dates et fonctionnalites (IA, accessibilite, tests)
- message de cloture sobre

Objectif du visuel : terminer sur une note claire et confiante.

---

## Notes de presentation

### Structure de la presentation (rappel consignes jury)

- **1 minute** : Slide 1 — contexte, probleme vise, produit attendu, perimetre V0
- **7 minutes** : Slides 2 a 7 — avancement concret, demo du prototype
- **2 minutes** : Slides 8 a 9 — estimation effort, synthese et prochaines priorites

### Ton recommande

- rester honnete sur l'etat d'avancement
- bien distinguer prototype V0 et cible finale
- montrer que les choix actuels sont volontaires et justifies
- justifier l'effort investi (3 reunions de 7h)

### Conseils

- ajouter une capture d'ecran du prototype si possible (slide 3)
- ne pas surcharger les slides en texte
- garder une idee principale par slide
- insister sur les limites de maniere maitrisee, puis enchainer avec le planning
- le planning semaine par semaine (slide 7) est le point le plus attendu par le jury

### A preparer en complement

- capture d'ecran du prototype en fonctionnement
- demo live si possible (30 secondes)
- compte-rendu de cette reunion a rediger apres la presentation

---

## Version courte du fil narratif

Nous avons un projet avec un enjeu fort d'accessibilite.
Le prototype V0 valide les bases essentielles : interface accessible, camera, guidage vocal, commandes vocales et structure technique modulaire.
L'effort correspond aux trois reunions de sept heures prevues.
Les prochaines etapes sont l'integration de l'IA, l'amelioration de l'accessibilite native, les tests utilisateurs, puis la preparation de la soutenance en juin.
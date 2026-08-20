# Guide de vérification pour un tiers

## À quoi sert cet outil ?

ProovIT Verify permet à une personne extérieure à ProovIT de contrôler une archive de preuve avec un logiciel open source et, lorsque cela est possible, avec les données publiques de la blockchain.

Le contrôle ne repose donc pas uniquement sur une page Web ou sur une affirmation de ProovIT. Le tiers reçoit une archive, son code d’accès et le vérificateur ; il peut reproduire les calculs localement.

## Ce que le contrôle établit techniquement

Le vérificateur peut établir notamment :

- que l’archive est lisible avec le code fourni ;
- que les fichiers présents correspondent à l’inventaire et à leurs empreintes SHA-256 ;
- que le manifeste est canonique selon les règles publiées ;
- que la signature Ed25519 correspond à une clé publique publiée ;
- que la timeline Web est cohérente lorsqu’elle est présente ;
- que la transaction globale et les transactions de fichiers sont retrouvées et décodées lorsque leurs informations sont présentes ;
- que les valeurs publiques blockchain correspondent aux valeurs de l’archive.

## Ce que le contrôle ne décide pas

L’outil ne décide pas de la recevabilité, de la force probante, de l’imputabilité d’un fait ou de la qualification juridique d’un contenu. Ces appréciations relèvent des professionnels et des autorités compétentes, avec le contexte du dossier, la chaîne de conservation et les autres éléments disponibles.

## Procédure recommandée

1. Conserver l’archive originale sans la modifier.
2. Conserver séparément le code d’accès et la version du vérificateur utilisée.
3. Télécharger le vérificateur depuis la page officielle des releases GitHub.
4. Exécuter le contrôle et conserver la sortie texte ou JSON.
5. En cas de résultat `!`, lire le détail et distinguer une différence historique d’un échec d’intégrité.
6. Conserver les fichiers, la sortie du contrôle, la date du contrôle et l’environnement utilisé.

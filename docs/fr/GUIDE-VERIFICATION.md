# Guide de vérification pour un tiers

**Public :** avocats, commissaires de justice, experts, magistrats, assureurs, DSI et toute personne chargée d’examiner une archive.

## Objet du contrôle

ProovIT Verify permet à une personne extérieure à ProovIT de contrôler une archive de preuve avec un logiciel open source et, lorsque cela est possible, avec les données publiques de la blockchain.

Le contrôle ne repose donc pas uniquement sur une page Web ou sur une affirmation de ProovIT. Le tiers reçoit une archive, son code d’accès et le vérificateur ; il peut reproduire les calculs localement.

## Préparer l’archive

Conserver le ZIP original, le code d’accès et la version téléchargée depuis la page officielle des releases. Si l’archive est chiffrée en AES-256, utiliser un outil compatible lorsque l’explorateur Windows ne permet pas son ouverture.

## Lancer le vérificateur

```bash
proovit-verify archive.zip --password 'CODE_D_ACCES'
proovit-verify archive.zip --password 'CODE_D_ACCES' --json > rapport.json
```

## Contrôles hors ligne

Le vérificateur peut établir notamment :

- que l’archive est lisible avec le code fourni ;
- que les fichiers présents correspondent à l’inventaire et à leurs empreintes SHA-256 ;
- que le manifeste est canonique selon les règles publiées ;
- que la signature Ed25519 correspond à une clé publique publiée ;
- que la timeline Web est cohérente lorsqu’elle est présente ;
- que la transaction globale et les transactions de fichiers sont retrouvées et décodées lorsque leurs informations sont présentes ;
- que les valeurs publiques blockchain correspondent aux valeurs de l’archive.

Les contrôles hors ligne portent sur la lisibilité, l’inventaire, les SHA-256, le manifest canonique, la signature Ed25519 et la chronologie Web lorsqu’elle est présente.

## Contrôles en ligne

Lorsque le manifest fournit un RPC public, l’outil peut retrouver le reçu blockchain, décoder `ProofStoredV3` et interroger séparément les transactions `FileAddedV3`. Une référence enregistrée sans RPC est présentée comme enregistrée, non comme contrôlée.

## Lire le résultat

| Résultat | Signification |
|---|---|
| `✓` / `PASS` | Le contrôle a été exécuté et les valeurs correspondent. |
| `✗` / `FAIL` | Le contrôle a été exécuté et une différence a été détectée. |
| `ℹ` / `INFO` | L’information est absente, non disponible ou non applicable. |
| `!` / `WARN` | Le contrôle fournit une observation à examiner, souvent liée au contexte ou à la compatibilité. |

Une timeline absente peut être normale pour une preuve multimédia. Lorsque les fichiers sont ajoutés par des transactions séparées, le rapport utilise ces transactions individuelles comme référence pour le décompte vérifié.

## Périmètre de l’appréciation

L’outil ne statue pas sur la recevabilité, la force probante, l’imputabilité d’un fait ou la qualification juridique d’un contenu. Ces appréciations relèvent des professionnels et des autorités compétentes, avec le contexte du dossier, la chaîne de conservation et les autres éléments disponibles.

## Procédure recommandée

1. Conserver l’archive originale sans la modifier.
2. Conserver séparément le code d’accès et la version du vérificateur utilisée.

3. Télécharger le vérificateur depuis la page officielle des releases GitHub.
4. Exécuter le contrôle et conserver la sortie texte ou JSON.
5. En cas de résultat `!`, lire le détail et distinguer une observation de contexte d’un échec d’intégrité.
6. Pour la blockchain, conserver le RPC utilisé et distinguer un contrôle réalisé d’une référence enregistrée.
7. Conserver les fichiers, la sortie du contrôle, la date du contrôle et l’environnement utilisé.

## Pour aller plus loin

Voir [Comprendre une preuve](COMPRENDRE-UNE-PREUVE.md), [Interpréter un rapport](INTERPRETER-UN-RAPPORT.md) et l’[architecture de vérification](../expert/ARCHITECTURE-DE-VERIFICATION.md).

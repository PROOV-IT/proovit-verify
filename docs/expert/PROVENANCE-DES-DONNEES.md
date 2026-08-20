# Provenance des données

**Public :** experts numériques, analystes forensiques, DSI et RSSI.

Chaque catégorie doit être lue selon son origine :

- **Contrôle cryptographique indépendant** : empreintes de fichiers, manifeste canonique, signature, chaîne de timeline et racines de fichiers.
- **Observation technique enregistrée** : navigateur, environnement d’exécution, réponse reçue, date serveur et paramètres de capture.
- **Déclaration ou contexte d’acquisition** : identité de compte, coordonnées fournies par le terminal, identifiants d’appareil et informations déclaratives.
- **Attestation externe** : reçu blockchain, jeton RFC3161 ou stockage immuable lorsqu’il est fourni par un système externe.

Une provenance décrit l’origine d’une valeur ; elle ne modifie pas le résultat du contrôle cryptographique.

| Donnée | Origine typique | Persistance | Intégrité | Contrôle tiers |
|---|---|---|---|---|
| URL demandée | `DECLARED_BY_USER` / `OBSERVED_BY_BROWSER` | Manifest et contexte | Manifest signé | Lecture et comparaison |
| URL finale | `OBSERVED_BY_BROWSER` | Manifest Web | Manifest et timeline | Lecture ; pas de rejeu distant |
| HTML, DOM, capture | `OBSERVED_BY_BROWSER` / `OBSERVED_BY_RUNNER` | Archive | SHA-256 et inventaire | Recalcul local |
| Géolocalisation | Environnement client | Contexte d’acquisition | Manifest signé | Présence et cohérence de forme |
| Date serveur | `OBSERVED_BY_BACKEND` | Manifest | Signature, éventuellement timestamp | Recalcul de signature |
| Empreinte fichier | `DERIVED_BY_PROOVIT` | Manifest et blockchain éventuelle | SHA-256, `metaHash` | Recalcul local et comparaison |
| Signature du manifest | `DERIVED_BY_PROOVIT` | Manifest | Ed25519 | Vérification avec registre public |
| Reçu blockchain | `EXTERNAL_ATTESTATION` | Référence et rapport | Réseau public | Interrogation RPC |

# Interpréter un rapport de vérification

**Public :** professionnels du droit, experts et responsables de conservation.

## Les statuts à distinguer

- **Enregistré** : la valeur figure dans l’archive ou dans un reçu.
- **Présent** : l’élément est disponible pour le contrôle.
- **Vérifié** : le calcul ou la comparaison a été réalisé avec succès.
- **Non disponible / non applicable** : la donnée n’est pas exploitable pour ce contrôle ou le contrôle ne concerne pas ce type de preuve.

Dans la sortie du programme, ces notions apparaissent notamment sous les
formes `PRESENT`, `RECORDED`, `VERIFIED`, `NOT_AVAILABLE`, `NOT_APPLICABLE`,
`INFO`, `WARN` et `FAIL` selon la version du rapport.

## Lire les contrôles

| Information | Statut attendu | Signification |
|---|---|---|
| Archive lisible, inventaire et fichiers | `VERIFIED` | Les entrées reçues sont lisibles et leurs empreintes correspondent. |
| Manifest et empreinte canonique | `VERIFIED` | Le manifest a été normalisé et son empreinte recalculée. |
| Signature Ed25519 | `VERIFIED` | La signature correspond à une clé publique publiée. |
| Timeline Web | `VERIFIED` ou `NOT_APPLICABLE` | La continuité est contrôlée lorsqu'une timeline est fournie. |
| Reçu blockchain et identifiants | `VERIFIED` ou `NOT_AVAILABLE` | Le reçu et les champs publics sont comparés si le RPC est accessible. |
| Fichiers blockchain séparés | `VERIFIED` | Chaque transaction `FileAddedV3` référencée a été vérifiée. |
| Géolocalisation, terminal, contexte d'acquisition | `RECORDED` | La valeur est enregistrée dans l'archive ; cela ne constitue pas une observation indépendante. |
| Horodatage | `RECORDED` ou `VERIFIED` | Le rapport précise le mécanisme et son niveau exact, notamment RFC3161 non qualifié. |
| Élément absent du format concerné | `NOT_APPLICABLE` | Le contrôle ne concerne pas ce type de preuve. |
| Échec d'une comparaison | `FAIL` | Une incohérence technique doit être analysée avant toute utilisation du résultat. |

Un statut `PRESENT` indique seulement que l'élément est disponible. Un statut
`RECORDED` indique qu'il est déclaré ou conservé dans l'archive. Seul
`VERIFIED` signifie que le contrôle correspondant a effectivement réussi.

## Principales rubriques

- **Archive et fichiers** : lisibilité, inventaire et empreintes.
- **Manifeste** : canonicalisation, empreinte et signature.
- **Timeline Web** : continuité et hash de chaque événement, lorsqu’une timeline est fournie.
- **Blockchain** : reçu, réseau, contrat, identifiant de preuve et valeurs publiques.
- **Contexte** : géolocalisation, terminal, horodatage et autres informations enregistrées.

Un résultat positif signifie que le contrôle correspondant est cohérent. Il ne transforme pas une donnée de contexte en observation indépendante et ne constitue pas, à lui seul, une conclusion juridique.

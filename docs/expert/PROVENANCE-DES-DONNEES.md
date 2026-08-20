# Provenance des données

**Public :** experts judiciaires, experts numériques, analystes forensiques,
RSSI et auditeurs.

La provenance décrit l'origine annoncée d'une valeur et le moment où elle a
été produite. Elle ne constitue pas, par elle-même, une preuve d'exactitude.
Les niveaux utilisés dans les archives sont : `DECLARED_BY_USER`,
`OBSERVED_BY_CLIENT`, `OBSERVED_BY_BROWSER`, `OBSERVED_BY_RUNNER`,
`OBSERVED_BY_BACKEND`, `DERIVED_BY_PROOVIT`, `EXTERNAL_ATTESTATION` et
`INDEPENDENTLY_RECALCULABLE`.

Les colonnes « signé » et « ancré » décrivent une couverture ou une attestation
éventuelle ; elles ne signifient pas que la valeur a été observée
indépendamment. Le vérificateur distingue toujours `RECORDED`,
`INTEGRITY_PROTECTED`, `SIGNED`, `ANCHORED` et `VERIFIED`.

| Élément | Type de preuve | Origine | Producteur | Moment d'acquisition | Protection d'intégrité | Inclus dans un manifest | Signé | Ancré | Vérification possible | Mode de vérification |
|---|---|---|---|---|---|---:|---:|---:|---|---|
| Identifiant de preuve | contexte | backend | backend | création | manifest/signature | oui | oui | référence possible | oui | lecture et comparaison |
| Date de création | contexte | backend | backend | création/réception | manifest/timeline | oui | oui | timestamp possible | selon mécanisme | examiner le mécanisme déclaré |
| Fichier original | contenu | client ou utilisateur | client/backend | import ou capture | SHA-256, inventaire | oui | indirectement | `metaHash` possible | oui | recalcul local |
| SHA-256 original | dérivée | traitement PROOV-IT | backend | réception | manifest | oui | oui | `dataHash`/`filesRoot` possible | oui | recalcul sur les octets |
| Artefact dérivé | contenu dérivé | traitement PROOV-IT | backend | génération | SHA-256, inventaire | oui | indirectement | possible | oui | recalcul et relation original/dérivé |
| Type MIME, taille, dimensions, durée, codecs | métadonnées | client/backend | producteur indiqué | capture ou traitement | manifest, hash de fichier | oui | indirectement | éventuel | partiellement | lecture et cohérence avec le fichier |
| Manifest | structure | backend | backend | finalisation | empreinte canonique | oui | oui | `dataHash` possible | oui | canonicalisation puis SHA-256 |
| Empreinte du manifest | dérivée | traitement PROOV-IT | backend | finalisation | chaîne de calcul | oui | couverte par signature | possible | oui | recalcul canonique |
| Signature Ed25519 | signature | backend | clé identifiée | finalisation | Ed25519 | oui | n/a | n/a | oui | clé publique et message signé |
| Archive manifest / inventaire ZIP | structure | backend | backend | export | hashes et signature du manifest | oui | oui | indirectement | oui | lecture, chemins et hashes |
| Transaction blockchain | attestation externe | réseau public | contrat/réseau | ancrage | reçu et événements | référence | n/a | oui | si RPC accessible | reçu, événement et champs |
| Bloc blockchain | attestation externe | réseau public | réseau | confirmation | hash de bloc/référence | référence éventuelle | n/a | oui | si RPC accessible | interrogation du réseau |
| Image metadata / EXIF | observation ou métadonnée | fichier/client | producteur indiqué | capture/import | hash du fichier | si présent | indirectement | éventuel | présence et cohérence | ne pas traiter comme observation indépendante |
| Géolocalisation / device context | contexte | client | environnement client | capture | manifest si présent | oui si fournie | oui indirectement | éventuel | forme et présence | comparer aux autres éléments |
| Capture d'écran / contexte écran | observation | client/browser/runner | producteur indiqué | capture | SHA-256 et inventaire | oui si fournie | indirectement | éventuel | oui pour les octets | recalcul du fichier |
| URL demandée | observation/contexte | utilisateur/browser | producteur indiqué | navigation | manifest/timeline | oui si fournie | oui | éventuel | oui | lecture et comparaison |
| URL finale et redirects | observation navigateur | browser/runner | runner | navigation | manifest/timeline | oui si fournie | oui | éventuel | oui | lire l'ordre enregistré |
| HTML / DOM | artefact Web | browser/runner | runner | capture | SHA-256 et inventaire | oui si fourni | indirectement | éventuel | oui pour les octets | recalcul local, sans rejeu |
| HTTP status / headers | observation | runner | runner | réponse | manifest/timeline | oui si fourni | oui | éventuel | oui comme enregistrement | comparaison du contenu enregistré |
| DNS / TLS | observation | runner | runner | requête | manifest/timeline | oui si fourni | oui | éventuel | oui comme enregistrement | pas de nouvelle résolution implicite |
| Ressources téléchargées | artefact/référence | browser/runner | runner | navigation | hashes et inventaire | oui si fourni | indirectement | éventuel | oui pour les fichiers | recalcul et liens |
| Download | fichier | browser/runner | runner | navigation | SHA-256, manifest, `metaHash` possible | oui si fourni | indirectement | possible | oui | identité, taille et hash |
| Timeline | structure temporelle | runner/backend | producteur indiqué | événements | hash chain | oui si fournie | manifest | root possible | oui | séquence, précédent, dernier hash |
| Browser/runner runtime | contexte | runner | runner | acquisition | manifest/timeline si fourni | oui si fourni | oui indirectement | non en soi | enregistré seulement | lecture, pas d'attestation indépendante |
| Horodatage serveur | observation backend | backend | backend | réception/finalisation | manifest/signature | oui si fourni | oui | possible | selon mécanisme | distinguer enregistré et qualifié |
| Horodatage RFC3161 | attestation externe | autorité de temps | service externe | émission du jeton | signature du jeton | si fourni | oui par le jeton | externe | oui si jeton accessible | vérifier le jeton et son statut |
| `evidence_root_hash` | dérivée | traitement PROOV-IT | backend | finalisation | SHA-256 et manifest | oui si fourni | oui | possible | oui | recalcul de l'objet canonique |
| Object Lock / WORM | attestation externe | stockage | service de stockage | conservation | attestation du service | seulement si représenté | selon service | externe | seulement si référence présente | vérifier la preuve de conservation |

## Lecture par un tiers

Une donnée peut être enregistrée, couverte par une empreinte, incluse dans une
signature et finalement vérifiée sans que son origine devienne indépendante.
Par exemple, le vérificateur peut recalculer le SHA-256 d'une géolocalisation
présente dans un manifest, mais cela vérifie l'intégrité de la valeur enregistrée,
pas la position réelle du terminal.

La vérification indépendante porte donc sur les octets, les relations de
manifest, les signatures, les chaînes de timeline et les engagements publics
effectivement accessibles. L'appréciation de l'acquisition, de la conservation
et du contexte relève du dossier complet.

# Comprendre une preuve PROOV-IT

**Public :** utilisateurs, avocats, commissaires de justice, magistrats, assureurs et décideurs.

## Objet d’une preuve PROOV-IT

Une preuve PROOV-IT rassemble un ou plusieurs éléments numériques et les informations techniques qui permettent d’en contrôler l’intégrité et la traçabilité. L’archive portable est conçue pour être transmise, conservée et examinée indépendamment de l’interface d’origine.

```text
capture ou import → réception → empreinte → manifest → ancrage
      → archive portable → vérification indépendante
```

## Éléments constituant une preuve

Selon le type de dépôt, l’archive peut contenir le fichier d’origine, des versions de preuve ou artefacts dérivés, un certificat PDF, un inventaire ZIP, un manifest signé, des informations de contexte et des références blockchain.

## Fichier d’origine et version de preuve

Le fichier d’origine est la représentation utilisateur contrôlée par son empreinte. Une version de preuve, une miniature ou un certificat est un artefact dérivé ; il est identifié séparément et ne remplace pas l’original.

## Empreinte cryptographique SHA-256

Une empreinte SHA-256 est calculée sur les octets d’un fichier. Modifier un seul octet produit normalement une empreinte différente. Le vérificateur recalcule cette valeur à partir de l’archive reçue.

## Manifest de preuve

Le manifest décrit les fichiers, leurs rôles, les empreintes, le contexte, l’horodatage et les références publiques. Sa forme canonique permet à plusieurs implémentations de produire le même résultat.

## Signature du manifest

La signature Ed25519 permet de vérifier que le manifest correspond à une clé publique publiée dans le registre du vérificateur. Elle protège la correspondance entre le manifest et sa signature ; elle ne transforme pas toutes les données de contexte en observations indépendantes.

## Horodatage

L’archive peut associer une date serveur, un jeton RFC3161 ou une autre référence temporelle. Le rapport indique le mécanisme et son statut exact. Un horodatage identifié comme non qualifié ne doit pas être présenté comme un horodatage qualifié.

## Ancrage blockchain

Le CID peut désigner une représentation chiffrée stockée sur IPFS. Il ne doit donc pas être confondu avec l’empreinte ou la taille du fichier utilisateur en clair.

## Données de contexte

L’archive peut contenir une date serveur, un jeton RFC3161, une géolocalisation, des informations de terminal ou une chronologie Web. Chaque donnée doit être interprétée selon son origine : donnée déclarée, observation technique, donnée dérivée ou attestation externe.

## Vérification indépendante

Le contrôle peut être effectué hors de l’infrastructure PROOV-IT à partir de l’archive, du code d’accès et du vérificateur. Il établit l’intégrité et la cohérence des éléments contrôlables ; il ne remplace pas l’examen du contexte d’acquisition, de la conservation et de la transmission.

## Preuves multimédia

Les images, vidéos, audios et documents sont contrôlés comme des fichiers. Les métadonnées, aperçus et transformations sont des éléments associés dont l’origine doit être lue dans le manifest.

## Preuves Web

Une preuve Web peut contenir une URL demandée, une URL finale, des captures, des ressources, un DOM, des informations de navigateur et une chronologie d’événements. La chronologie est contrôlée lorsqu’elle est présente ; le vérificateur ne rejoue pas automatiquement le site distant.

## Lecture dans le contexte d’un dossier

La vérification porte sur l’intégrité, la cohérence et les attestations techniques associées à la preuve. Son appréciation dans un dossier s’effectue au regard de son contexte et des autres éléments disponibles.

## Pour aller plus loin

Voir le [guide de vérification](GUIDE-VERIFICATION.md), l’[interprétation d’un rapport](INTERPRETER-UN-RAPPORT.md) et le [modèle de confiance expert](../expert/MODELE-DE-CONFIANCE.md).

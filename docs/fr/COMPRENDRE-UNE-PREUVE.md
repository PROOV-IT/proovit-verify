# Comprendre une preuve PROOV-IT

**Public :** utilisateurs, avocats, commissaires de justice, magistrats, assureurs et décideurs.

## Qu’est-ce qui est vérifié ?

Une archive PROOV-IT rassemble des fichiers, un inventaire, un manifeste et des informations de contexte. Le vérificateur recalcule les empreintes des éléments reçus et compare les résultats aux valeurs enregistrées.

## Empreintes et manifeste

Une empreinte SHA-256 représente le contenu d’un fichier à un instant donné. Le manifeste décrit les fichiers, leur rôle, leurs empreintes et les références de vérification. Sa forme canonique permet à un tiers de refaire exactement le calcul.

## Signature et blockchain

La signature Ed25519 permet de vérifier que le manifeste correspond à une clé publique publiée. L’ancrage blockchain ajoute une attestation publique : le vérificateur peut retrouver un reçu et comparer les valeurs décodées avec l’archive.

Le CID peut désigner une représentation chiffrée stockée sur IPFS. Il ne doit donc pas être confondu avec l’empreinte ou la taille du fichier utilisateur en clair.

## Horodatage et contexte

L’archive peut contenir une date serveur, un jeton RFC3161, une géolocalisation, des informations de terminal ou une chronologie Web. Chaque donnée doit être interprétée selon son origine : donnée déclarée, observation technique, donnée dérivée ou attestation externe.

## Vérification indépendante

Le contrôle peut être effectué hors de l’infrastructure PROOV-IT à partir de l’archive, du code d’accès et du vérificateur. Il établit l’intégrité et la cohérence des éléments contrôlables ; il ne remplace pas l’examen du contexte d’acquisition, de la conservation et de la transmission.

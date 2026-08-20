# Archive portable et `archive_manifest_v1`

L’archive ZIP portable regroupe les fichiers de preuve, les documents techniques et les métadonnées nécessaires à un contrôle indépendant.

`archive_manifest_v1` inventorie les entrées contrôlables. Pour chaque entrée, il peut fournir son chemin, son rôle, son identifiant de fichier, sa taille et son SHA-256. Le vérificateur relit l’entrée dans le ZIP, recalcule son SHA-256 et compare le résultat à l’inventaire.

Cette étape contrôle l’archive reçue. Elle ne prétend pas prouver, à elle seule, l’origine du contenu avant son dépôt.

Les archives sont chiffrées avec un code d’accès. Le code ne sert pas de signature : il permet de lire les données ; l’authenticité du manifeste repose sur la signature Ed25519.

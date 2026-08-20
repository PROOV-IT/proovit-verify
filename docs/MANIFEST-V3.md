# Manifeste de certification V3

Le manifeste `proovit.manifest.v3` décrit le contexte de la preuve, les fichiers, les empreintes, la signature, l’horodatage et les références blockchain.

## Canonicalisation et signature

Le hash canonique est calculé sur une représentation JSON UTF-8 compacte, triée par clés, avec les champs de hash et de signature neutralisés selon le protocole du dépôt. La valeur hexadécimale SHA-256 obtenue est signée avec Ed25519. La clé publique est sélectionnée par `signing_key_id` dans le registre public du vérificateur.

## Blockchain publique

Les versions récentes peuvent inclure : `chain_id`, `contract_address`, `proof_chain_id`, `transaction_hash`, `data_hash`, `files_root`, `file_count` et `file_transactions`. Les transactions de fichiers décrivent notamment le `file_id`, le hash de fichier, le CID et la taille déclarée.

La taille déclarée par le protocole récent correspond au fichier utilisateur en clair (`size_basis: plaintext_user_file`). Le CID peut identifier une représentation chiffrée stockée sur IPFS ; il n’a donc pas vocation à être égal au SHA-256 du fichier en clair.

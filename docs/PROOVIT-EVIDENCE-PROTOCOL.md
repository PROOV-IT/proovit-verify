# Protocole public ProovIT Evidence

Le protocole décrit la relation vérifiable entre une archive ProovIT, ses fichiers, ses manifestes, sa signature et son ancrage blockchain.

1. `archive_manifest_v1` inventorie les entrées de l’archive et leurs SHA-256.
2. Le manifeste de certification est canonique et signé avec Ed25519.
3. Les preuves Web peuvent ajouter une timeline chaînée par hash et un `evidence_root_hash`.
4. L’ancrage `storeProofV3` publie notamment `proofId`, `dataHash`, `filesRoot` et `fileCount` dans l’événement `ProofStoredV3`.
5. `proovit-verify` recalcule les contrôles locaux puis interroge directement le RPC indiqué par l’archive ou fourni par l’utilisateur.

Le logiciel ne déduit pas la recevabilité juridique : il établit des faits techniques reproductibles à partir de l’archive et de données publiques.

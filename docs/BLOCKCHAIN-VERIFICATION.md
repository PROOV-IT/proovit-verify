# Vérification blockchain ProovIT

Une archive portable peut contenir l’identifiant de transaction et les paramètres publics de l’ancrage. Lorsque le RPC est accessible, `proovit-verify` récupère le reçu et recherche l’événement `ProofStoredV3` du contrat ProovStore.

Le vérificateur décode les champs publics de cet événement : `proofId`, `dataHash`, `filesRoot` et `fileCount`. Il les compare aux valeurs présentes dans le snapshot blockchain ou le manifeste de l’archive.

Le calcul de `filesRoot` utilisé par le backend est un arbre binaire Keccak-256 : les feuilles sont les hash de fichiers convertis en `bytes32`, le dernier nœud est dupliqué lorsque le niveau comporte un nombre impair de nœuds, puis chaque paire concaténée est hachée. Une archive ancienne peut ne pas contenir la liste exacte des feuilles éligibles à l’ancrage ; dans ce cas, le vérificateur signale une valeur attendue absente au lieu de fabriquer une conclusion.

La présence d’un reçu prouve que la transaction a été incluse. La conformité du contrat et du réseau doit également être documentée dans le manifeste pour permettre un contrôle strict de ces deux paramètres.

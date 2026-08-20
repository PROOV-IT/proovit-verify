# Vérification blockchain ProovIT

Une archive portable peut contenir l’identifiant de transaction et les paramètres publics de l’ancrage. Lorsque le RPC est accessible, `proovit-verify` récupère le reçu et recherche l’événement `ProofStoredV3` du contrat ProovStore.

Le vérificateur décode les champs publics de cet événement : `proofId`, `dataHash`, `filesRoot` et `fileCount`. Il les compare aux valeurs présentes dans le snapshot blockchain ou le manifeste de l’archive.

Les événements `FileAddedV3` sont également décodés lorsqu’ils sont présents dans un reçu accessible. Le vérificateur compare alors le `fileId`, la taille, le CID et le `metaHash` avec les métadonnées locales de chaque fichier. Les transactions d’ajout de fichiers sont généralement séparées de la transaction de dépôt ; leurs hash sont donc transportés dans `file_transactions` lorsque l’archive les fournit.

Le calcul de `filesRoot` utilisé par le backend est un arbre binaire Keccak-256 : les feuilles sont les hash de fichiers convertis en `bytes32`, le dernier nœud est dupliqué lorsque le niveau comporte un nombre impair de nœuds, puis chaque paire concaténée est hachée. Une archive ancienne peut ne pas contenir la liste exacte des feuilles éligibles à l’ancrage ; dans ce cas, le vérificateur signale une valeur attendue absente au lieu de fabriquer une conclusion.

La présence d’un reçu établit que la transaction a été incluse. La conformité du contrat et du réseau est contrôlée lorsque leurs références sont présentes et que le RPC utilisé permet de les vérifier. `fileCount` dans l’événement global représente l’état enregistré par `ProofStoredV3` ; les transactions `FileAddedV3` peuvent être vérifiées séparément.

# ProovIT Verify

Current release: `v0.2.7`.

Vérificateur indépendant des archives portables ProovIT. Il ne dépend pas de l’API ProovIT pour les contrôles offline : il lit l’archive, recalcule les hashes, vérifie la canonicalisation du manifeste, la signature Ed25519 et la timeline Web.

## Utilisation

```bash
proovit-verify preuve.zip --password 'CODE'
```

Le code est demandé interactively s’il n’est pas fourni. Pour une sortie machine :

```bash
proovit-verify preuve.zip --password 'CODE' --json
```

Les clés publiques officielles connues sont intégrées au vérificateur et sélectionnées avec `signing_key_id`. `--public-key` reste disponible uniquement pour un override technique, une ancienne clé ou un environnement privé.

La vérification blockchain utilise automatiquement l’URL publique `blockchain.rpc_url` présente dans le manifest lorsqu’elle existe. L’option manuelle reste disponible pour remplacer cette URL :

```bash
proovit-verify preuve.zip --password 'CODE' --rpc-url 'https://...'
```

Sans RPC, l’outil indique qu’une transaction est enregistrée dans l’archive mais ne prétend pas avoir vérifié le réseau.

Avec un RPC, il décode aussi l’événement `ProofStoredV3` et compare les valeurs publiques `proofId`, `dataHash`, `filesRoot` et `fileCount` avec l’archive. Voir [docs/BLOCKCHAIN-VERIFICATION.md](docs/BLOCKCHAIN-VERIFICATION.md) et [docs/PROOVIT-EVIDENCE-PROTOCOL.md](docs/PROOVIT-EVIDENCE-PROTOCOL.md).

Les événements `FileAddedV3` sont décodés lorsqu’ils sont présents dans les reçus blockchain disponibles. Les archives doivent conserver les hash des transactions individuelles pour permettre leur récupération automatique lorsque ces ajouts ont été effectués dans des transactions séparées.

## Compilation

Le projet utilise PyInstaller pour produire un exécutable autonome pour le système sur lequel la compilation est effectuée :

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt pyinstaller
.venv/bin/pyinstaller --clean --onefile --name proovit-verify proovit_verify.py
```

Pour Windows, exécuter le même build sur Windows (ou dans une CI Windows) ; PyInstaller ne réalise pas une compilation croisée fiable depuis Linux.

## Comprendre le résultat

Les contrôles `✓` sont établis à partir de l’archive, de sa signature et, si un RPC est disponible, de données publiques de la blockchain. Les lignes `ℹ` signalent une information absente ou un contrôle non applicable ; elles ne constituent pas un échec. Une ligne `!` signale une différence à examiner. La validité technique ne constitue pas, à elle seule, une décision sur la recevabilité ou la force probante juridique.

Pour un lecteur non technique, le résultat répond à quatre questions : l’archive est-elle lisible, les fichiers reçus sont-ils ceux décrits, le manifeste est-il authentique, et les éléments blockchain correspondent-ils aux données publiques de l’archive ?

## Documentation

- [Présentation pour les tiers](docs/THIRD-PARTY-GUIDE.md)
- [Protocole public ProovIT Evidence](docs/PROOVIT-EVIDENCE-PROTOCOL.md)
- [Archive et manifeste](docs/ARCHIVE-MANIFEST-V1.md)
- [Manifeste de certification V3](docs/MANIFEST-V3.md)
- [Protocole de capture Web V2](docs/WEB-EVIDENCE-V2.md)
- [Preuves multimédias](docs/MULTIMEDIA-EVIDENCE-V1.md)
- [Vérification blockchain](docs/BLOCKCHAIN-VERIFICATION.md)
- [Clés publiques](docs/PUBLIC-KEYS.md)
- [Synthetic test vectors](docs/test-vectors/README.md)

## Limites actuelles

- Le contrôle de l’archive porte sur les entrées référencées par `archive_manifest_v1`.
- Les anciennes archives peuvent ne pas contenir `proof_chain_id`, `dataHash`, `filesRoot`, `fileCount` ou les transactions individuelles des fichiers. Elles restent contrôlables pour les éléments effectivement présents.
- Pour les nouvelles archives, la taille blockchain des fichiers est documentée comme `plaintext_user_file`. Les anciennes transactions peuvent avoir utilisé la taille du blob chiffré ; le vérificateur le signale comme avertissement.
- La force juridique et la recevabilité ne sont pas déduites automatiquement par l’outil.

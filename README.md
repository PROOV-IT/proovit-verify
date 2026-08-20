# ProovIT Verify

Current release: `v0.1.3`.

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

## Compilation

Le projet utilise PyInstaller pour produire un exécutable autonome pour le système sur lequel la compilation est effectuée :

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt pyinstaller
.venv/bin/pyinstaller --clean --onefile --name proovit-verify proovit_verify.py
```

Pour Windows, exécuter le même build sur Windows (ou dans une CI Windows) ; PyInstaller ne réalise pas une compilation croisée fiable depuis Linux.

## Limites actuelles

- La conformité du hash effectivement encodé dans une transaction blockchain nécessite la connaissance de l’ABI et des règles d’encodage du contrat ; la première version vérifie la présence du reçu RPC, pas encore la reconstitution complète de l’appel contractuel.
- Le contrôle de l’archive porte sur les entrées référencées par `archive_manifest_v1`.
- La force juridique et la recevabilité ne sont pas déduites automatiquement par l’outil.

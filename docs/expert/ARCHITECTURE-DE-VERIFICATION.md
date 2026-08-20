# Architecture de vérification

**Public :** experts judiciaires, experts numériques, auditeurs et RSSI.

Le vérificateur suit une chaîne de contrôles indépendante : lecture ZIP, déchiffrement avec le code fourni, inventaire des entrées, empreintes SHA-256, canonicalisation du manifeste, signature Ed25519, timeline Web, puis références blockchain.

```mermaid
flowchart LR
  A[Archive portable] --> B[Inventaire ZIP]
  B --> C[SHA-256 des entrées]
  C --> D[Manifest V3 canonique]
  D --> E[Signature Ed25519]
  D --> F[Timeline Web]
  D --> G[Reçu blockchain]
  E --> H[Rapport]
  F --> H
  G --> H
```

## Séquences spécialisées

```mermaid
flowchart LR
  W[Session Web] --> W1[Événements]
  W1 --> W2[Chaîne de hashes]
  W2 --> W3[evidence_root_hash]
  M[Fichier original] --> M1[SHA-256]
  M1 --> M2[Artefacts dérivés]
  M2 --> M3[Manifest par fichier]
  M3 --> G[Ancrage blockchain]
```

Les contrôles hors ligne ne nécessitent pas l’API PROOV-IT. Les contrôles blockchain utilisent un RPC public indiqué dans le manifeste ou fourni explicitement. Les réponses réseau sont traitées comme des données externes et doivent être conservées avec le rapport.

Les contrôles sont séparés par domaine afin qu’une donnée absente ou non applicable ne soit pas interprétée comme une altération d’un autre domaine. Les formats et algorithmes exacts sont décrits dans [les spécifications](../specs/PROOVIT-EVIDENCE-PROTOCOL.md), [le manifeste V3](../specs/MANIFEST-V3.md) et [la vérification blockchain](../specs/BLOCKCHAIN-VERIFICATION.md).

## Ordre et indépendance

Les contrôles locaux peuvent être réalisés sans API PROOV-IT. Les contrôles externes commencent uniquement après résolution d’une référence de transaction et d’un RPC public. Chaque résultat conserve sa source : archive, calcul local ou réponse réseau.

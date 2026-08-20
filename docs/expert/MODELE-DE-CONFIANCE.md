# Modèle de confiance

## Contrôles reproductibles indépendamment

À partir de l’archive et des ressources publiques, un tiers peut recalculer les empreintes des fichiers, la canonicalisation du manifeste, la signature Ed25519, la chaîne de timeline Web et les valeurs décodées d’un reçu blockchain lorsque le réseau est accessible.

## Contexte d’acquisition enregistré

Le navigateur, l’environnement d’exécution, l’URL demandée, l’identité de compte, la géolocalisation fournie par le terminal et certains identifiants d’appareil sont des informations enregistrées dans le contexte d’acquisition. Leur origine et leur portée doivent être appréciées avec les éléments du dossier.

## Attestations externes

La blockchain publique, un jeton RFC3161 ou un stockage immuable peuvent fournir des attestations externes lorsqu’ils sont présents et contrôlables. Un jeton identifié comme non qualifié ne doit pas être présenté comme un horodatage qualifié.

## Périmètre d’interprétation

Le vérificateur établit des correspondances cryptographiques et des cohérences techniques. Il ne statue pas sur la vérité matérielle d’un événement, l’identité de son auteur, la recevabilité d’un document ou sa force probante.

## Traitement des entrées

Implementations should reject malformed JSON, invalid UTF-8, invalid signatures, path traversal, oversized decompression and unsafe HTML rendering. RPC responses and archive metadata must be treated as untrusted data.

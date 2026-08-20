# Preuves multimédias

Les preuves multimédias peuvent contenir des images, vidéos, fichiers audio, documents, signatures et artefacts techniques. Chaque fichier est contrôlé individuellement lorsqu’il est référencé dans l’inventaire de l’archive.

Le hash de fichier porte sur la représentation utilisateur conservée dans l’archive. Les opérations techniques de stockage, d’encryption ou de dérivation peuvent produire des artefacts différents ; ils doivent être décrits séparément et ne doivent pas être confondus avec le hash du fichier utilisateur.

Pour les fichiers ancrés sur la blockchain, `FileAddedV3` publie l’identifiant du fichier, son CID, sa taille déclarée et son `metaHash`. Le CID peut viser le contenu chiffré, tandis que `metaHash` et la taille suivent le fichier utilisateur selon la version du protocole.

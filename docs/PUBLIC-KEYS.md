# Clés publiques de signature

Le vérificateur contient un registre de clés publiques identifiées par `signing_key_id`. Une clé publique est utilisée uniquement pour vérifier une signature ; aucune clé privée n’est distribuée dans ce dépôt.

Le registre actuel est maintenu dans `proovit_verify.py`. Toute rotation de clé doit publier un nouvel identifiant, conserver l’ancienne clé pour les archives historiques et faire l’objet d’une release documentée.

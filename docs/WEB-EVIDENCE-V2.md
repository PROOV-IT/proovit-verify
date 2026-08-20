# Protocole de capture Web V2

Une preuve Web peut contenir une chronologie d’événements : ouverture de session, navigation, capture, gel d’état et finalisation. Chaque événement contient un numéro de séquence, un type, un contenu normalisé et le hash de l’événement précédent.

Le vérificateur contrôle que les séquences sont continues, que le premier événement référence l’absence de précédent, que chaque hash correspond au contenu canonique et que le dernier hash correspond à la valeur annoncée.

Une archive qui ne contient pas de timeline Web n’est pas une preuve Web incomplète par défaut : elle peut correspondre à une capture multimédia ou à un autre type de preuve. Le résultat indique alors que le contrôle Web n’est pas applicable.

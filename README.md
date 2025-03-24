# FrancisBot

**FrancisBot** est un bot Telegram créé par [eNudimmud](https://github.com/eNudimmud), un fermier virtuel du canton de Vaud qui aide les utilisateurs à explorer le monde des cryptomonnaies de manière ludique et éducative. Avec Francis, vous pouvez simuler du trading, suivre les prix des cryptos, gérer un portefeuille fictif, et même préparer l’arrivée de $MILK et des NFT Highland !

## Fonctionnalités
- **Conseils crypto** : Obtenez des astuces pour le trading classique, degen, la gestion des risques, et plus encore.
- **Prix en temps réel** : Consultez les prix actuels des cryptomonnaies avec `/prix <symbole>` (ex. `/prix BTC`).
- **Portefeuille simulé** : Gérez un champ fictif avec `/portefeuille` (ajouter, voir, stats, retirer, top).
- **$MILK & $CHEESE** : Gagnez du $MILK fictif et stackez-le en $CHEESE pour les futurs services premium.
- **Phases lunaires** : Découvrez l’impact de la lune sur le marché avec `/lune`.
- **NFT Highland** : Préparez-vous pour les futurs NFT avec `/nft`.

## Prérequis
- Python 3.12+
- Bibliothèques : `python-telegram-bot`, `aiohttp`, `ephem`, `nest_asyncio`
- Un token Telegram via [BotFather](https://t.me/BotFather)


Commandes



start - Démarrer Francis 



help - Voir la liste des commandes



trading - Conseil de trading classique 



degen - Conseil pour le trading degen 



risques - Conseil sur la gestion des risques 



scam - Prévention des arnaques 



bots - Découvrir les outils et bots 



conseil - Conseil crypto aléatoire 



lune - Impact de la lune sur le marché 



swissmilk - Future tokenisation de Francis 



prix - Prix actuel d’une crypto (ex. /prix BTC) 



portefeuille - Gérer ton champ simulé (ajouter, voir, stats, retirer, top)



milk - Voir ton $MILK et $CHEESE



stack - Stacker ton $MILK en $CHEESE (simulation)



nft - Découvrir les futurs NFT Highland


Structure du projet

main.py : Point d’entrée du bot



config/settings.py : Constantes et configuration



utils/helpers.py : Fonctions utilitaires (API, JSON)



commands/ : Commandes Telegram (basic, advice, info, portfolio, token)



tasks/price_update.py : Mise à jour périodique des prix




# TODO.md - CLI Todo Python

## Status: EN COURS

## Critères de Succès

- [ ] `todo.py` existe et est exécutable
- [ ] Commande `add` fonctionne
- [ ] Commande `list` fonctionne
- [ ] Commande `done` fonctionne
- [ ] Commande `delete` fonctionne
- [ ] Gestion d'erreur ID inexistant
- [ ] Tests passent : `python -m pytest tests/`
- [ ] README.md complet

## Plan d'Exécution

### Phase 1 : Setup
- [ ] Créer la structure de dossiers
- [ ] Créer `todo.py` avec argparse de base
- [ ] Créer `tests/test_todo.py` vide
- [ ] Commit initial

### Phase 2 : Stockage
- [ ] Implémenter `load_todos()` - charge le JSON
- [ ] Implémenter `save_todos()` - sauvegarde le JSON
- [ ] Tester le stockage

### Phase 3 : Commandes
- [ ] Implémenter `add`
- [ ] Tester `add` manuellement
- [ ] Implémenter `list`
- [ ] Tester `list` manuellement
- [ ] Implémenter `done`
- [ ] Tester `done` manuellement
- [ ] Implémenter `delete`
- [ ] Tester `delete` manuellement

### Phase 4 : Robustesse
- [ ] Ajouter gestion d'erreur (ID inexistant)
- [ ] Ajouter messages d'aide

### Phase 5 : Tests & Docs
- [ ] Écrire tests unitaires (5+ tests)
- [ ] Vérifier `pytest` passe
- [ ] Écrire README.md

### Phase 6 : Validation
- [ ] Vérifier tous les critères
- [ ] Commit final

## État Actuel

**Tour actuel :** 0
**Dernière action :** En attente
**Prochaine action :** Lire PROMPT.md, créer structure

## Notes

(Ralph ajoute ses notes ici)

## HARD STOP TRIGGER

<!-- Décommenter quand le projet est terminé -->
<!-- - [x] DONE - Projet terminé -->

"""Recherche du racourci de l'équipe."""
def help_teams(team):
    equipes=[["NYJ","New York Jets"],["CBr","Cleveland Browns"]]
    for liste in equipes:
        if team in liste[0] or team in liste[1]:
            return liste
        else:
            return "Aucune équipe ne correspond à vortee entrée"

"""Traitement des données"""
liste_franchise=[]
from csv import*
with open('NYJ.csv', 'r') as csvfile:
    obj = reader(csvfile)

    for ligne in obj:
        liste_franchise.append(ligne)
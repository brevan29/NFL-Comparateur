"""Importation des modules et définition des variables"""
from csv import*
import matplotlib.pyplot as plt

liste_franchise=[]
Attaques={}
Defenses={}
stats=[]
chiffre=""
AGarder_att=[]
AGarder_def=[]
Matchs_joués=0
at=0
de=0
franchises=[["ACa","Arizona Cardinals"],["AFa","Atlanta Falcons"],["BRa","Baltimore Ravens"],["BBi","Buffalo Bills"],["CPa","Carolina Panthers"],["ChB","Chicago Bears"],["CiB","Cincinnati Bengals"],
            ["CBr","Cleveland Browns"],["DCo","Dallas Cowboys"],["DBr","Denver Broncos"],["DLi","Detroit Lions"],["GBP","Green Bay Packers"],["HTe","Houston Texans"],["ICo","Indianapolis Colts"],
            ["JJa","Jacksonville Jaguars"],["KCC","Kansas City Chiefs"],["LVR","Las Vegas Raiders"],["LAC","Los Angeles Chargers"],["LAR","Los Angeles Rams"],["MDo","Miami Dolphins"],
            ["MVi","Minnesota Vikings"],["NEP","New England Patriots"],["NOS","New Orleans Saints"],["NYG","New York Giants"],["NYJ","New York Jets"],["PEa","Philadelphia Eagles"],
            ["PSt","Pittsburgh Steelers"],["SF49","San Francisco 49ers"],["SSe","Seattle Seahawks"],["TBB","Tempa Bay Buccaneers"],["TTi","Tenessee Titans"],["WCo","Washington Commanders"]]
#^Elles sont rangées par ordre alphabétique selon leur nom^


"""Recherche du racourci de l'équipe."""
def help_teams(team):
    for liste in franchises:
        if team in liste[0] or team in liste[1]:
            return liste
    return "Aucune équipe ne correspond à vortee entrée"


"""Lecture des données"""

for i in range (4):
    equipe=franchises[i][0]
    fichiercsv="Equipes/"+equipe+".csv"
    fichier=open(fichiercsv, 'r', encoding='utf-8')
    obj = reader(fichier)

    for ligne in obj:
        liste_franchise.append(ligne)
        
    fichier.close()
    
    Matchs_joués=len(liste_franchise) #Pour travailler avec des moyennes et apporter une égalité avec les équipes ayant eu leur "bye week" (Ne se fera que pour ce qui se compte en Yards)
    
    for element in liste_franchise:
        while element[0]!="":
            if element[0][0]!=";":
                chiffre+=element[0][0]
            else:
                if "." in chiffre:
                    stats.append(float(chiffre))
                else:
                    stats.append(int(chiffre))
                chiffre=""
            if len(element[0])>=2:
                element[0]=element[0][1:]
            else:
                element[0]=""
                stats.append(int(chiffre))
        AGarder_att.append(stats[1:8])
        AGarder_def.append(stats[8:])
        stats=[]
        
    AGarder_att.append([0,0,0,0.0,0,0,0])
    AGarder_def.append([0,0,0,0.0,0,0,0]) #Ajout d'une liste pour le total
    
    for t in range (7): #Pour le total de toutes les stats
        at=AGarder_att[0][t]+AGarder_att[1][t]+AGarder_att[2][t]
        de=AGarder_def[0][t]+AGarder_def[1][t]+AGarder_def[2][t]
        if t<4 :
            AGarder_att[3][t]=at/(Matchs_joués)
            AGarder_def[3][t]=de/(Matchs_joués)
            if t<3:
                AGarder_att[3][t]=int(AGarder_att[3][t])
                AGarder_def[3][t]=int(AGarder_def[3][t])
            else:
                AGarder_att[3][t]=float(str(AGarder_att[3][t])[:3])
                AGarder_def[3][t]=float(str(AGarder_def[3][t])[:3])
        else :
            AGarder_att[3][t]=at
            AGarder_def[3][t]=de
        
    Attaques[equipe]=AGarder_att
    Defenses[equipe]=AGarder_def
    AGarder_def=[]
    AGarder_att=[]
    liste_franchise=[]
    
def classement(qui, quoi):
    """
    qui = l'équipe si on la définit avec son ID sinon inscrire 'ovr' (overall) qui nous donnera la meilleure équipe pour la catégorie souhaitée
    quoi = catégorie dont on souhaite le classement de l'équipe (ou la meilleure équipe de la catégorie)
    Les catégories sont :
        Attaque:
            Attaque : Les yards en tout
            A_Passe : Les yards parcourus à la passe
            A_Course : Les yards parcourus à la course
            A_Action : Nombre de Yards parcouru en moyenne par action
            A_Sacks : Nombre de sacks encaissé par l'équipe offensive
            A_Int : Nombre de passes qui ont été interceptées par l'équipe adverse
            A_Marqués : Points marqués
        Défense:
            Defense : Yards concédés par l'équipe défensive
            D_Passe : Yards encaissés à la passe
            D_Course : Yards perdus à la course
            D_Action : Nombre moyen de yards encaissés par action
            D_Sacks : Nombre de Sacks effectués
            D_Int : Nombre de ballons récupérés par interception
            D_Encaissés : Points encaissés
    """
    """Recherche de ce qui doit être traité"""
    Dico={"At": "Attaque", "De": "Défense", "A_": "Attaque", "D_": "Défense", "t":0,"f":0,"P":1,"C":2,"A":3,"S":4,"I":5,"M":6,"E":6}
    jeu=Dico[quoi[0:2]] #Soit Attaque, Soit Défense. La première lettre en dit beaucoup.
    Catégorie=Dico[quoi[2]]#Tout, Passe, Course, Progression, Sacks, Intercepetion ? La différence se trouve sur la 3ème lettre.
    score=1
    meilleur_score=0
    best_equipe="Moi"
    if qui=="ovr":
        for team in franchises[0:4]:
            if (jeu=="Attaque" and "A_I" not in quoi and "A_S" not in quoi) or ("D_S" in quoi or "D_I" in quoi): #Les catégories qui sont mieux quand c'est plus grand
                if jeu=="Attaque":
                    score=Attaques[team[0]][3][Catégorie]
                else:
                    score=Defenses[team[0]][3][Catégorie]
                if score>meilleur_score:
                    meilleur_score=score
                    best_equipe=team[1]
                    
            else : #C'est mieux quand c'est plus petit
                if best_equipe=="Moi":
                    if jeu=="Defense":
                        meilleur_score=Defenses[team[0]][3][Catégorie]
                    else:
                        meilleur_score=Attaques[team[0]][3][Catégorie]
                    best_equipe=team[1]
                    
                if jeu=="Défense":
                    score=Defenses[team[0]][3][Catégorie]
                else:
                    score=Attaques[team[0]][3][Catégorie]
                if score>meilleur_score:
                    meilleur_score=score
                    best_equipe=team[1]
        return best_equipe
    else:
        if jeu=="Attaque":
            meilleur_score=Attaques[qui][3][Catégorie]
        else:
            meilleur_score=Defenses[qui][3][Catégorie]
        for team in franchises[0:4]:
            if team[0]!=qui:
                if (jeu=="Attaque" and "A_I" not in quoi and "A_S" not in quoi) or ("D_S" in quoi or "D_I" in quoi): #Les catégories qui sont mieux quand c'est plus grand
                    if jeu=="Attaque":
                        if Attaques[team[0]][3][Catégorie]>meilleur_score:
                            score+=1
                    else:
                        if Defenses[team[0]][3][Catégorie]>meilleur_score:
                            score+=1
                else:
                    if jeu=="Défense":
                        if Defenses[team[0]][3][Catégorie]<meilleur_score:
                            score+=1
                    else:
                        if Attaques[team[0]][3][Catégorie]<meilleur_score:
                            score+=1
    return score

classement('BRa', 'Defense')
  
    
"""Faire le suivi de 2 équipes et les comparaisons de classement"""

def comparaison(team1, team2, quoi):
    t1=help_teams(team1)[1]
    t2=help_teams(team2)[1]
    Dico={"At": "Attaque", "De": "Défense", "A_": "Attaque", "D_": "Défense", "t":0,"f":0,"P":1,"C":2,"A":3,"S":4,"I":5,"M":6,"E":6}
    jeu=Dico[quoi[0:2]]
    Catégorie=Dico[quoi[2]]
    
    print('Comparaison entre '+t1+' et '+t2+' :')
    print("Attaque : "+str(classement(team1, 'Attaque'))+' vs '+str(classement(team2, 'Attaque')))
    print("Passe :"+str(classement(team1, 'A_Passe'))+' vs '+str(classement(team2, 'A_Passe')))
    print("Course : "+str(classement(team1, 'A_Course'))+' vs '+str(classement(team2, 'A_Course')))
    print("Action : "+str(classement(team1, 'A_Action'))+' vs '+str(classement(team2, 'A_Action')))
    print("Sacks : "+str(classement(team1, 'A_Sacks'))+' vs '+str(classement(team2, 'A_Sacks')))
    print("Interceptions : "+str(classement(team1, 'A_Int'))+' vs '+str(classement(team2, 'A_Int')))
    print("Points marqués : "+str(classement(team1, 'A_Marqués'))+' vs '+str(classement(team2, 'A_Marqués')))
    print('')
    print("Defense : "+str(classement(team1, 'Defense'))+' vs '+str(classement(team2, 'Defense')))
    print("Passe : "+str(classement(team1, 'D_Passe'))+' vs '+str(classement(team2, 'D_Passe')))
    print("Course : "+str(classement(team1, 'D_Course'))+' vs '+str(classement(team2, 'D_Course')))
    print("Action : "+str(classement(team1, 'D_Action'))+' vs '+str(classement(team2, 'D_Action')))
    print("Sacks : "+str(classement(team1, 'D_Sacks'))+' vs '+str(classement(team2, 'D_Sacks')))
    print("Interceptions : "+str(classement(team1, 'D_Int'))+' vs '+str(classement(team2, 'D_Int')))
    print("Points encaissés : "+str(classement(team1, 'D_Encaissés'))+' vs '+str(classement(team2, 'D_Encaissés')))
    #créer une ui dans la console pour faciliter la création du grafiak :)
    if jeu=="Attaques":
        plt.plot([1,2,3],[Attaques[team1][0][Catégorie],Attaques[team1][1][Catégorie],Attaques[team1][2][Catégorie]], label=t1)
        plt.plot([1,2,3],[Attaques[team2][0][Catégorie],Attaques[team2][1][Catégorie],Attaques[team2][2][Catégorie]], label=t2)
    else:
        plt.plot([1,2,3],[Defenses[team1][0][Catégorie],Defenses[team1][1][Catégorie],Defenses[team1][2][Catégorie]], label=t1)
        plt.plot([1,2,3],[Defenses[team2][0][Catégorie],Defenses[team2][1][Catégorie],Defenses[team2][2][Catégorie]], label=t2)
    plt.legend()
    plt.show()
    return None


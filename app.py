import mariadb
import random
from flask import Flask, render_template, request, redirect, url_for, session
from classes import Produit, Compte
from bd import obtenirConnexion

app = Flask(__name__)
app.secret_key = 'JeSuisUneCleQuiDoitDemeureeSecrete'

@app.route('/déconnexion')
def deconnexion():
    session.pop('utilisateur', None)
    return redirect(url_for('connexion'))

@app.route('/')
def pageAccueil():
    return redirect('/connexion')

@app.route('/connexion')
def connexion():
    return render_template('authentification.html')

@app.route('/connexion',methods=['POST'])
def connexionPost():
    nomUtilisateur = request.form['fNomUtilisateur']
    motDePasse = request.form['fMotDePasse']
    if( not nomUtilisateur or not motDePasse):
        message = 'Information incorrecte'
        return render_template('/authentification.html', message = message)
    connexion = obtenirConnexion()
    try :
        curseur = connexion.cursor()
        curseur.execute('SELECT admin FROM utilisateur WHERE nom=? AND motDePasse=?',(nomUtilisateur,motDePasse))
        estAdmin = curseur.fetchone()
        if(estAdmin is None):
           return render_template('authentification.html', message = "Vous avez entrez les mauvaises informations")
        estAdmin = estAdmin[0]
        session['utilisateur'] = nomUtilisateur
        if estAdmin == 1:
            return redirect(url_for('admin'))
        else:
            return redirect('/magasins')
    finally:
        connexion.close()


@app.route('/admin')
def admin():
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        if 'utilisateur' not in session:
            return redirect(url_for('connexion'))
        nomUtilisateur = session['utilisateur']
        curseur.execute('SELECT admin FROM utilisateur WHERE nom = ?', (nomUtilisateur,))
        estAdmin, = curseur.fetchone()
        if  estAdmin is None or estAdmin == 0:
            return redirect(url_for('connexion'))
    finally:
        connexion.close()
    return render_template('/comptes/admin.html')

@app.route('/admin/comptes',methods=['GET'])
def comptes():
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        if 'utilisateur' not in session:
            return redirect(url_for('connexion'))

        nomUtilisateur = session['utilisateur']
        curseur.execute('SELECT admin FROM utilisateur WHERE nom = ?', (nomUtilisateur,))
        estAdmin, = curseur.fetchone()
        curseur.close()
        if  estAdmin is None or estAdmin == 0:
            return redirect(url_for('connexion'))
        else:
            curseur = connexion.cursor()
            curseur.execute('SELECT id, nom FROM utilisateur')
            return render_template('/comptes/comptes.html', liste = curseur.fetchall())
    finally:
        connexion.close()

@app.route('/admin/comptes/creer')
def creationCompte():
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        if 'utilisateur' not in session:
            return redirect(url_for('connexion'))

        nomUtilisateur = session['utilisateur']
        curseur.execute('SELECT admin FROM utilisateur WHERE nom = ?', (nomUtilisateur,))
        estAdmin, = curseur.fetchone()
        curseur.close()
        if  estAdmin is None or estAdmin == 0:
            return redirect(url_for('connexion'))
        else:
            return render_template('/comptes/creationCompte.html')
    finally:
        connexion.close()

@app.route('/admin/comptes/creer', methods=['POST'])
def creationComptePost():
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        nom = request.form['fNomUtilisateur'].strip()
        motDePasse = request.form['fMotDePasse'].strip()
        admin = request.form.get('fAdmin')
        if (admin == 'on'):
            admin = True
        else:
            admin = False
        if (len(nom) > 0 and len(motDePasse) > 0):
            sql = 'INSERT INTO utilisateur (nom, motDePasse,admin) VALUES (?, ?, ?)'
            values = (nom, motDePasse, int(admin))
            curseur.execute(sql, values)
            connexion.commit()
        else:
            message = 'Veuillez remplir les champs correctement'
            return render_template('/comptes/creationCompte.html', message = message)
        return redirect('/admin/comptes')
    finally:
        connexion.close()

@app.route('/admin/comptes/supprimer/<int:idUtilisateur>')
def supprimerCompte(idUtilisateur):
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        curseur.execute('DELETE FROM utilisateur WHERE id = ?',(idUtilisateur, ))
        connexion.commit()
        return redirect(url_for('comptes'))
    finally:
        connexion.close()


@app.route('/magasins', methods=['GET'])
def magasins():
    connexion = obtenirConnexion()
    try:
        curseurMagasins = connexion.cursor()
        curseurMagasins.execute('SELECT * FROM magasin')
        return render_template('/magasins/magasins.html', liste = curseurMagasins.fetchall())
    finally:
        connexion.close()

@app.route('/magasins/<string:id>',methods=['GET'])
def afficherProduitDeUnMagasin(id):
    connexion = obtenirConnexion()
    try:
        curseurProduits = connexion.cursor()
        curseurProduits.execute('SELECT * FROM produit WHERE magasinId = ? OR magasinId IS NULL', (id,))
        lstProduits = []
        for produit in curseurProduits:
            lstProduits.append(Produit(produit))
        curseurProduits.close()
        curseurMagasin = connexion.cursor()
        for produit in lstProduits:
            curseurMagasin.execute('SELECT type FROM type WHERE typeId = ?', (produit.type,))
            for leType, in curseurMagasin:
                produit.type = leType
        return render_template('/produits/produits.html', lstProduits = lstProduits, id = id)
    finally: 
        connexion.close()



@app.route('/magasins/tous', methods=['GET'])
def listeProduits():
    connexion = obtenirConnexion()
    try:
        curseurProduits = connexion.cursor()
        curseurProduits.execute('SELECT * FROM produit')
        lstProduits = []
        for produit in curseurProduits:
            lstProduits.append(Produit(produit))
        curseurProduits.close()
        curseurMagasin = connexion.cursor()
        for produit in lstProduits:
            curseurMagasin.execute('SELECT type FROM type WHERE typeId = ?', (produit.type,))
            for leType, in curseurMagasin:
                produit.type = leType
        return render_template('/produits/produits.html', lstProduits = lstProduits, id = 'tous')
    finally:
        connexion.close()

@app.route('/magasins/<string:id>/produit/créer', methods=['GET'])
def creerProduit(id):
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        lstCategories = []
        curseur.execute('SELECT * FROM type')
        for categorie in curseur:
            lstCategories.append(categorie)
        curseur.close()
        return render_template('/produits/CréationProduit.html', idMagasin= id, lstCategories = lstCategories)
    finally:
        connexion.close()

@app.route('/magasins/<string:id>/produit/créer', methods=['POST'])
def produitCreer(id):
    lstMessages = []
    nom = str(random.randint(60000000000, 69999999999))
    description = request.form['fDescription']
    if len(description)<=0:
        lstMessages.append('Le produit doit avoir une description')
    prix = request.form['fPrix']
    if len(prix)<=0:
        lstMessages.append('Le produit doit avoir un prix (insérez 0 s\'il est gratuit)') 
    coutant = request.form['fCoutant']
    if len(coutant)<=0:
        lstMessages.append('Le produit doit avoir un prix coutant (insérez 0 s\'il coute rien)') 
    stock = request.form['fStock']
    if len(stock)<=0:
        lstMessages.append('Le produit doit avoir une quantité en stock (insérez 0 s\'il n\'est pas en stock)') 
    format = request.form['fFormat']
    taxe = request.form['fTaxe']
    taxableFederal = taxe == 'F'
    taxableProvincial = taxe == 'P'
    categorie = request.form['Categorie']

    if len(lstMessages) > 0:
        return render_template('produits/CréationProduit.html', lstMessages = lstMessages)

    connexion = obtenirConnexion()
    if id != 'tous':
        idMagasin = id
    else: idMagasin = None
    try:
        sql = 'INSERT INTO produit (nom, description, stock, coutant, format, prix, magasinId, type, taxableFederal, taxableProvincial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        values = (nom, description,stock, coutant,format ,prix, idMagasin, categorie, taxableFederal, taxableProvincial)
        curseur = connexion.cursor()
        curseur.execute(sql, values)
        connexion.commit()
    finally:
        connexion.close()
    return redirect('/magasins/'+str(id))

@app.route('/magasins/<string:id>/produit/supprimer/<string:idProduit>')
def supprimerProduit(id, idProduit):
    if 'utilisateur' not in session:
        return redirect(url_for('connexion'))
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        sql = 'DELETE FROM produit WHERE produitId = ?'
        value = idProduit,
        curseur.execute(sql, value)
        connexion.commit()
    finally:
        connexion.close()
    return redirect('/magasins/' + id)

@app.route('/magasins/<string:id>/produit/modifier/<string:idProduit>', methods=['GET'])
def modifierProduit(id, idProduit):
    connexion = obtenirConnexion()
    try:
        curseur = connexion.cursor()
        lstCategories = []
        curseur.execute('SELECT * FROM type')
        for categorie in curseur:
            lstCategories.append(categorie)
        curseur.close()
        curseur = connexion.cursor()
        sql = 'SELECT * FROM produit WHERE produitId = ?'
        value = idProduit,
        curseur.execute(sql, value)
        produit = curseur.fetchone()
        leProduit = []
        for produits in produit:
            leProduit.append(produits)
        leProduit.append('')
        if (bool(leProduit[10])):
            leProduit[10] = 'checked=True'
        elif(bool(leProduit[11])):
            leProduit[11] = 'checked=True'
        else:
            leProduit[12] = 'checked=True'
        return render_template('produits/modificationProduits.html',idMagasin = id ,lstCategories = lstCategories, produit = leProduit, id = idProduit)
    finally:
        connexion.close()

@app.route('/magasins/<string:id>/produit/modifier/<string:idProduit>', methods=['POST'])
def modifierProduitPost(id, idProduit):
    description = request.form['fDescription']
    prix = request.form['fPrix']
    coutant = request.form['fCoutant']
    stock = request.form['fStock']
    format = request.form['fFormat']
    taxe = request.form['fTaxe']
    taxableFederal = taxe == 'F'
    taxableProvincial = taxe == 'P'
    categorie = request.form['Categorie']
    connexion = obtenirConnexion()
    if id != 'tous':
        idMagasin = id
    else: idMagasin = None
    try:
        sql = 'UPDATE produit SET description=?, stock=?, coutant=?, format=?, prix=?, magasinId=?, type=?, taxableFederal=?, taxableProvincial=? WHERE produitId = ?'
        values =  (description,stock, coutant,format ,prix, idMagasin, categorie, taxableFederal, taxableProvincial, idProduit)
        curseur = connexion.cursor()
        curseur.execute(sql, values)
        connexion.commit()
    finally:
        connexion.close()
    return redirect('/magasins/'+str(id))


@app.errorhandler(404)
def erreur404(e):
    return render_template('/erreurs/404.html')

if __name__ == '__main__':
    app.run(debug=True)


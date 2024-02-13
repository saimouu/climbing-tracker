# Climbing Tracker / Tietokannat ja web-ohjelmointi, Kevät 2024

## Tilanne 4.2.2024
Sovelluksen runko on toimiva. Käyttäjiin liittyvät ominaisuudet kuten sisäänkirjautuminen ja rekisteröiminen toimii sujuvasti.
Reittejä pystyy lisäämään ja niitä kommentoimaan. Reitin lisääjä pystyy myös poistamaan reitin. Tällä hetkellä etusivulla näkyy kaikki
muiden käyttäjien lisäämät reitit, joka tilanteessa jossa olisi esim. 1000 reittiä ei olisi kovin realistista. Ylläpitäjä toiminto puuttuu ja reitteihin
on ideana vielä lisätä enemmän dataa. Osa uudelleenohjauksista toimii hieman epäintuitiivisesti ja reittien poisto-ominaisuus täytyy muutta lomakkeeksi.

## Ohjeet sovelluksen testaamiseen paikallisesti
Kloonaat tämä repositorio ja luo sen juurikansioon seuraavanlainen .env tiedosto.

```
DATABASE_URL=<tietokannan osoite>
SECRET_KEY=<salainen avain>
```
Luo virtuaaliympäristö ja asenna riippuvuudet.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
Pävitä tietokannan skeema ja käynnistä sovellus
```
$ psql < schema.sql
$ flask run
```
## Sovelluksen perusidea
Sovelluksen avulla käyttäjä pystyy seuraamaan omaa kiipeily kehitystään, ja jakamaan saavutuksiaan ja tavoitteittaan. 
Pääpiirteenä on juuri omien kiivettyjen reittien ja kehityksen seuaranta, mutta myös niiden jakaminen muiden kanssaharrastajien kesken.
Reittejä pystyy jakamaan ja arvioimaan, ja käyttäjät voivat tutkia muiden käyttäjien sivuja. Käyttäjä pystyy tutkimaan omalla sivullaan
yhteenvetoa kiivetyistä reiteistä ja seurata mahdollisten tavoitteiden etenemistä.

Suunniteltuja sovelluksen ominaisuuksia: 
   - Käyttäjä voi kirjautua sisään ja luoda uuden tunnuksen
   - Käyttäjä näkee omat reittinsä ja niihin liittyvät datat
   	  - esim. reitin vaikeustaso, sijainti, ulko/sisä reitti, flash (ei/kyllä)
   - Käyttäjä pystyy lisäämään reittejä ja niihin liittyvää informaatiota
   - Käyttäjä voi selata muiden lisäämiä reittejä ja heidän kommentteja niihin liittyen
       - esim. sijainnin perusteella
   - Käyttäjä voi arvoida reittin vaikeustasoa ja verrata muiden antamiin vaikeustasoihin 
   	(tai reitin suunnitelijan antamaan)
   - Ylläpitäjä voi poistaa reittejä
   - (Mahdollinen ryhmä ominaisuus)

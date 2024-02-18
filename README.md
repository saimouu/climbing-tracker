# Climbing Tracker / Tietokannat ja web-ohjelmointi, Kevät 2024

## Sovelluksen perusidea
Sovelluksen avulla käyttäjä pystyy seuraamaan omaa kiipeily kehitystään ja jakamaan saavutuksiaan. 
Pääpiirteenä on juuri omien kiivettyjen reittien ja kehityksen seuranta, mutta myös niiden jakaminen muiden kanssaharrastajien kesken.
Reittejä pystyy jakamaan ja käyttäjät voivat tutkia muiden käyttäjien sivuja. Käyttäjä pystyy tutkimaan omalla sivullaan
yhteenvetoa kiivetyistä reiteistä ja seurata mahdollisten tavoitteiden etenemistä.

## Tämän hetkiset ominaisuudet
   - Käyttäjä voi kirjautua sisään/ulos ja luoda uuden tunnuksen
   - Käyttäjä pystyy lisäämään reittejä ja niihin liittyvää informaatiota
      - vaikeustaso, sijainti, ulko/sisä reitti, flash (ei/kyllä), kuva
   - Reittejä voi selata ja niitä kommentoida
   - Käyttäjä voi poistaa omia reittejään ja kommenttejaan
   - Käyttäjä näkee omalla sivullaan omat reittinsä, vaikeustasojen jakauman ja kommenttinsa
   - Käyttäjä voi tutkia muiden käyttäjien sivuja

## Mahdollisia listättäviä ominaisuuksia
   - Haku ominaisuus tiedettyjen sijaintien perusteella
   - Reittien lisääminen yksityisiksi
   - Admin työkalujen järkevä toteutus

## Ohjeet sovelluksen testaamiseen paikallisesti
Kloonaa tämä repositorio ja luo sen juurikansioon seuraavanlainen .env tiedosto.

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

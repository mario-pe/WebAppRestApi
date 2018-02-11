Instrukcja do API

dodanie Url:
a adres  http://127.0.0.1:8000/zad/get_url/ metoda POST należy przeslac adres który zostanie zachowany oraz zabezpieczony 

{
        "url": "https://www.google.pl/"
    }

pobranie pliku:
na adres http://127.0.0.1:8000/zad/get_file/ metoda PUT należy przeslac request w body powinien znalezc
 
 {
        "url": "/zad/details_url/165/",
        "password": "KFLqKdtqUd"
    }

dodanie pliku:
na adres http://127.0.0.1:8000/zad/get_file/ metoda POST należy przeslac plik

pobranie pliku:
na adres http://127.0.0.1:8000/zad/get_file/ metoda PUT należy przeslac request w body powinien znalezc się adres pliku i haslo
 
 {
        "url": "/zad/details_file/19/",
        "password": "GxQ3jzZ2kk"
    }
    
pobranie statystyk:
do adres http://127.0.0.1:8000/zad/archive/<data_from>/<data_to> należy dolaczyc parametry: date od kiedy maja być pobrane statystyki oraz date do kiedy moja być pobrane statystyki. Wymagany format daty RRRR-MM-DD

http://127.0.0.1:8000/zad/archive/2018-02-05/2018-02-10

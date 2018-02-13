Instrukcja startu aplikacji pod systemem operacyjnym Linux

W terminalu utworz nowy katalog w ktorym znajdzie sie projekt:

mkdir ale_super_project

nastepnie postepuj zgodnie z punktami

1) cd ale_super_project
2) git init
3) git clone https://github.com/mario-pe/BitCraft.git
4) cd BitCraft/
5) python manage.py makemigrations
6) python manage.py migrate
7) python manage.py test  - polecenie to uruchomi testy jednostkowe
8) python manage.py runserver

w drugim terminalu nalezy przejsc do katalogu zawierajacego projekt wpisac polecenie:

  celery -A BitCraft worker --loglevel=info --beat

uruchomi ono watki odpowiedzialne za czyszczenie bazy oraz przygotowywanie statystyk.
Teraz aplikacja powinna dzialac. W razie problemow prosze o kontakt. 

Instrukcja do API

dodanie Url:
na adres  http://127.0.0.1:8000/zad/get_url/ metoda POST należy przeslac adres który zostanie zachowany oraz zabezpieczony 

{
        "url": "https://www.google.pl/"
    }

pobranie pliku:
na adres http://127.0.0.1:8000/zad/get_file/ metoda PUT należy przeslac request w body powinien znalezc wygenrowany adres do zasobu oraz poprawne hasło
 
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

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Player, Type_Player
from .serializers.playerSerializer import PlayerSerializer
from .serializers.typePlayerSerializer import TypePlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    url = 'https://www.hltv.org'

    def scrape(self, url_player):

        """ Configuraciones del navegador """
        options = Options() # Se crea configuración para el navegador automatizado
        options.headless = True  # Ejecutar sin abrir ventana

        driver = webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub",
                options=options
            ) # Se crea instancia del navegador con la config indicada, Selenium lo maneja

        """ Abre la página a scrapear """
        driver.get(url_player) 

        """ Espera a que cargue la página y exista el elemento con la clase específicada """
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "playerNickname"))
        )

        """ Se obtiene el código html completo de la página, para luego ser analizada con BeautifulSoup """
        html = driver.page_source

        """ Cierra el navegador y libera recursos """
        driver.quit()

        """ Creación objeto BeautifulSoup con el código html obtenido para analizar """
        soup = BeautifulSoup(html, 'html.parser') # html.parser es el parser que usa para interpretar HTML

        """ Búsqueda de elementos específicos en el HTML """
        nickname_tag = soup.find('h1', class_='playerNickname')
        player_realname_div = soup.find('div', class_='playerRealname')
        age_container = soup.find('div', class_='playerInfoRow playerAge')

        nickname = ''
        first_name = ''
        last_name = ''
        age = None
        nationality = ''

        print("nickname_tag:", nickname_tag)
        print("player_realname_div:", player_realname_div)
        print("age_container:", age_container)

        if nickname_tag:
            nickname = nickname_tag.text.strip()

        if age_container:
            age_text = age_container.find('span', itemprop='text')
            if age_text:
                age = int(age_text.text.strip().split()[0])

        if player_realname_div:
            full_name = player_realname_div.get_text(strip=True)
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            flag_img = player_realname_div.find('img', itemprop='nationality')
            if flag_img and 'alt' in flag_img.attrs:
                nationality = flag_img['alt']
        
        if nickname and first_name and last_name and age and nationality:
            type_player = TypePlayerViewSet.get_type_player(self, url_player)

            player, created = Player.objects.update_or_create(
                nickname=nickname,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'nationality': nationality,
                    'type_player_id': type_player['id']
                }
            )
            print({"nickname": player.nickname, "first_name": player.first_name, "last_name": player.last_name, "age": player.age, "nationality": player.nationality, "created": created})
            return Response({
                'nickname': player.nickname,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'age': player.age,
                'nationality': player.nationality,
                'created': created  
            }, status=201 if created else 200)
        
        print("Algo falló en la obtención de datos")

        return Response('Algo falló en la obtención de datos', status=400)
    
    def search_player(self, nickNamePlayer):
        options = Options()
        options.headless = True

        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=options
        )
        driver.get(self.url)

        search_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navsearchinput"))    
        )

        search_input.clear()
        search_input.send_keys(nickNamePlayer)
        search_input.submit()

        current_url = driver.current_url

        if current_url:
            return current_url

        return None

    def get_profile_player(self, nickNamePlayer):
        options = Options()
        options.headless = True
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=options
        )

        try:
            search_url = f"https://www.hltv.org/search?query={nickNamePlayer}"
            driver.get(search_url)
            print("url tabla jugadores", search_url)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table'))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Buscar todas las tablas
            tables = soup.select('table.table')

            player_url = None
            for table in tables:
                header = table.find('td', class_='table-header')
                if header and header.text.strip() == 'Player':
                    # Esta es la tabla que queremos
                    first_link = table.select_one('td a')
                    print("first_link:", first_link)
                    if first_link:
                        base_url = "https://www.hltv.org"
                        player_url = base_url + first_link['href']
                        print("player_url first:", player_url)
                    break  # Ya encontramos la tabla correcta
            
            if player_url:
                print("player_url return:", player_url)
                return player_url
            else:
                print(f"No se encontró el jugador: {nickNamePlayer}")
                return None

        except Exception as e:
            print(f"Error al buscar jugador '{nickNamePlayer}'")
            return None

        finally:
            driver.quit()

    
    @action(detail=False, methods=['get'], url_path='create-player')
    def create_player(self, request):
        nick = request.query_params.get('name')
        print("nick:", nick)
        player_url = self.get_profile_player(nick)
        print("player_url:", player_url)
        if player_url:
            return self.scrape(player_url)
        return Response('No se encontró el jugador', status=404)

class TypePlayerViewSet(viewsets.ModelViewSet):
    queryset = Type_Player.objects.all()
    serializer_class = TypePlayerSerializer

    def get_type_player(self, url_player):
        options = Options()
        options.headless = True
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=options
        )

        driver.get(url_player)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "primaryRole"))    
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        type_player_div = soup.find('div', class_='primaryRole')

        if type_player_div:
            type_player_text = type_player_div.text.strip()

            try:
                type_player = Type_Player.objects.get(type_name=type_player_text)
                print("type_player:", type_player.type_name)
                return {
                    'id': type_player.id,
                    'type_name': type_player.type_name,
                    'description': type_player.description
                }
            except Type_Player.DoesNotExist:
                return None
            
            finally:
                driver.quit()
        return None



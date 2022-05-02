#@title **GarticFinder**
#@markdown Execute e preencha as informações
#criado por @Paperx / github: @Papeeeel
from bs4 import BeautifulSoup
import urllib.request
import json
from termcolor import colored
from urllib import request, parse

print(colored("""
 _____            _   _     ______ _           _            
|  __ \          | | (_)    |  ___(_)         | |           
| |  \/ __ _ _ __| |_ _  ___| |_   _ _ __   __| | ___ _ __  
| | __ / _` | '__| __| |/ __|  _| | | '_ \ / _` |/ _ \ '__| 
| |_\ \ (_| | |  | |_| | (__| |   | | | | | (_| |  __/ |    
 \____/\__,_|_|   \__|_|\___\_|   |_|_| |_|\__,_|\___|_|""", 'blue'))
print()


exit_code = 2
nick = input('Digite o nick do usuario desejado para a busca: ')


def get_cookie():
  url = 'https://gartic.com.br/log_ajax.php'
  data = {'userLogin':'getcookiepublic', 'senhaLogin':'cookie'} #oh voce descobriu a minha senha
  data = parse.urlencode(data).encode()
  req =  request.Request(url, data=data)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0')
  resp = request.urlopen(req)
  cookie = resp.info().get_all('Set-Cookie')
  return cookie[0]

def status_nick(nick):
  if nick[0] == '~':
    return 4
  try:
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(f"https://gartic.com.br/{nick}",None,headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8", 'ignore')
    soup = BeautifulSoup(data, "html.parser")
    resp = soup.find("div", class_="internoConteudo").text
    if "Offline" in resp:
      return 0
    elif "Jogando" in  resp:
      return 1
    elif "Online no site" in resp:
      return 2
  except:
    return 3

def verifica_no_json(url, nick):#verifica se o nick esta dentro do dicionario gerado
    request=urllib.request.Request(url, None)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0')
    response = urllib.request.urlopen(request)
    data = response.read()
    decode = data.decode('UTF-8')
    json_r = json.loads(decode)

    for c in range(len(json_r['jogadores'])):
      json_r['jogadores'][c] = json_r['jogadores'][c].lower()
    
    # print(json_r['nome'],':',*json_r['jogadores'])# deixe comentado se não quiser mostrar as salas e os nicks
    if nick in json_r["jogadores"]:
      print(colored(f'o(a) jogador(a) {nick} está na sala {json_r["nome"]}', 'blue'))
      return True
    else:
      return False

status = status_nick(nick)
cookie_logado = get_cookie()
if status == 1:
  caminho_procura = input("onde deseja procurar? [c=salas criadas, p=salas padrão, t=todas as salas, a=terminar procura: ").lower()
  if caminho_procura != 'a':
    print(f'Procurando {nick}...')
  #requisita as informaçoes das salas 
  request=urllib.request.Request("https://gartic.com.br/lista_sala.php?x=''&l=1",None)
  request.add_header('Cookie', cookie_logado)
  request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0')
  response = urllib.request.urlopen(request)
  data = response.read()
  decode = data.decode('UTF-8')
  json_salas = json.loads(decode)

  #verifica o tipo de caminho escolhido
  if caminho_procura == 'c':
    #busca os ids das salas
    for a in range(len(json_salas[0]["c"])):
      id = json_salas[0]["c"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)#verifica se o nick esta dentro do dicionario gerado

      if status_code:#verifica se foi encontrado o nick escolhido
        break

  elif caminho_procura == 'p':
    for a in range(len(json_salas[0]["o"])):
      id = json_salas[0]["o"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        break

  elif caminho_procura == 't': 

    for a in range(len(json_salas[0]["o"])):
      id = json_salas[0]["o"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        exit_code = 3
        break

    for a in range(len(json_salas[0]["c"])):
      if exit_code == 3:
        break
      id = json_salas[0]["c"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        exit_code = 0
        break

      else:
        exit_code = 1

  elif caminho_procura == 'a':
    pass   

  else:    
    print('escolha uma forma de procura válida!')

  if exit_code == 1:
    print('jogador não encontrado')

elif status == 0:
  print(f'O jogador {nick} está Offline.')

elif status == 2:
  print(f'O jogador {nick} está online no site, porém não está jogando.')

elif status == 3:
  print(f'O jogador {nick} não foi encontrado')


if status == 4:
  caminho_procura = input("onde deseja procurar? [c=salas criadas, p=salas padrão, t=todas as salas, a=terminar procura: ").lower()
  if caminho_procura != 'a':
    print(f'Procurando {nick}...')
  #requisita as informaçoes das salas 
  request=urllib.request.Request("https://gartic.com.br/lista_sala.php?x=''&l=1",None)
  request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0')
  response = urllib.request.urlopen(request)
  data = response.read()
  decode = data.decode('UTF-8')
  json_salas = json.loads(decode)

  #verifica o tipo de caminho escolhido
  if caminho_procura == 'c':
    #busca os ids das salas
    for a in range(len(json_salas[0]["c"])):
      id = json_salas[0]["c"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)#verifica se o nick esta dentro do dicionario gerado

      if status_code:#verifica se foi encontrado o nick escolhido
        break

  elif caminho_procura == 'p':
    for a in range(len(json_salas[0]["o"])):
      id = json_salas[0]["o"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        break

  elif caminho_procura == 't': 

    for a in range(len(json_salas[0]["o"])):
      id = json_salas[0]["o"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        exit_code = 2
        break

    for a in range(len(json_salas[0]["c"])):
      if exit_code == 3:
        break
      id = json_salas[0]["c"][a]["i"]
      url_sala_info = f"https://gartic.com.br/info_sala.php?id_sala={id}"
      status_code = verifica_no_json(url_sala_info, nick)

      if status_code:
        exit_code = 0
        break

      else:
        exit_code = 1

  elif caminho_procura == 'a':
    pass   

  else:    
    print('escolha uma forma de procura válida!')

  if exit_code == 1:
    print('jogador não encontrado')

print('Finalizado.')

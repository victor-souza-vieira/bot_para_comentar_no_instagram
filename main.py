from selenium import webdriver
import time
import random as rand

USER = ''
PASSWORD = ''
WAIT_TIME = 3

def login(navegador):
    navegador.get('https://www.instagram.com/accounts/login/')

    time.sleep(WAIT_TIME)

    user_field = navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    user_field.send_keys(USER)

    time.sleep(WAIT_TIME * rand.randint(1, 5))

    password_field = navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_field.send_keys(PASSWORD)

    time.sleep(WAIT_TIME * rand.randint(1, 5))
    navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()

    return navegador

def link_ultima_postagem(tags):
    for tag in tags:
        tag = tag.get_attribute('href')
        if '/p/' in tag:
            return tag
    return None

def coleta_ultima_postagem(navegador, pessoa):
    navegador.get('https://www.instagram.com/' + pessoa)

    tags_das_postagens = navegador.find_elements_by_tag_name('a')
    link_last_post = link_ultima_postagem(tags_das_postagens)
    
    return navegador, link_last_post

def carrega_lista_de_pessoas_e_comentarios(path):
    arquivo = open(path, 'r')

    pessoas_comentario = []

    for line in arquivo:
        pessoas_comentario.append(line.replace('\n', '').split(';'))

    return pessoas_comentario

def atualiza_link_ultima_postagem_arquivo_pessoas(path, pessoas):
    arquivo = open(path, 'w')
    for pessoa in pessoas:
        arquivo.write(pessoa[0]+';'+pessoa[1]+';'+pessoa[2]+'\n')
    arquivo.close()

def publica_comentario(navegador, pessoa):
    navegador.get(pessoa[2])
    time.sleep(WAIT_TIME)

    comment_field = navegador.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea').click()
    time.sleep(WAIT_TIME)

    comment_field = navegador.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/textarea')
    comment_field.clear()

    for letra in pessoa[1]:
        comment_field.send_keys(letra)
        time.sleep(rand.randint(1, 10)/30)

    time.sleep(WAIT_TIME)
    navegador.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[3]/div/form/button[2]').click()
    time.sleep(WAIT_TIME * rand.randint(1, 5))

if __name__ == '__main__':
    navegador = webdriver.Chrome()
    navegador = login(navegador)
    pessoas = carrega_lista_de_pessoas_e_comentarios('pessoas.csv')
    while True:
        try:
            for pessoa in pessoas:
                time.sleep(WAIT_TIME * rand.randint(1, 5))
                navegador, postagem = coleta_ultima_postagem(navegador, pessoa[0])
                if pessoa[2] != postagem:
                    pessoa[2] = postagem
                    pessoa.append('postagem nova')
                else:
                    pessoa.append('sem postagem nova')
        
            for pessoa in pessoas:
                if 'sem postagem nova' in pessoa[3]:
                    continue
                else:
                    time.sleep(WAIT_TIME * rand.randint(1, 5))
                    publica_comentario(navegador, pessoa)
            
            atualiza_link_ultima_postagem_arquivo_pessoas('pessoas.csv', pessoas)
        except:
            pass
        time.sleep(300 * rand.randint(1, 3) + rand.randint(-100, 100))
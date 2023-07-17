from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import os
import time

from sqlalchemy import between


def recorrer_publicaciones_empresa(cant):
    try:
        print("Obteniendo las publicaciones de {} \n".format(nombre_pagina))
        time.sleep(2)
        todas_publicaciones = driver.find_elements(By.CSS_SELECTOR, "div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
        intentos = 0
        while len(todas_publicaciones) < cant:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            todas_publicaciones = driver.find_elements(By.CSS_SELECTOR, "div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
            if intentos == 3:
                cant = len(todas_publicaciones)
                break
            else:
                intentos += 1
        elem_publ = [""] * cant
        lista_url_imagenes = []
        num_imagen = 1
        for contador in range(cant):        
            try:
                contenido = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[data-ad-comet-preview="message"]').text #publicacion sin traducir
            except:
                try:
                    contenido = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m"]').text #Traducida automaticamente por la página
                except:
                    contenido = "Contenido no disponible" 
            try:
                fecha = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'a[class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]').text
            except:
                break #Siempre habrá fecha si existe la publicación
            try:
                comentarios = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[class="oajrlxb2 gs1a9yip mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o tgvbjcpo hpfvmrgz esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl dwo3fsh8 g5ia77u1 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv gmql0nx0 kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h du4w35lb gpro0wi8"]').text
            except:
                comentarios = "0 comentarios"
            try:
                reacciones = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'span[class="pcp91wgn"]').text + " reacciones"
            except:
                reacciones = "0 reacciones"
            try:
                todas_imagenes = todas_publicaciones[contador].find_elements(By.CSS_SELECTOR, 'img[class="i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm"]') #Clase conjunto imagenes
                str_imagen = " --- "
                if len(todas_imagenes) == 0:
                    imagen = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'img[class="i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6"]') #clase imagen única
                else:
                    imagen = todas_imagenes[0]
                lista_url_imagenes.append(imagen.get_attribute('src')) #Obtenemos la direccion de la imagen para descargarla luego
                str_imagen = str_imagen + "imagen" + str(num_imagen) + " --- "
                num_imagen = num_imagen + 1
                for cont_imagenes in range(1, len(todas_imagenes)):
                    imagen = todas_imagenes[cont_imagenes]
                    lista_url_imagenes.append(imagen.get_attribute('src'))
                    str_imagen = str_imagen + "imagen" + str(num_imagen) + " --- "
                    num_imagen = num_imagen + 1
            except:
                imagen = "No hay imagen"
            elem_publ[contador] = list((contenido, fecha, comentarios, reacciones, str_imagen))
    except:
        return elem_publ
    print("Publicaciones obtenidas.\n")
    print("Empezando la descarga de las imagenes obtenidas.\n")
    obtener_imagenes(lista_url_imagenes)
    print("Descarga de imagenes finalizada\n")
    return elem_publ

def recorrer_publicaciones_persona(cant):
    try:
        print("Obteniendo las publicaciones de {} \n".format(nombre_pagina))
        time.sleep(2)
        todas_publicaciones = driver.find_elements(By.CSS_SELECTOR, "div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
        intentos = 0
        while len(todas_publicaciones) < cant:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            todas_publicaciones = driver.find_elements(By.CSS_SELECTOR, "div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
            if intentos == 3:
                cant = len(todas_publicaciones)
                break
            else:
                intentos += 1
        elem_publ = [""] * cant
        lista_url_imagenes = []
        num_imagen = 1
        print("Inicio de la obtención de las publicaciones\n")
        for contador in range(cant):
            try:
                if perfil_nuestro:
                    contenido = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]').text 
                else:
                    try:
                        contenido = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[data-ad-comet-preview="message"]').text #publicacion sin traducir
                    except:
                        contenido = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q"]').text #Traducida automaticamente por la página
            except:
                contenido = "Sin descripción"
            try:
                fecha = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'a[class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]').text
            except:
                break #Siempre habrá fecha si existe la publicación
            try:
                comentarios = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'div[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw m9osqain"]').text
            except:
                comentarios = "0 comentarios"
            try:
                reacciones = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'span[class="pcp91wgn"]').text + " reacciones"
            except:
                reacciones = "0 reacciones"
            try:
                todas_imagenes = todas_publicaciones[contador].find_elements(By.CSS_SELECTOR, 'img[class="i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm"]') #Clase conjunto imagenes
                str_imagen = " --- "
                if len(todas_imagenes) == 0:
                    imagen = todas_publicaciones[contador].find_element(By.CSS_SELECTOR, 'img[class="i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6"]') #clase imagen única
                else:
                    imagen = todas_imagenes[0]
                lista_url_imagenes.append(imagen.get_attribute('src')) #Obtenemos la direccion de la imagen para descargarla luego
                str_imagen = str_imagen + "imagen" + str(num_imagen) + " --- "
                num_imagen = num_imagen + 1
                for cont_imagenes in range(1, len(todas_imagenes)):
                    imagen = todas_imagenes[cont_imagenes]
                    lista_url_imagenes.append(imagen.get_attribute('src'))
                    str_imagen = str_imagen + "imagen" + str(num_imagen) + " --- "
                    num_imagen = num_imagen + 1
            except:
                imagen = "No hay imagen"
            if(imagen == " --- "):
                imagen = "No hay imagen"
            elem_publ[contador] = list((contenido, fecha, comentarios, reacciones, str_imagen))
    except:
        return elem_publ
    print("Publicaciones obtenidas.\n")
    print("Empezando la descarga de las imagenes obtenidas.\n")
    obtener_imagenes(lista_url_imagenes)
    print("Descarga de imagenes finalizada\n")
    return elem_publ


def escritura_fichero(tipo): # 0 --> Persona,  1 --> Empresa
    print("Comienzo de la extracción.\n")
    with open(nombre_pagina, "w") as f:
        f.write("A continuación aparecerá los datos del usuario {}".format(nombre_pagina))
        f.write("\n\n\n\n")
        f.write("Primero un poco de información de la página: \n\n")
        lista_info = informacion_pagina(tipo);
        if(len(lista_info) == 0):
            f.write("Sin información adicional disponible \n")
        else:
            for info in lista_info:
                f.write(info + "\n")
        f.write("\n\n\n\n")
        f.write("Ahora obtendremos las últimas publicaciones de este usuario: \n\n")
        if tipo == 0:
            publicaciones = recorrer_publicaciones_persona(cant)
        else:
            publicaciones = recorrer_publicaciones_empresa(cant)
        for index in range(len(publicaciones)):
            if(publicaciones[index] == ""):
                break
            if(publicaciones[index][0] == ""):
                f.write("Contenido: El autor no ha introducido texto o este se encuentra en un idioma distinto al Español\n")
            else:
                f.write("Contenido: " + publicaciones[index][0] + "\n")
            f.write("Fecha de publicación: " + publicaciones[index][1] + "\n")
            f.write("Cantidad de comentarios: " + publicaciones[index][2] + "\n")
            f.write("Cantidad de reacciones: " + publicaciones[index][3] + "\n")
            f.write("Imagenes: " + publicaciones[index][4] + "\n\n")
    #driver.close()

    
def inicio_sesion(user, passw):
    #Inicio sesion
    #Con CSS_SELECTOR busca un elemento button cuyo titulo sea el que le pasamos
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    time.sleep(2)
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    time.sleep(2)
    submit   = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login']")))

    username.clear()
    username.send_keys(user)
    password.clear()
    password.send_keys(passw)
    submit.click()

def obtener_imagenes(lista_url):
    path = os.getcwd()
    path = path + "/" + nombre_pagina + "_imagenes"
    try:
        os.mkdir(path, 0o777)
    except:
        pass
    num_imagen = 1
    for url in lista_url:
        driver.get(url)
        driver.save_screenshot(path+"/imagen{}.png".format(num_imagen))
        num_imagen += 1
        time.sleep(2)
#Setup webdriver


def informacion_pagina(tipo_pag):
    lista_info = []
    try:
        seccion_informacion = driver.find_elements(By.CSS_SELECTOR, 'div[class="j83agx80 l9j0dhe7 k4urcfbm"]')[0]
        if(perfil_nuestro):
            seccion_informacion = driver.find_elements(By.CSS_SELECTOR, 'div[class="j83agx80 l9j0dhe7 k4urcfbm"]')[1]
        if tipo_pag == 0:            
            secciones = seccion_informacion.find_elements(By.CSS_SELECTOR, 'div[class="rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw i1fnvgqd gs1a9yip owycx6da btwxx1t3 hv4rvrfc dati1w0a discj3wi b5q2rw42 lq239pai mysgfdmx hddg9phg"]')
            for seccion in secciones:
                lista_info.append(seccion.text)
        else:
            secciones = seccion_informacion.find_elements(By.CSS_SELECTOR, 'div[class="taijpn5t cbu4d94t j83agx80"]')
            for seccion in secciones:
                lista_info.append(seccion.text)
    except:
        return lista_info
    return lista_info


if __name__ == "__main__":
    path = os.getcwd()
    gecko_location = path + "/geckodriver"
    s = Service(gecko_location)
    driver = webdriver.Firefox(service=s)
    driver.implicitly_wait(10)


    driver.get('https://www.facebook.com')
    driver.implicitly_wait(10)
    cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Allow essential and optional cookies']"))).click()
    #Con esto apretamos el botón de aceptar cookies

    while True:
        usuario = input("Correo: ")
        password = getpass("Contraseña: ") #Función importada para que no muestre la contraseña por consola al introducirla
        inicio_sesion(usuario, password)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[id="loginbutton"]')
            print("Inicio de sesión fallido\n")
            driver.get('https://www.facebook.com')
        except:
            break

    respuesta = input("\nQuieres buscar información de tu cuenta? (S/N): ")
    while True:
        if respuesta == "S":
            perfil_nuestro = True
            break
        elif respuesta == "N":
            perfil_nuestro = False
            break
        else:
            respuesta = input("Respuesta no válida. Si desea buscar en su página introduzca S, si quiere de otra ajena introduza N: \n")
                        
    if not perfil_nuestro:
        while True:
            try:
                pagina_ajena = input("Introduzca la url entera de la página: ")
                driver.get(pagina_ajena)
                try:
                    driver.find_element(By.CSS_SELECTOR, 'div[class="qublvx3c oh7imozk cbu4d94t j83agx80 bp9cbjyn"]').find_element(By.CSS_SELECTOR, 'img[class="hu5pjgll"]')
                    print("La url introducida no existe, asegurese de haberla copiado bien\n")
                except:
                    break
            except:
                print("La página debe estar dentro de Facebook, cualquier url fuera de esta es inválida\n")

    else:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/me/']"))).click()

    cant = input("\nIndique la cantidad de publicaciones desea obtener (1-7). Recuerde que cuantas más publicaciones, mayor será el tiempo de ejecución de la aplicación: ")
    while True:
        cant = int(cant)
        if cant in range(1, 8):
            break
        else:
            cant = input("Número incorrecto, vuelva a introducirlo: ")
    print("\nDatos iniciales correctos.\n")

    time.sleep(3)
    tipo_pag = 0 #Diferencia entre tipos de páginas
    try:
        nombre_pagina = driver.find_element(By.CSS_SELECTOR, 'span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 qg6bub1s teo7jy3c mhxlubs3 p5u9llcw hnhda86s oo9gr5id hzawbc8m"]').text #El nombre de la página que hemos buscado
    except:
        try:
            nombre_pagina = driver.find_element(By.CSS_SELECTOR, 'h2[class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"]').text #El nombre de la página puede ser largo
        except:
            nombre_pagina = driver.find_element(By.CSS_SELECTOR, 'span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em h6olsfn3 m6dqt4wy h7mekvxk hnhda86s oo9gr5id hzawbc8m"]').text
            tipo_pag = 1

    #print(driver.find_element(By.CSS_SELECTOR, 'h1[class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl"]').text)
    url = driver.current_url

    escritura_fichero(tipo_pag)
    print("Programa finalizado")


    # 1 min --> < 30 seg
    # 7 max --> < 2:30 min
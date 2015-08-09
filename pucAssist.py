from requests import session
from re import findall, DOTALL


def applyRE(tx):
    """ Expresion regular que obtiene los valores ocultos en 
    el formulario de login, ya que estos deben enviarse en el
    POST que se hace para ingresar al portal """
    return findall(
        '<input type="hidden" name=".*?" value="([^"]*)" \/>',
        tx,
        DOTALL
    )


def dict_form(hidden_input_values, user, secret):
    """ Este diccionario contiene los parametros que deben 
    ser enviados en el POST para validar las credenciales antes
    de ingresar al portal """
    return {
        'action': 'login',
        'username': user,
        'password': secret,
        'lt': hidden_input_values[0],
        'execution': hidden_input_values[1],
        '_eventId': hidden_input_values[2]
    }


def Chequear_credenciales(user, secret):
    """ Dado un usuario y su clave se simula un ingreso al portal y
    se verifica si fue un ingreso exitoso o no """
    with session() as c:
        # Veo el login
        miro_el_formulario = c.get(
            'https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login')
        # y obtengo los valores ocultos del formulario
        HIV = applyRE(miro_el_formulario.text)

        # Pruebo la llave
        llave = c.post('https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login',
                       data=dict_form(HIV, user, secret))
        if llave.url == 'https://portal.uc.cl/web/home-community/inicio':
            return True
    # Ante cualquier error de conexion o de credenciales se retorna False
    return False


def Obtener_notas(user, secret):
    """ Dado un usuario y su clave se ingresa al portal y se sigue
    la ruta hasta la Ficha Academica Acumulada, la cual se retorna 
    en forma de texto html """
    with session() as c:
        # Veo el login
        miro_el_formulario = c.get(
            'https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login')
        # y obtengo los valores ocultos del formulario
        HIV = applyRE(miro_el_formulario.text)

        # Mando mis credenciales para ingresar al portal
        llave = c.post('https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login',
                       data=dict_form(HID, user, secret))
        # y reviso si pude ingresar
        if llave.url != 'https://portal.uc.cl/web/home-community/inicio':
            return None

        # > Info academica del portal
        voy_a_la_info_academica = c.get(
            'https://portal.uc.cl/web/home-community/informacion-academica?gpi=10225')

        # > Siguiendole la pista a banner
        banner_maldito = c.get(
            'https://portal.uc.cl/luminis-banner/lp5Banner?externalsystem=SSB&url=urlPathbwskotrn.P_ViewTermTran')

        # > Vamos por las notas
        dame_mis_notas = c.post(
            'https://ssb.uc.cl/ERPUC/bwskotrn.P_ViewTran', data={'tprt': 'FAA'})

        # Retorna el texto en html de la Ficha Academica Acumulada
        return dame_mis_notas
    # Ante cualquier error de conexion o de credenciales se retorna None
    return None
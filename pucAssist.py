from requests import session

URL_LOGIN = "https://ssb.uc.cl/ERPUC/twbkwbis.P_ValLogin"
URL_NOTAS = "https://ssb.uc.cl/ERPUC/bwskotrn.P_ViewTran"

def Obtener_notas(user, secret):
    """ Dado un usuario y su clave se ingresa a la plataforma y se sigue
    la ruta hasta la Ficha Academica Acumulada, la cual se retorna 
    en forma de texto html """
    with session() as SESSION:

        SESSION.get(URL_LOGIN)

        login = SESSION.post(URL_LOGIN,
                         params={'sid': user, 'PIN': secret})

        notas = SESSION.post(URL_NOTAS,
                         data={'tprt': 'FAA'})

        return notas
    # Ante cualquier error de conexion o de credenciales se retorna None
    return None
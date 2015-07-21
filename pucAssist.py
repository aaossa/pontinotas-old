from requests import session
import re


def applyRE(tx):
    return re.findall(
        '<input type="hidden" name=".*?" value="([^"]*)" \/>',
        tx,
        re.DOTALL
    )


def dict_form(hidden_input_values, user, secret):
    return {
        'action': 'login',
        'username': user,
        'password': secret,
        'lt': hidden_input_values[0],
        'execution': hidden_input_values[1],
        '_eventId': hidden_input_values[2]
    }


def Chequear_credenciales(user, secret):
    with session() as c:
        # Veo el login
        miro_el_formulario = c.get(
            'https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login')
        HID = applyRE(miro_el_formulario.text)
        # Pruebo la llave
        llave = c.post('https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login',
                       data=dict_form(HID, user, secret))
        if llave.url == 'https://portal.uc.cl/web/home-community/inicio':
            return True
    return False


def Obtener_notas(user, secret):
    with session() as c:
        # Veo el login
        miro_el_formulario = c.get(
            'https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login')
        HID = applyRE(miro_el_formulario.text)

        # Mando mis credenciales
        llave = c.post('https://sso.uc.cl/cas/login?service=https://portal.uc.cl/c/portal/login',
                       data=dict_form(HID, user, secret))

        # Pruebo la llave
        if llave.url != 'https://portal.uc.cl/web/home-community/inicio':
            return None

        # Info academica del portal
        voy_a_la_info_academica = c.get(
            'https://portal.uc.cl/web/home-community/informacion-academica?gpi=10225')

        # Siguiendole la pista a banner
        banner_maldito = c.get(
            'https://portal.uc.cl/luminis-banner/lp5Banner?externalsystem=SSB&url=urlPathbwskotrn.P_ViewTermTran')

        # Vamos por las notas
        dame_mis_notas = c.post(
            'https://ssb.uc.cl/ERPUC/bwskotrn.P_ViewTran', data={'tprt': 'FAA'})

        return dame_mis_notas
    return None

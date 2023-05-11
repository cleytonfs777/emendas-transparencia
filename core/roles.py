from rolepermissions.roles import AbstractUserRole


class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_disparador': True,
        'listar_disparador': True,
        'cadastrar_recursos': True,
        'disparar_mensagem': True,
    }
    
class Disparador(AbstractUserRole):
    available_permissions = {
        'disparar_mensagem': True,
    }
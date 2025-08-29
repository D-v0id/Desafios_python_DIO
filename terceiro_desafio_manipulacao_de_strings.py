email = input().strip()

# TODO: Verifique as regras do e-mail:
def validar_email(email):
    if ' ' in email:
        return False
    
    if email.startswith('@') or email.endswith('@'):
        return False
    
    if '@' not in email:
        return False
    
    partes = email.split('@')
    if len(partes) != 2:  # Deve ter exatamente 2 partes: usuário e domínio
        return False
    
    usuario, dominio = partes
    
    if '.' not in dominio or dominio.startswith('.') or dominio.endswith('.'):
        return False
    
    return True

# Verifica o e-mail e imprime o resultado
if validar_email(email):
    print("E-mail válido")
else:
    print("E-mail inválido")
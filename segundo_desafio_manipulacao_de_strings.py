import sys

def main():
    descontos = {"DESCONTO10": 0.10, "DESCONTO20": 0.20, "SEM_DESCONTO": 0.00}
    
    # Para teste local (comente para a plataforma)
    print("Digite o preço: ", end="", flush=True)
    preco = float(sys.stdin.readline().strip())
    
    print("Digite o cupom: ", end="", flush=True)
    cupom = sys.stdin.readline().strip().upper()
    
    # Para plataforma (descomente para enviar)
    # preco = float(sys.stdin.readline().strip())
    # cupom = sys.stdin.readline().strip().upper()
    
    if cupom in descontos:
        preco_final = preco * (1 - descontos[cupom])
        print(f"{preco_final:.2f}")
    else:
        print(f"{preco:.2f}")

if __name__ == "__main__":
    main()
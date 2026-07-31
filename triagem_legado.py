# triagem_legado.py - CÓDIGO LEGADO (MONOLÍTICO)
# IMPORTANTE: Este script funciona, mas é difícil de manter e impossível de testar.

print("=== SISTEMA DE TRIAGEM DE CHAMADOS (V1 LEGADO) ===")

cliente_nome = input("Digite o nome do cliente: ")
cliente_email = input("Digite o e-mail do cliente: ")
mensagem = input("Descreva o problema: ")
urgencia_input = input("Urgência (1-Baixa, 2-Média, 3-Alta): ")

# Validação e processamento da urgência
if urgencia_input == "1":
    urgencia_label = "BAIXA"
    prazo_horas = 72
elif urgencia_input == "2":
    urgencia_label = "MÉDIA"
    prazo_horas = 24
elif urgencia_input == "3":
    urgencia_label = "ALTA"
    prazo_horas = 4
else:
    print("ERRO: Opção de urgência inválida! Definindo como BAIXA por padrão.")
    urgencia_label = "BAIXA"
    prazo_horas = 72

# Identificação simples de categoria por palavra-chave
mensagem_lc = mensagem.lower()
if "senha" in mensagem_lc or "login" in mensagem_lc or "acesso" in mensagem_lc:
    categoria = "AUTENTICACAO"
    departamento = "SUPORTE_TI"
elif "fatura" in mensagem_lc or "pagamento" in mensagem_lc or "cartao" in mensagem_lc:
    categoria = "FINANCEIRO"
    departamento = "FINANCEIRO_ATENDIMENTO"
elif "bug" in mensagem_lc or "erro" in mensagem_lc or "falha" in mensagem_lc:
    categoria = "SISTEMA"
    departamento = "ENGENHARIA"
else:
    categoria = "GERAL"
    departamento = "TRIAGEM_HUMANA"

# Formatação da saída para salvar no log
ticket_id = "TCK-" + str(hash(cliente_email + mensagem))[-6:]
log_ticket = f"[{ticket_id}] CLIENTE: {cliente_nome} ({cliente_email}) | DEPT: {departamento} | CAT: {categoria} | URG: {urgencia_label} | PRAZO: {prazo_horas}h"

print("\n--- TICKET GERADO COM SUCESSO ---")
print(log_ticket)

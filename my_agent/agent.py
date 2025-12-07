import sys
import os
import json
from google.adk.agents.llm_agent import Agent

def getCompany() -> dict:
    """
    Acessa o arquivo empresa_dados.json e retorna seu conteúdo.
    Use esta função para obter dados brutos para cálculos e respostas.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), 'empresa_dados.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        return {"erro": "Arquivo empresa_dados.json não encontrado."}

def compare_benchmark() -> dict:
    """
    Compara os indicadores da empresa com o benchmark de mercado.
    Retorna um comparativo de Liquidez Corrente e Margem Líquida.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    benchmark_path = os.path.join(parent_dir, 'benchmark.json')
    try:
        with open(benchmark_path, 'r', encoding='utf-8') as f:
            benchmark_data = json.load(f)
    except FileNotFoundError:
        return {"erro": "Arquivo benchmark.json não encontrado."}
            
    empresas = benchmark_data.get('benchmark_empresas_similares', [])

    total_liq = 0
    total_margem = 0
    count = len(empresas)
    
    for emp in empresas:
        indicadores = emp.get('indicadores_financeiros', {})
        total_liq += indicadores.get('liquidez_corrente', 0)
        total_margem += indicadores.get('margem_liquida', 0)
        
    media_liq = total_liq / count if count > 0 else 0
    media_margem = total_margem / count if count > 0 else 0

    empresa_path = os.path.join(parent_dir, 'empresa_dados.json')
    try:
        with open(empresa_path, 'r', encoding='utf-8') as f:
            empresa_data = json.load(f)
    except FileNotFoundError:
        return {"erro": "Arquivo empresa_dados.json não encontrado."}

    try:
        fin = empresa_data['cliente_analisado']['dados_financeiros']['demonstracoes']
        ativo_circ = fin['balanco_patrimonial']['ativo_circulante']
        passivo_circ = fin['balanco_patrimonial']['passivo_circulante']
        lucro_liq = fin['dre']['lucro_liquido']
        receita_liq = fin['dre']['receita_liquida']
        
        empresa_liq = ativo_circ / passivo_circ if passivo_circ else 0
        empresa_margem = lucro_liq / receita_liq if receita_liq else 0
    except KeyError:
        return {"erro": "Dados financeiros incompletos no arquivo da empresa."}
    
    return {
        "liquidez_corrente": {
            "empresa": round(empresa_liq, 4),
            "media_mercado": round(media_liq, 4),
            "status": "Acima da média" if empresa_liq > media_liq else "Abaixo da média"
        },
        "margem_liquida": {
            "empresa": round(empresa_margem, 4),
            "media_mercado": round(media_margem, 4),
            "status": "Acima da média" if empresa_margem > media_margem else "Abaixo da média"
        }
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Agente especialista em análise de crédito e dados financeiros.",
    instruction="Você é um assistente financeiro. Use 'getCompany' para ler os dados do cliente e 'compare_benchmark' para comparar com o mercado.",
    tools=[getCompany, compare_benchmark],
)

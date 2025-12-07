import os
import sys
import json
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

try:
    import analise_credito
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        import analise_credito
    except ImportError:
        print("Erro: Não foi possível importar 'analise_credito.py'.")
        sys.exit(1)

@tool
def getFinancial():
    """
    Calcula e retorna os indicadores financeiros (liquidez corrente e margem líquida)
    do cliente analisado, utilizando a lógica definida em analise_credito.py.
    """
    cliente = analise_credito.cliente
    
    liq_corr = cliente.dados_financeiros.demonstracoes.balanco_patrimonial.liquidez_corrente()
    marg_liq = cliente.dados_financeiros.demonstracoes.dre.margem_liquida()
    
    return {
        "id_cliente": cliente.id_cliente,
        "liquidez_corrente": round(liq_corr, 4),
        "margem_liquida": round(marg_liq, 4),
        "ano_referencia": cliente.dados_financeiros.ano_referencia
    }

@tool
def getData():
    """
    Retorna o dicionário completo de dados brutos carregados do arquivo empresa_dados.json.
    Útil para consultar campos específicos que não estão nos indicadores calculados.
    """
    return analise_credito.dados

@tool
def compare_benchmark():
    """
    Compara os indicadores financeiros da empresa atual com a média do mercado (benchmark).
    Lê o arquivo benchmark.json e calcula a média dos indicadores das empresas similares.
    Retorna um comparativo de Liquidez Corrente e Margem Líquida.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    benchmark_path = os.path.join(script_dir, 'benchmark.json')
    
    try:
        with open(benchmark_path, 'r', encoding='utf-8') as f:
            benchmark_data = json.load(f)
    except FileNotFoundError:
        return {"erro": "Arquivo benchmark.json não encontrado."}
            
    empresas = benchmark_data.get('benchmark_empresas_similares', [])
    
    if not empresas:
        return {"erro": "Nenhuma empresa encontrada no benchmark."}

    total_liq = 0
    total_margem = 0
    count = len(empresas)
    
    for emp in empresas:
        indicadores = emp.get('indicadores_financeiros', {})
        total_liq += indicadores.get('liquidez_corrente', 0)
        total_margem += indicadores.get('margem_liquida', 0)
        
    media_liq = total_liq / count if count > 0 else 0
    media_margem = total_margem / count if count > 0 else 0

    cliente = analise_credito.cliente
    empresa_liq = cliente.dados_financeiros.demonstracoes.balanco_patrimonial.liquidez_corrente()
    empresa_margem = cliente.dados_financeiros.demonstracoes.dre.margem_liquida()
    
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

@tool
def gerar_relatorio_pdf(texto_relatorio: str):
    """
    Gera um arquivo PDF com o relatório de análise de crédito.
    Recebe o texto completo do relatório e salva como 'relatorio_analise_credito.pdf'.
    Retorna o caminho do arquivo gerado.
    """
    filename = "relatorio_analise_credito.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de Análise de Crédito")
    
    c.setFont("Helvetica", 12)
    y_position = height - 80
    
    lines = texto_relatorio.split('\n')
    for line in lines:
        words = line.split(' ')
        current_line = ""
        for word in words:
            if c.stringWidth(current_line + " " + word, "Helvetica", 12) < (width - 100):
                current_line += " " + word
            else:
                c.drawString(50, y_position, current_line)
                y_position -= 15
                current_line = word
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 50
        
        if current_line:
            c.drawString(50, y_position, current_line)
            y_position -= 15
            
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
            
    c.save()
    return f"Relatório PDF gerado com sucesso: {os.path.abspath(filename)}"

def main():
    if "GROQ_API_KEY" not in os.environ:
        print("Aviso: A variável de ambiente GROQ_API_KEY não está definida.")

    llm = ChatGroq(
        temperature=0,
        model_name="openai/gpt-oss-120b"
    )

    tools = [getFinancial, getData, compare_benchmark, gerar_relatorio_pdf]

    system_prompt = (
        "Você é um analista de crédito experiente. "
        "Você tem acesso a dados financeiros de uma empresa através de ferramentas. "
        "Use 'getFinancial' para ver a saúde financeira básica. "
        "Use 'getData' se precisar de detalhes específicos do balanço ou DRE que não estão nos indicadores. "
        "Use 'compare_benchmark' para ver como a empresa se sai em relação aos concorrentes. "
        "Use 'gerar_relatorio_pdf' para criar um arquivo PDF com o parecer final da análise. "
        "Responda de forma clara e profissional."
    )

    agent_graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    print("\n--- Agente de Análise de Crédito (LangChain + Groq) ---")
    print("Digite 'sair' para encerrar.")
    
    while True:
        user_input = input("\nPergunta: ")
        if user_input.lower() in ['sair', 'exit', 'quit']:
            break
            
        try:
            messages = [HumanMessage(content=user_input)]

            result = agent_graph.invoke({"messages": messages})

            last_message = result["messages"][-1]
            print(f"\nResposta: {last_message.content}")
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

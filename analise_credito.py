from dataclasses import dataclass
from typing import Optional, List
import json

with open('empresa_dados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

@dataclass
class BalancoPatrimonial:
    ativo_circulante: float
    ativo_nao_circulante: float
    passivo_circulante: float
    passivo_nao_circulante: float
    patrimonio_liquido: float
    ativo_total: float
    passivo_total: float
    
    def liquidez_corrente(self):
        return self.ativo_circulante / self.passivo_circulante
        
    def endividamento(self):
        return self.passivo_total / self.ativo_total
        
@dataclass    
class Dre:
    receita_liquida: float
    custo_mercadorias_vendidas: float
    despesas_operacionais: float
    despesas_financeiras: float
    outras_receitas_despesas: float
    lucro_liquido: float
    
    def margem_liquida(self):
        return self.lucro_liquido/self.receita_liquida
    
    #def margem_operacional(self):
        
    
@dataclass
class Demonstracoes:
    balanco_patrimonial: BalancoPatrimonial
    dre: Dre

@dataclass
class DadosFinanceiros:
    ano_referencia: int
    demonstracoes: Demonstracoes

@dataclass
class ClienteAnalisado:
    id_cliente: str
    dados_financeiros: DadosFinanceiros
    
def partse_balance(d):
    return BalancoPatrimonial(**d)

def parse_dre(d):
    return Dre(**d)

def partse_statements(d):
    return Demonstracoes(
        balanco_patrimonial=partse_balance(d["balanco_patrimonial"]),
        dre=parse_dre(d["dre"])
    )


def partse_financial(d):
    return DadosFinanceiros(
        ano_referencia=d["ano_referencia"],
        demonstracoes=partse_statements(d["demonstracoes"])
    )

def partse_client(d):
    return ClienteAnalisado(
        id_cliente=d["id_cliente"],
        dados_financeiros=partse_financial(d["dados_financeiros"])
    )


cliente = partse_client(dados['cliente_analisado'])
liq_corr = cliente.dados_financeiros.demonstracoes.balanco_patrimonial.liquidez_corrente()
marg_liq = cliente.dados_financeiros.demonstracoes.dre.margem_liquida()

print (f"Liquidez corrente: {liq_corr:.4f}")
print (f"Margem liquida: {marg_liq:.4f}")
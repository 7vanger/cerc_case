from dataclasses import dataclass
from typing import Optional, List
import json

with open('empresas_dados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print (dados)

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
        self.ativo_circulante / self.ativo_nao_circulante
        
    def endividamento(self):
        self.passivo_total / self.ativo_total
    
class dre:
    receita_liquida: float
    custo_mercadorias_vendidas: float
    despesas_operacionais: float
    despesas_financeiras: float
    outras_receitas_despesas: float
    lucro_liquido: float
    
    def margem_liquida(self):
        self.lucro_liquido/self.receita_liquida
    
    def margem_operacional(self):
        
    
@dataclass
class Demonstracoes:
    balanco_patrimonial: BalancoPatrimonial
    dre: dre

@dataclass
class DadosFinanceiro:
    ano_referencia: int
    demonstracoes: Demonstracoes

@dataclass
class ClienteAnalisado:
    dados_financeiros: DadosFinanceiro


cliente = parse_cliente(dados['cliente_analisado'])
indice = 
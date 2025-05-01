import json
import re

class SintegraGoiasRetorno:
    def __init__(self, html_site):
        self.html_site = html_site

    def tratar_dados(self):
        retorno_formatado = {
            'cnpj': self.getLabelText('CNPJ'),
            'inscricao_estadual': self.getLabelText('Inscrição Estadual'),
            'cadastro_atualizado_em': self.getLabelText('Cadastro Atualizado em'),
            'nome_empresarial': self.getLabelText('Nome Empresarial'),
            'contribuinte': self.getLabelText('Contribuinte?'),
            'nome_propriedade': self.getLabelText('Nome da Propriedade:'),
            'nome_fantasia': self.getLabelText('Nome Fantasia'),
            'endereco_estabelecimento': self.getLabelText('Endereço Estabelecimento ', 'div'),
            'atividade_principal': self.getAtividadePrincipal(),
            'atividade_secundaria': self.getAtividadesSecundarias(),
            'informacoes_complementares': {
                'unidade_auxiliar': self.getLabelText('Unidade Auxiliar:'),
                'condicao_uso': self.getLabelText('Condição de Uso:'),
                'data_final_contrato': self.getLabelText('Data Final de Contrato:'),
                'regime_apuracao': self.getLabelText('Regime de Apuração:'),
                'situacao_cadastral_vigente': self.getLabelText('Situação Cadastral Vigente:'),
                'data_desta_situacao_cadastral': self.getLabelText('Data desta Situação Cadastral:'),
                'data_cadastramento': self.getLabelText('Data de Cadastramento:'),
                'operacao_nfe': self.getLabelText('Operações com NF-E:')
            }
        }
        return retorno_formatado

    def getLabelText(self, nm_busca, html_busca='span'):
        elemento = self.html_site.find(html_busca, text=nm_busca)
        if elemento:
            proximo = elemento.find_next('span', class_='label_text')
            if proximo:
                return proximo.text.strip()
        return ""

    def getAtividadePrincipal(self):
        elemento = self.html_site.find('strong', string="Atividade Principal")
        if elemento:
            proximo = elemento.find_parent().find_next_sibling('span', class_='label_text')
            if proximo:
                return proximo.text.strip()
        return ""

    def getAtividadesSecundarias(self):
        elemento = self.html_site.find('strong', string="Atividade Secundária")
        if not elemento:
            return []
        atividades = []
        for span in elemento.find_parent().find_all_next('span', class_='label_text'):
            texto = span.text.strip()
            if re.match(r'^\d{7} -', texto):
                atividades.append(texto)
        return atividades

    def to_json(self):
        data = {
            "status_task": "processed",
            "processed_data": self.tratar_dados()
        }
        return json.dumps(data, indent=4)


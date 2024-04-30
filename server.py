import cherrypy
import subprocess

class ImpressoraController(object):
    servidor_impressora = r'\\192.0.1.61'  # Defina o servidor da impressora aqui

    # Dicionário com os nomes das impressoras e seus respectivos nomes
    impressoras = {
        "PL CSC ADM": "\csc-adm-preto-sp5200s",
        "Comercial": "\csc-comercial-preto-sp5200s",
        "Marketing": "\csc-mkt-preto-c368",
        "Exportação": "\csc-exportacao-preto-sp377sf",
        "Financeiro": "\csc-financeiro-1102w"
    }
    
    @cherrypy.expose
    def index(self):
        # Lê o conteúdo do arquivo HTML
        with open('templates/index.html', 'r') as file:
            html_content = file.read()
        return html_content
    
    @cherrypy.expose
    def pl_csc(self):
        # Lê o conteúdo do arquivo HTML
        with open('templates/pl_csc.html', 'r') as file:
            html_content = file.read()
        return html_content
    
    @cherrypy.expose
    def adicionar(self, nome_impressora):
        print(f"Adicionando impressora: {nome_impressora}")
        # Verifica se o nome da impressora está no dicionário
        if nome_impressora in self.impressoras:
            # Obtém o caminho completo da impressora
            caminho_impressora = self.servidor_impressora + self.impressoras[nome_impressora]
            print(f"Caminho da impressora: {caminho_impressora}")

            # Caminho completo para o executável do PowerShell
            #caminho_powershell = r'C:\\Program Files\\PowerShell\\7\\pwsh.exe'  # Substitua pelo caminho correto no seu sistema

            # Comando PowerShell para adicionar a impressora
            comando_ps = f"powershell -Command (New-Object -ComObject WScript.Network).AddWindowsPrinterConnection('{caminho_impressora}')"
            print(f"Comando PowerShell: {comando_ps}")

            # Executa o comando PowerShell
            resultado_ps = subprocess.run(comando_ps, capture_output=True, text=True, shell=True)
            print(f"Resultado PowerShell: {resultado_ps.stdout}")

            # Verifica se a impressora foi adicionada com sucesso
            if resultado_ps.returncode == 0:
                return f"Impressora {nome_impressora} adicionada com sucesso!"
            else:
                return f"Erro ao adicionar impressora {nome_impressora}: {resultado_ps.stderr.strip()}"
        else:
            return f"Impressora {nome_impressora} não encontrada."

# Configura o servidor CherryPy
cherrypy.config.update({'server.socket_host': '127.0.0.1'})  # Permitir acesso externo
cherrypy.config.update({'server.socket_port': 8080})       # Definir porta

# Adiciona o controlador à árvore do CherryPy
cherrypy.tree.mount(ImpressoraController(), '/')

# Inicia o servidor
cherrypy.engine.start()
cherrypy.engine.block()
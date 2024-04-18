import win32print
import cherrypy
import json
import os

class PrintersWebService(object):
    def __init__(self):
        self.platina_csc_printers = {
            "PL CSC ADM": "\\\\192.0.0.61\\csc-adm-preto-sp5200s",
            "Exportação": "\\\\192.0.0.61\\csc-exportacao-preto-sp377sf",
            "Comercial": "\\\\192.0.0.61\\csc-comercial-preto-sp5200s",
            "Marketing": "\\\\192.0.0.61\\csc-mkt-preto-c368",
            "Financeiro": "\\\\192.0.0.61\\csc-financeiro-1102w"
        }
        self.platina_log_printers = {
            "PL LOG ADM": "\\\\192.0.0.61\\platina-log-adm-preto",
            "Ambulatório": "\\\\192.0.0.61\\platina-log-ambulatorio-preto-m320f",
            "Expedição": "\\\\192.0.0.61\\platina-log-exp-preto-c368",
            "Expedição Zebra": "\\\\192.0.0.61\\log-exp-zebra-zt230",
            "Portaria Zebra": "\\\\192.0.0.61\\platina-log-rec-zgk420t",
            "Segurança": "\\\\192.0.0.61\\platina-log-seg-preto-sp3710sf"
        }
        self.masterline_main_printers = {
            "MLN ADM": "\\\\192.0.0.61\\mln-adm-a3-mpc3503",
            "Almoxarifado Pigmento - Sankhya": "\\\\192.0.0.61\\mln-almoxpigmento-sankhya-zebrazm400",
            "Almoxarifado Quimico": "\\\\192.0.0.61\\mln-almoxquimica-preto-brother8157",
            "Almoxarifado Quimico - Etiquetas": "\\\\192.0.0.61\\mln-almoxquimica-etiquetas-zebrazm400",
            "Almoxarifado Rótulos": "\\\\192.0.0.61\\mln-almoxrotulos-preto-b400v4ps",
            "Almoxarifado Rótulos - Sankhya": "\\\\192.0.0.61\\mln-almoxrotulos-sankhya-zebrazt410",
            "Ambulatório": "\\\\192.0.0.61\\mln-ambulatorio-preto-sp5210sf",
            "RH": "\\\\192.0.0.61\\mln-dp-preto-mpc3003",
            "Envase": "\\\\192.0.0.61\\mln-envase-preto-sp5200s",
            "Etiquetas Corpore01": "\\\\192.0.0.61\\mln-etiquetas-corpore01-zebrazt410",
            "Etiquetas Corpore02": "\\\\192.0.0.61\\mln-etiquetas-corpore02-zebrazt410",
            "Etiquetas Corpore03": "\\\\192.0.0.61\\mln-etiquetas-corpore03-zebrazt410",
            "Etiquetas Corpore05": "\\\\192.0.0.61\\mln-etiquetas-corporeO5-zebrazt411",
            "Etiquetas Corpore06": "\\\\192.0.0.61\\mln-etiquetas-corpore06-zebrazt411",
            "Etiquetas Corpore07": "\\\\192.0.0.61\\mln-etiquetas-corpore07-zebrazt411",
            "Fisico Quimico - Sankhya": "\\\\192.0.0.61\\mln-fisicoquimico-sankhyal-zebrazt411",
            "Manutenção": "\\\\192.0.0.61\\mln-manutencao-preto-sp5210sf",
            "P&D": "\\\\192.0.0.61\\mln-ped-preto-mpc3003",
            "Pesagem": "\\\\192.0.0.61\\mln-presagem-preto-sp4510sf",
            "Pesagem - Sankhya01": "\\\\192.0.0.61\\mln-pesagem-sankhya-zebras4m",
            "Pesagem - Sankhya02": "\\\\192.0.0.61\\mln-pesagem-sankhya-zebrazt410"
        }
        self.masterline_log_printers = {
            "MLN LOG ADM": "\\\\192.0.0.61\\mln-log-g2-preto-sp377sfwx",
            "MLN LOG ADM - Sankhya": "\\\\192.0.0.61\\mln-log-g2-zebra-gk420t",
            "MLN LOG Estoque": "\\\\192.0.0.61\\mln-log-estoque-preto-sp5210sf",
            "MLN LOG Estoque - Sankhya": "\\\\192.0.0.61\\mln-log-estoque-sankhya-gk420t"
        }
        self.masterline_emb_printers = {
            "MLN EMB ADM": "\\\\192.0.0.61\\mln-embalagem-preto-sp5200s",
            "MLN EMB - Sankhya": "\\\\192.0.0.61\\mln-emabalagem-sankhya-zebrazm400"
        }
        self.masterline_flexo_printers = {}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def adicionar_impressora(self):
        data = cherrypy.request.json
        printer_name = data.get('printerName')
        caminho_impressora = None

        for printer_dict in [self.platina_csc_printers,
                            self.platina_log_printers,
                            self.masterline_main_printers,
                            self.masterline_log_printers,
                            self.masterline_flexo_printers,
                            self.masterline_emb_printers]:
            if printer_name in printer_dict:
                caminho_impressora = printer_dict[printer_name]
                break
        if caminho_impressora is None:
            cherrypy.response.status = 404
            return {'message': 'Printer not found'}

        try:
            win32print.AddPrinterConnection(caminho_impressora)
            return {'message': 'Impressora adicionada com sucesso'}
        except Exception as e:
            cherrypy.response.status = 500
            return {'message': f'Erro ao adicionar a impressora: {e}'}

    @cherrypy.expose
    def index(self):
        return open('templates/index.html')

    @cherrypy.expose
    def pl_csc(self):
        return open('templates/pl_csc.html')
'''
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('pl_log.html')
        return tmpl.render()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('ml_main.html')
        return tmpl.render()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('ml_log.html')
        return tmpl.render()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('ml_flexo.html')
        return tmpl.render()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('ml_emb.html')
        return tmpl.render()
'''

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, 'static')

    cherrypy.quickstart(PrintersWebService(), '/', {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir
        }
    })
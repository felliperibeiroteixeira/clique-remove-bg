from removebg import rm
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.image import Image
from io import BytesIO
import os 

Window.clearcolor = .10, .10, .10, 1

Builder.load_file('clique_remove_bg.kv')

#Armazena em variável o arquivo temporário da imagem para a remoção da pasta temp.
temp = 'temp/alpha.png'

class Geral():
    def gerenciar_painel(self, painel, slide='Slide', efeito='left'):
        if (slide == 'Slide'):
            self.manager.transition = SlideTransition()
        else:
            self.manager.transition = NoTransition()
            self.manager.transition.direction = efeito
            self.manager.current = painel

class PainelImportar(Screen, Geral):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self.abrir)       

    def gerenciar_msg(self, texto):
        lb = self.ids.mensagem
        lb.text = texto    

    def abrir(self, window, caminho_arquivo):
        c = caminho_arquivo.decode('utf-8')
        if (rm.carregar_img(c) == False):
            self.gerenciar_msg('Erro ao importar arquivo')
        else:
            self.gerenciar_painel('painel_editar', 'No')
            painel_editar = self.manager.get_screen('painel_editar')
            painel_editar.exibir_img()
            
class PainelEditar(Screen, Geral):  
    def on_pre_enter(self):
        Window.bind(on_request_close=self.remove_temp)

    #Remove o arquivo temporário ao fechar o aplicativo.

    def remove_temp(self, *args, **kwargs):
        os.remove(temp)
    
    def exibir_img(self):
        area_img = self.ids.area_img
        area_img.clear_widgets()
        img_buffer = BytesIO()
        rm.img.save(img_buffer, format=rm.img_formato)
        img_buffer.seek(0)
        c = CoreImage(img_buffer, ext=rm.img_formato.lower())
        t = c.texture
        img_buffer.close()
        img = Image()
        img.texture = t
        area_img.add_widget(img)

    def btnRemover_bg(self):
        rm.remover_bg()
        self.exibir_img()

    def voltar_inicio(self):
        painel_importar = self.manager.get_screen('painel_importar')
        painel_importar.gerenciar_msg('Arraste uma imagem aqui')
        self.gerenciar_painel('painel_importar', 'No')

    def btnIniciar(self):
        #Verefica se o arquivo temporário está na pasta temp e o deleta.
        if (os.path.exists(temp)): 
            os.remove(temp)
            rm.resetar()
            self.voltar_inicio()
        else:
            rm.resetar()
            self.voltar_inicio()       

    def btnExportar(self):
        rm.exportar(rm.img_local, rm.img_nome + '_bg_removido')

sm = ScreenManager()
sm.add_widget(PainelImportar(name='painel_importar'))
sm.add_widget(PainelEditar(name='painel_editar'))

class clique_remove_bg(App):
    title = 'Clique Remove BG'
    def build(self):
        self.icon = 'icones/clique_remove_bg.png'
        return sm

if __name__ == '__main__':
    clique_remove_bg().run()

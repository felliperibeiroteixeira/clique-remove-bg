from rembg import remove
from PIL import Image
from os import path
import os

#Armazena em variável o arquivo temporário da imagem com o canal Alpha RGBA aplicado.
temp = 'temp/alpha.png'

class remove_bg():
    img = None
    img_formato = None
    img_local = None
    img_nome = None
    img_ext = None

    def resetar(self):
        self.img = None
        self.img_formato = None
        self.img_local = None
        self.img_nome = None
        self.img_ext = None

    def carregar_img(self, img):
        try:
            self.img = Image.open(img)
            """Converte a imagem e aplica o canal Alpha RGBA,
            e o aramazena na pasta temp para reimportala"""
            self.img.save(temp) 
            self.img = Image.open(temp)
            self.img_formato = self.img.format
            self.img_local = path.dirname(path.realpath(img))
            self.img_nome, self.img_ext = path.splitext(path.basename(img))
            return True
        except:
            return False
        
    def remover_bg(self):
        output = remove(self.img)
        self.img = output

    def exportar(self, local_img, nome_img):
        ln = local_img + '/' + nome_img + '.png'
        self.img.save(ln)
                        
rm = remove_bg()

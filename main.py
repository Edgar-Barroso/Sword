# coding: utf-8
import kivy

kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

Window.size = (525, 600)


class Receita:
    def __init__(self):
        self.ingredientes = []

    def custo(self):
        cust = 0
        for ingrediente in self.ingredientes:
            cust += ingrediente.custo
        return f"R${cust:.2f}"

    def gastos(self):
        gast = ''
        for ingrediente in self.ingredientes:
            gast += f'R${ingrediente.custo:.2f} em {ingrediente.nome}\n'
        return gast


class Ingrediente:
    def __init__(self, nome, quantidade, quantidade_embalagem, valor_da_unidade):
        self.nome = nome
        self.custo = float(quantidade) * (float(valor_da_unidade) / float(quantidade_embalagem))



class Tela2(BoxLayout):
    def salvar(self):
        try:
            nome = self.ids.tx1.text
            quantidade = self.ids.tx2.text
            quantidade_embalagem = self.ids.tx3.text
            valor_da_unidade = self.ids.tx4.text
            ingrediente = Ingrediente(nome, quantidade, quantidade_embalagem, valor_da_unidade)
            receita.ingredientes.append(ingrediente)
            print(nome, quantidade, quantidade_embalagem, valor_da_unidade , "salvo")
            self.ids.tx5.text = receita.custo()
        except TypeError:
            pass
    def finalizar(self):
        print(receita.gastos())


class Tela1(FloatLayout):

    def entrar(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Tela2())


class ReceitaApp(App):
    def __init__(self):
        super(ReceitaApp, self).__init__()

    def build(self):
        return Tela1()


receita = Receita()
janela = ReceitaApp()
janela.run()

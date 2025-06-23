import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        if anno is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, seleziona un anno"))
        elif forma is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzeione, seleziona una forma"))
        else:
            connesse, maxCon = self._model.buildGraph(anno,forma)
            numNodi, numArchi = self._model.getGraphDetails()
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Grafo creato correttamente"))
            self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {numNodi}"))
            self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {numArchi}"))
            self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {len(connesse)} componenti connesse"))
            self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {len(maxCon)} nodi"))
            for n in maxCon:
                self._view.txt_result1.controls.append(ft.Text(f"{n}"))
        self._view.update_page()





    def handle_path(self, e):
        pass

    def fillDDYear(self):
        anni = self._model.getYears()
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillDDShape(self,e):
        self._view.ddshape.options.clear()
        anno = self._view.ddyear.value
        forme = self._model.getShape(anno)
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))
        self._view.update_page()

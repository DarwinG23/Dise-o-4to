from typing import Type
from controls.dao.daoAdapter import DaoAdapter
from models.periodoacademico import PeriodoAcademico

class PeriodoAcademicoControl(DaoAdapter):
    def __init__(self):
        super().__init__(PeriodoAcademico) 
        self.__periodo_academico = None

    @property
    def _periodo_academico(self):
        if self.__periodo_academico is None:
            self.__periodo_academico = PeriodoAcademico()
        return self.__periodo_academico

    @_periodo_academico.setter
    def _periodo_academico(self, value):
        self.__periodo_academico = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        self._save(self._periodo_academico)

    def merge(self, pos):
        self._merge(self._periodo_academico, pos)

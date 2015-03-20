# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# TODO switch to to average tax rates

from __future__ import division

import copy
from numpy import logical_not as not_, minimum as min_

import logging

from openfisca_core import columns, formulas, reforms
from openfisca_france import entities
from openfisca_france.model import base
from openfisca_france.model.prelevements_obligatoires.impot_revenu import ir

log = logging.getLogger(__name__)


class ppe(formulas.SimpleFormulaColumn):
    label = u"PPE annulée"
    reference = ir.ppe

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        cd1 = simulation.calculate('cd1', period)

        return period, cd1 * 0


class charge_loyer(formulas.SimpleFormulaColumn):
    column = columns.FloatCol
    entity_class = entities.FoyersFiscaux
    label = u"Charge déductible pour paiement d'un loyer"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        loyer_holder = simulation.calculate('loyer', period)
        nbptr = simulation.calculate('nbptr', period)
        loyer = self.cast_from_entity_to_role(loyer_holder, entity = "menage", role = base.PREF)
        loyer = self.sum_by_entity(loyer)
        charge_loyer = simulation.legislation_at(period.start).charge_loyer

        plaf = charge_loyer.plaf
        plaf_nbp = charge_loyer.plaf_nbp
        plafond = plaf * (not_(plaf_nbp) + plaf * nbptr * plaf_nbp)

        return period, 12 * min_(loyer / 12, plafond)


# Reform legislation
reform_legislation_subtree = {
    "charge_loyer": {
        "@type": "Node",
        "description": "Charge de loyer",
        "children": {
            "active": {
                "@type": "Parameter",
                "description": "Activation de la charge",
                "format": "bool",
                "values": [{'start': u'2002-01-01', 'stop': '2013-12-31', 'value': 1}],
                },
            "plaf": {
                "@type": "Parameter",
                "description": 'Plafond mensuel',
                "format": 'integer',
                "unit": 'currency',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 1000}],
                },
            "plaf_nbp": {
                "@type": "Parameter",
                "description": 'Ajuster le plafond au nombre de part',
                "format": 'bool',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 0}],
                },
            },
        }
    }


# Build function

def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)
    Reform = reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u'Loyer comme charge déductible (Trannoy-Wasmer)',
        new_formulas = (ppe, charge_loyer),
        reference = tax_benefit_system,
        )
    return Reform()

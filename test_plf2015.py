# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

import datetime

from openfisca_core import periods, reforms
import openfisca_france

TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test(year = 2014):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salbrut',
                max = 100000,
                min = 0,
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    print simulation.calculate('revdisp')
 
def test_plf15_reform():
    simulation_year = 2014
    simulation_period = periods.period('year', simulation_year)
    reference_legislation_json = tax_benefit_system.legislation_json
#    import json
#    import os
#    with open(os.path.join(os.path.dirname(__file__), 'reference_legislation.json'), 'w') as json_file:
#        json.dump(reference_legislation_json, json_file, indent = 4)

    return
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reference_legislation_json,
        path = ('children', 'ir', 'children', 'bareme', 'slices', 0, 'rate'),
        period = simulation_period,
        value = 1,
        )

    reform = reforms.Reform(
        name = u'IR_100_tranche_1',
        label = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche",
        legislation_json = reform_legislation_json,
        reference_legislation_json = reference_legislation_json
        )

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        period = simulation_period,
        parent1 = dict(birth = datetime.date(simulation_year - 40, 1, 1)),
        )

    simulation = scenario.new_simulation(debug = True)
    assert_less(max(abs(simulation.calculate('impo') - [0, -7889.20019531, -23435.52929688])), .01)

    reform_simulation = reform.new_simulation(debug = True, scenario = scenario)
    assert_less(max(abs(reform_simulation.calculate('impo') - [0., -13900.20019531, -29446.52929688])), .0001)

   
   
   
if __name__ == '__main__':
#    test()
    test_plf15_reform()

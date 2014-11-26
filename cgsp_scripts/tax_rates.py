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


import matplotlib.pyplot as plt


from openfisca_france.tests import base
from openfisca_qt.matplotlib import graphs


def draw_tax_rate(filename = None):
    year = 2013
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10000,
                name = 'salbrut',
                max = 60000,
                min = 0,
                ),
            ],
        period = year,
        parent1 = dict(agem = 40 * 12 + 6),
        ).new_simulation()  # Remove debug = True, because logging is too slow.

    fig = plt.figure()
    axes = plt.gca()

    graphs.draw_rates(
        simulation = simulation,
        axes = axes,
        x_axis = 'salsuperbrut',
        y_axis = 'revdisp',
        )
    if filename:
        fig.savefig('{}.png'.format(filename))


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    draw_tax_rate()

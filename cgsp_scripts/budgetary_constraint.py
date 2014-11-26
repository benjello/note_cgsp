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


from __future__ import division


import datetime
import os

import matplotlib.pyplot as plt

from openfisca_core import periods
from openfisca_france.tests import base
from openfisca_qt.matplotlib import graphs


def celibataire(year):
    return dict(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        menage = dict(so = 4),
        )


def parent_isole(year):
    return dict(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(so = 4),
        )


def couple_sans_enfant(year):
    return dict(
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            statmarit = 1,
            ),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        menage = dict(so = 4),
        )


def couple_deux_enfants(year):
    return dict(
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            statmarit = 1,
            ),
        parent2 = dict(
            birth = datetime.date(year - 40, 1, 1),
            statmarit = 1,
            ),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(so = 4),
        )


def plot_and_save_figure(single_entity_kwargs, filename = None, show = None):
    scenario = base.tax_benefit_system.new_scenario().init_single_entity(**single_entity_kwargs)
    simulation = scenario.new_simulation(debug = True)
#    sali = simulation.calculate('sali')
#    print 'statmarit :', simulation.calculate('statmarit')
    n_pers = simulation.calculate('nb_adult') + simulation.calculate('nb_pac')
#   n = max(n_pers)
#    loyer = sali.copy()[0::n] / 3 / 12
    import numpy as np
#    simulation.get_or_new_holder('loyer').array = np.maximum(loyer, max(400 * n, 1000))
    simulation.get_or_new_holder('loyer').array = 500 * np.minimum(n_pers, 2)

    simulation.calculate('revdisp')
    print simulation
    fig = plt.figure()
    axes = plt.gca()
    graphs.draw_bareme(
        simulation = simulation,
        axes = axes,
        x_axis = 'sal',
        visible_lines = ['revdisp'],
        legend_position = 4,
        )
    if show:
        plt.show()

    if filename:
        fig.savefig('figures/{}.png'.format(filename))


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    for year in range(2002,2015):
        for menage in [celibataire, parent_isole, couple_sans_enfant, couple_deux_enfants]:

            single_entity_kwargs = menage(year)
            filename = "{}_{}".format(menage.__name__, year)
            single_entity_kwargs.update(
                dict(
                    axes = [
                        dict(
                            count = 200,
                            max = 40000,
                            min = 0,
                            name = 'sali',
                            ),
                        ],
                    period = periods.period('year', year),
                    )
                )
            print filename
            print single_entity_kwargs
            plot_and_save_figure(single_entity_kwargs, filename = filename)

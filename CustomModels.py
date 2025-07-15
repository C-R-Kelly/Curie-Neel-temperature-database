from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from chemdataextractor.model import Compound
from chemdataextractor.model.base import StringType, ModelType, FloatType
from chemdataextractor.model.units.temperature import TemperatureModel

from chemdataextractor.parse.elements import I, R, W, T
from chemdataextractor.parse.actions import join

from CDE_Model.CustomParsers.ct_v4_wiley_dev import CtParser
from CDE_Model.CustomParsers.nt import NtParser


class CurieTemperature(TemperatureModel):
    specifier = StringType(
        parse_expression=(((I('Curie') + I('Temperature')).add_action(join)) | I('Tc') | I('Tcurie')),
        required=True)
    compound = ModelType(Compound, required=True, contextual=True, binding=True, updatable=False)
    compound.model_class.fields['names'].required = True
    confidence = FloatType()
    sentence = StringType()

    parsers = [CtParser()]


class NeelTemperature(TemperatureModel):
    specifier = StringType(
        parse_expression=((((I('Néel') | I('Neel')) + I('Temperature')).add_action(join)) | I('Tn') | I('TNéel') | I(
            'TNeel')),
        required=True)
    compound = ModelType(Compound, required=True, contextual=True, binding=True, updatable=False)
    compound.model_class.fields['names'].required = True

    confidence = FloatType()
    sentence = StringType()

    parsers = [NtParser()]

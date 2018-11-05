import api.models

def get_model(model_name, *args):
    row = None if not len(args) else args[0]
    instance = {
        'civilizations': lambda row:
            api.models.civilization.CivilizationModel(*row) if len(args) else api.models.civilization.CivilizationModel,
        'units': lambda row:
            api.models.unit.UnitModel(*row) if len(args) else api.models.unit.UnitModel,
        'structures': lambda row:
            api.models.structure.StructureModel(*row) if len(args) else api.models.structure.StructureModel,
        'technologies': lambda row:
            api.models.technology.TechnologyModel(*row) if len(args) else api.models.technology.TechnologyModel
    }[model_name](row)

    return instance

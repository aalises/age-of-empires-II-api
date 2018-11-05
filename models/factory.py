import models

def get_model(model_name, *args):
    row = None if not len(args) else args[0]
    instance = {
        'civilizations': lambda row:
            models.civilization.CivilizationModel(*row) if len(args) else models.civilization.CivilizationModel,
        'units': lambda row:
            models.unit.UnitModel(*row) if len(args) else models.unit.UnitModel,
        'structures': lambda row:
            models.structure.StructureModel(*row) if len(args) else models.structure.StructureModel,
        'technologies': lambda row:
            models.technology.TechnologyModel(*row) if len(args) else models.technology.TechnologyModel
    }[model_name](row)

    return instance

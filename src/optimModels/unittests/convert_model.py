from optimModels.utils.utils import fix_exchange_reactions_model
from framed.io.sbml import load_cbmodel
if __name__=="__main__":
    SBML_FILE = "../../../examples/models/saraModel.xml"
    model = load_cbmodel(SBML_FILE, flavor="cobra")
    newModel = fix_exchange_reactions_model(model)
    newModel
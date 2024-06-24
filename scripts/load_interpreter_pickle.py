import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb

sb.set_theme()


def load_data():
    with open("results/interpreter_pickles/irr3_argentina.pickle", "rb") as f:
        irr = pickle.load(f)

    kcals = {
        "fish": irr.fish_kcals_equivalent.kcals,
        "csugar": irr.cell_sugar_kcals_equivalent.kcals,
        "scp": irr.scp_kcals_equivalent.kcals,
        "greenhouse": irr.greenhouse_kcals_equivalent.kcals,
        "seaweed": irr.seaweed_kcals_equivalent.kcals,
        "milk": irr.milk_kcals_equivalent.kcals,
        "meat": irr.meat_kcals_equivalent.kcals,
        "outcrop": irr.immediate_outdoor_crops_kcals_equivalent.kcals,
        "storedcrop": irr.new_stored_outdoor_crops_kcals_equivalent.kcals,
        "storedfood": irr.stored_food_kcals_equivalent.kcals,
    }

    kcals = pd.DataFrame(kcals)  # this is total kcals per category
    meat = pd.DataFrame(irr.meat_dictionary)  # this is total meat culled
    meat = meat.drop(columns=["milk_cattle"])
    meat.columns = [c.replace("meat_", "") for c in meat.columns]
    meat_ratio = meat.div(meat.sum(axis=1), axis=0)  # this is ratio of meat culled
    # I am using this ratio as a proxy for the composition of the 'meat' variable in the optimiser'
    # TODO: ask Simon if there is a better way than this
    return kcals, meat_ratio


def main():
    kcals, meat_ratio = load_data()
    print(meat_ratio.columns)


if __name__ == "__main__":
    main()

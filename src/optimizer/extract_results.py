#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Convert optimizer output to numpy arrays in order to later interpret and validate them 

Created on Tue Jul 22

@author: morgan
"""
import os
import sys
import numpy as np

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.food_system.food import Food


class Extractor:
    def __init__(self, constants):
        self.constants = constants

    def extract_results(
        self, model, variables, single_valued_constants, multi_valued_constants
    ):
        # extract the results from the model

        self.get_objective_optimization_results(model)

        # if no stored food, plot shows zero
        self.extract_stored_food_results(variables["stored_food_eaten"])

        # extract numeric seaweed results in terms of people fed and raw
        # tons wet

        # if seaweed not added to model, plot shows zero
        self.extract_seaweed_results(
            variables["seaweed_wet_on_farm"],
            variables["used_area"],
            multi_valued_constants["built_area"],
            variables["seaweed_food_produced"],
        )

        # if no cellulosic sugar, plot shows zero
        self.extract_cell_sugar_results(
            multi_valued_constants["production_kcals_cell_sugar_per_month"],
        )

        # if no scp, plot shows zero
        self.extract_SCP_results(
            multi_valued_constants["production_kcals_scp_per_month"],
            multi_valued_constants["production_fat_scp_per_month"],
            multi_valued_constants["production_protein_scp_per_month"],
        )

        # if no fish, plot shows zero
        self.extract_fish_results(
            multi_valued_constants["production_kcals_fish_per_month"],
            multi_valued_constants["production_fat_fish_per_month"],
            multi_valued_constants["production_protein_fish_per_month"],
        )

        # if no greenhouses, plot shows zero
        self.extract_greenhouse_results(
            multi_valued_constants["greenhouse_kcals_per_ha"],
            multi_valued_constants["greenhouse_fat_per_ha"],
            multi_valued_constants["greenhouse_protein_per_ha"],
            multi_valued_constants["greenhouse_area"],
        )

        # if no outdoor food, plot shows zero
        self.extract_outdoor_crops_results(
            variables["crops_food_eaten_no_rotation"],
            variables["crops_food_eaten_with_rotation"],
            variables["crops_food_storage_no_rotation"],
            variables["crops_food_storage_rotation"],
            multi_valued_constants["crops_food_produced"],
        )

        # if nonegg nondairy meat isn't included, these results plot shows zero
        self.extract_meat_dairy_results(
            multi_valued_constants["meat_eaten"],
            multi_valued_constants["dairy_milk_kcals"],
            multi_valued_constants["dairy_milk_fat"],
            multi_valued_constants["dairy_milk_protein"],
            multi_valued_constants["cattle_maintained_kcals"],
            multi_valued_constants["cattle_maintained_fat"],
            multi_valued_constants["cattle_maintained_protein"],
            multi_valued_constants["h_e_meat_kcals"],
            multi_valued_constants["h_e_meat_fat"],
            multi_valued_constants["h_e_meat_protein"],
            multi_valued_constants["h_e_milk_kcals"],
            multi_valued_constants["h_e_milk_fat"],
            multi_valued_constants["h_e_milk_protein"],
            multi_valued_constants["h_e_balance"],
        )

        return self

    # order the variables that occur mid-month into a list of numeric values
    def to_monthly_list(self, variables, conversion):
        variable_output = []
        # if the variable was not modeled
        if type(variables[0]) == type(0):
            return np.array([0] * len(variables))  # return initial value

        SHOW_OUTPUT = False
        if SHOW_OUTPUT:
            print("Monthly Output for " + str(variables[0]))

        for month in range(0, self.constants["NMONTHS"]):
            val = variables[month]

            # if something went wrong and the variable was not added for a certain month
            assert type(val) != type(0)
            variable_output.append(val.varValue * conversion)
            if SHOW_OUTPUT:
                print("    Month " + str(month) + ": " + str(variable_output[month]))
        return np.array(variable_output)

    # order the variables that occur mid-month into a list of numeric values

    def to_monthly_list_outdoor_crops_kcals(
        self,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        crops_kcals_produced,
        conversion,
    ):

        immediately_eaten_output = []
        new_stored_eaten_output = []
        cf_eaten_output = []
        cf_produced_output = []

        # if the variable was not modeled
        if type(crops_food_eaten_no_rotation[0]) == type(0):
            return [
                [0] * len(crops_food_eaten_no_rotation),
                [0] * len(crops_food_eaten_no_rotation),
            ]  # return initial value

        SHOW_OUTPUT = False
        if SHOW_OUTPUT:
            print("Monthly Output for " + str(crops_food_eaten_no_rotation[0]))

        for month in range(0, self.constants["NMONTHS"]):
            cf_produced = crops_kcals_produced[month]
            cf_produced_output.append(cf_produced)
            cf_eaten = (
                crops_food_eaten_no_rotation[month].varValue
                + crops_food_eaten_with_rotation[month].varValue
                * self.constants["OG_ROTATION_FRACTION_KCALS"]
            )
            cf_eaten_output.append(cf_eaten)

            if cf_produced <= cf_eaten:
                immediately_eaten = cf_produced
                new_stored_crops_eaten = cf_eaten - cf_produced
            else:  # crops_food_eaten < crops_kcals_produced
                immediately_eaten = cf_eaten
                new_stored_crops_eaten = 0

            immediately_eaten_output.append(immediately_eaten * conversion)
            new_stored_eaten_output.append(new_stored_crops_eaten * conversion)
            SHOW_OUTPUT = False
            if SHOW_OUTPUT:
                print(
                    "    Month "
                    + str(month)
                    + ": imm eaten: "
                    + str(immediately_eaten_output[month])
                    + " new stored eaten: "
                    + str(new_stored_eaten_output[month])
                )

        return [immediately_eaten_output, new_stored_eaten_output]

    # if greenhouses aren't included, these results will be zero

    def extract_greenhouse_results(
        self,
        greenhouse_kcals_per_ha,
        greenhouse_fat_per_ha,
        greenhouse_protein_per_ha,
        greenhouse_area,
    ):

        self.billions_fed_greenhouse_kcals = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_kcals_per_ha) * 1 / self.constants["KCALS_MONTHLY"],
        )

        self.billions_fed_greenhouse_fat = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_fat_per_ha) * 1 / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_greenhouse_protein = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_protein_per_ha)
            * 1
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        self.greenhouse = Food(
            kcals=self.billions_fed_greenhouse_kcals,
            fat=self.billions_fed_greenhouse_fat,
            protein=self.billions_fed_greenhouse_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # if fish aren't included, these results will be zero

    def extract_fish_results(
        self,
        production_kcals_fish_per_month,
        production_fat_fish_per_month,
        production_protein_fish_per_month,
    ):
        self.billions_fed_fish_kcals = (
            np.array(production_kcals_fish_per_month) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_fish_protein = (
            np.array(production_protein_fish_per_month)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.billions_fed_fish_fat = (
            np.array(production_fat_fish_per_month)
            / self.constants["FAT_MONTHLY"]
            / 1e9
        )

        self.fish = Food(
            kcals=self.billions_fed_greenhouse_kcals,
            fat=self.billions_fed_greenhouse_fat,
            protein=self.billions_fed_greenhouse_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # if outdoor growing isn't included, these results will be zero
    def extract_outdoor_crops_results(
        self,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        crops_food_storage_no_rot,
        crops_food_storage_rot,
        crops_food_produced,
    ):
        self.no_rot = self.to_monthly_list(crops_food_eaten_no_rotation, 1)
        self.rot = self.to_monthly_list(
            crops_food_eaten_with_rotation,
            self.constants["OG_ROTATION_FRACTION_KCALS"],
        )

        self.billions_fed_outdoor_crops_storage_no_rot = self.to_monthly_list(
            crops_food_storage_no_rot,
            1 / self.constants["KCALS_MONTHLY"],
        )

        # immediate from produced and storage changes account for all eaten
        # but storage can come from produced!
        # we know storage_change + all_eaten = produced
        # if(storage_change>=0):
        #   assert(all_eaten >= storage_change)
        #   eaten_from_stored = storage_change
        #   immediately_eaten = all_eaten - eaten_from_stored
        # else:
        #   eaten_from_stored = 0

        [
            self.billions_fed_immediate_outdoor_crops_kcals,
            self.billions_fed_new_stored_outdoor_crops_kcals,
        ] = self.to_monthly_list_outdoor_crops_kcals(
            crops_food_eaten_no_rotation,
            crops_food_eaten_with_rotation,
            og_produced_kcals,
            1 / self.constants["KCALS_MONTHLY"],
        )

        self.billions_fed_outdoor_crops_kcals = np.array(
            self.to_monthly_list(
                crops_food_eaten_no_rotation,
                1 / self.constants["KCALS_MONTHLY"],
            )
        ) + np.array(
            self.to_monthly_list(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_KCALS"]
                / self.constants["KCALS_MONTHLY"],
            )
        )

        self.billions_fed_outdoor_crops_fat = np.array(
            self.to_monthly_list(
                crops_food_eaten_no_rotation,
                self.constants["OG_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
            )
        ) + np.array(
            self.to_monthly_list(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_FAT"]
                / self.constants["FAT_MONTHLY"]
                / 1e9,
            )
        )

        # EACH MONTH: 1218263.5 billion kcals per person
        # 1000s tons protein equivalent:
        #

        # CROPS FOOD EATEN BILLION KCALS PER PERSON PER MONTH 1094666.5
        # OG_FRACTION_PROTEIN: 1000 tons protein per billion kcals
        # THOU_TONS_PROTEIN_NEEDED: thousands of tons per month for population
        # OG_FRACTION_PROTEIN: 1000tons/billion kcals
        # PROTEIN_MONTHLY: 1000 tons protein per month per person

        # crops_food_eaten_no_rotation:
        #   crops_food_eaten_no_rotation * OG_FRACTION_PROTEIN
        #   / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]

        #   gives a fraction, So

        #   [crops_food_eaten_no_rotation] == [?]
        #   [OG_FRACTION_PROTEIN] = 1000 tons protein per billion kcals
        #   [THOU_TONS_PROTEIN_NEEDED] = thousands of tons per month for population
        #   so, [?] = [thousands of tons per month for population]/[1000 tons protein per billion kcals]
        #   [?] = [billion kcals per month for population]
        #   [crops_food_eaten_no_rotation] = [billion kcals per month for population]
        #   therefore,
        #   [crops_food_eaten_no_rotation]
        #    * [OG_FRACTION_PROTEIN]
        #    / [PROTEIN_MONTHLY]
        #   gives us
        #   [billions_fed_outdoor_crops_protein] ==
        #   [billion kcals per month for population]
        #   * [1000tons protein/billion kcals]
        #   / [1000 tons protein per month per person]
        #   so
        #   [billions_fed_outdoor_crops_protein] ==
        #   [people]

        self.billions_fed_outdoor_crops_protein = np.array(
            self.to_monthly_list(
                crops_food_eaten_no_rotation,
                self.constants["OG_FRACTION_PROTEIN"]
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
            )
        ) + np.array(
            self.to_monthly_list(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_PROTEIN"]
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
            )
        )

        self.outdoor_crops = Food(
            kcals=self.billions_fed_outdoor_crops_kcals,
            fat=self.billions_fed_outdoor_crops_fat,
            protein=self.billions_fed_outdoor_crops_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.immediate_outdoor_crops = Food(
            kcals=self.billions_fed_immediate_outdoor_crops_kcals,
            fat=np.zeros(self.billions_fed_immediate_outdoor_crops_kcals.shape),
            protein=np.zeros(self.billions_fed_immediate_outdoor_crops_kcals.shape),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.new_stored_outdoor_crops = Food(
            kcals=self.billions_fed_new_stored_outdoor_crops_kcals,
            fat=np.zeros(self.billions_fed_new_stored_outdoor_crops_kcals.shape),
            protein=np.zeros(self.billions_fed_new_stored_outdoor_crops_kcals.shape),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # if cellulosic sugar isn't included, these results will be zero

    def extract_cell_sugar_results(
        self,
        production_kcals_cell_sugar_per_month,
    ):

        self.billions_fed_cell_sugar_kcals = (
            np.array(production_kcals_cell_sugar_per_month)
            / self.constants["KCALS_MONTHLY"]
        )

        self.cell_sugar = Food(
            kcals=self.billions_fed_cell_sugar_kcals,
            fat=np.zeros(self.billions_fed_cell_sugar_kcals.shape),
            protein=np.zeros(self.billions_fed_cell_sugar_kcals.shape),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # if methane scp isn't included, these results will be zero

    def extract_SCP_results(
        self,
        production_kcals_scp_per_month,
        production_fat_scp_per_month,
        production_protein_scp_per_month,
    ):

        self.billions_fed_SCP_kcals = (
            np.array(production_kcals_scp_per_month) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_SCP_fat = (
            np.array(production_fat_scp_per_month) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_SCP_protein = (
            np.array(production_protein_scp_per_month)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.scp = Food(
            kcals=self.billions_fed_SCP_kcals,
            fat=self.billions_fed_SCP_fat,
            protein=self.billions_fed_SCP_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # if stored food isn't included, these results will be zero
    def extract_meat_dairy_results(
        self,
        meat_eaten,
        dairy_milk_kcals,
        dairy_milk_fat,
        dairy_milk_protein,
        cattle_maintained_kcals,
        cattle_maintained_fat,
        cattle_maintained_protein,
        h_e_meat_kcals,
        h_e_meat_fat,
        h_e_meat_protein,
        h_e_milk_kcals,
        h_e_milk_fat,
        h_e_milk_protein,
        h_e_balance,
    ):

        self.billions_fed_meat_kcals_tmp = np.divide(
            meat_eaten, self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_meat_kcals = (
            self.billions_fed_meat_kcals_tmp
            + np.array(cattle_maintained_kcals) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_meat_fat_tmp = np.multiply(
            meat_eaten,
            self.constants["MEAT_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_meat_fat = (
            self.billions_fed_meat_fat_tmp
            + np.array(cattle_maintained_fat) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_meat_protein_tmp = np.multiply(
            meat_eaten,
            self.constants["MEAT_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        self.billions_fed_meat_protein = (
            self.billions_fed_meat_protein_tmp
            + np.array(cattle_maintained_protein)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.meat = Food(
            kcals=self.billions_fed_meat_kcals,
            fat=self.billions_fed_meat_fat,
            protein=self.billions_fed_meat_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.billions_fed_milk_kcals = (
            np.array(dairy_milk_kcals) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_milk_fat = (
            np.array(dairy_milk_fat) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_milk_protein = (
            np.array(dairy_milk_protein) / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.milk = Food(
            kcals=self.billions_fed_milk_kcals,
            fat=self.billions_fed_milk_fat,
            protein=self.billions_fed_milk_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.billions_fed_h_e_meat_kcals = (
            h_e_meat_kcals / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_h_e_meat_fat = (
            h_e_meat_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_meat_protein = (
            h_e_meat_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.h_e_meat = Food(
            kcals=self.billions_fed_h_e_meat_kcals,
            fat=self.billions_fed_h_e_meat_fat,
            protein=self.billions_fed_h_e_meat_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.billions_fed_h_e_milk_kcals = (
            h_e_milk_kcals / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_h_e_milk_fat = (
            h_e_milk_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_milk_protein = (
            h_e_milk_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.h_e_milk = Food(
            kcals=self.billions_fed_h_e_milk_kcals,
            fat=self.billions_fed_h_e_milk_fat,
            protein=self.billions_fed_h_e_milk_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.billions_fed_h_e_balance = h_e_balance.in_units_billions_fed()

    # if stored food isn't included, these results will be zero
    def extract_stored_food_results(self, stored_food_eaten):
        """
        TODO: Make this take the args:
            CROP_WASTE
            stored_food_eaten
        """

        self.billions_fed_stored_food_kcals = self.to_monthly_list(
            stored_food_eaten,
            1 / self.constants["KCALS_MONTHLY"],
        )

        self.sf = self.to_monthly_list(stored_food_eaten, 1)

        self.billions_fed_stored_food_fat = self.to_monthly_list(
            stored_food_eaten,
            self.constants["SF_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_stored_food_protein = self.to_monthly_list(
            stored_food_eaten,
            self.constants["SF_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        self.stored_food = Food(
            kcals=self.billions_fed_stored_food_kcals,
            fat=self.billions_fed_stored_food_fat,
            protein=self.billions_fed_stored_food_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def extract_seaweed_results(
        self,
        seaweed_wet_on_farm,
        used_area,
        built_area,
        seaweed_food_produced,
    ):

        self.seaweed_built_area = built_area
        self.seaweed_built_area_max_density = (
            np.array(built_area) * self.constants["MAXIMUM_DENSITY"]
        )

        self.seaweed_food_produced = self.to_monthly_list(seaweed_food_produced, 1)

        self.billions_fed_seaweed_kcals = self.to_monthly_list(
            seaweed_food_produced,
            self.constants["SEAWEED_KCALS"] / self.constants["KCALS_MONTHLY"],
        )

        self.billions_fed_seaweed_fat = self.to_monthly_list(
            seaweed_food_produced,
            self.constants["SEAWEED_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_seaweed_protein = self.to_monthly_list(
            seaweed_food_produced,
            self.constants["SEAWEED_PROTEIN"] / self.constants["PROTEIN_MONTHLY"] / 1e9,
        )

        self.seaweed = Food(
            kcals=self.billions_fed_seaweed_kcals,
            fat=self.billions_fed_seaweed_fat,
            protein=self.billions_fed_seaweed_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    # The optimizer will maximize minimum fat, calories, and protein over any month, but it does not care which sources these come from. The point of this function is to determine the probable contributions to excess calories used for feed and biofuel from appropriate sources (unless this has been updated, it takes it exclusively from outdoor growing and stored food).
    # there is also a constraint to make sure the sources which can be used for feed are not exhausted, and the model will not be able to solve if the usage from biofuels and feed are more than the available stored food and outdoor crop production.

    def get_objective_optimization_results(self, model):

        # I spent like five hours trying to figure out why the answer was wrong
        # until I finally found an issue with string ordering, fixed it below

        humans_fed_kcals = []
        humans_fed_fat = []
        humans_fed_protein = []
        order_kcals = []
        order_fat = []
        order_protein = []
        for var in model.variables():

            if "Humans_Fed_Kcals_" in var.name:
                humans_fed_kcals.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

                order_kcals.append(
                    int(var.name[len("Humans_Fed_Kcals_") :].split("_")[0])
                )

            if "Humans_Fed_Fat_" in var.name:
                order_fat.append(int(var.name[len("Humans_Fed_Fat_") :].split("_")[0]))

                humans_fed_fat.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

            if "Humans_Fed_Protein_" in var.name:

                order_protein.append(
                    int(var.name[len("Humans_Fed_Protein_") :].split("_")[0])
                )

                humans_fed_protein.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

        zipped_lists = zip(order_kcals, humans_fed_kcals)
        sorted_zipped_lists = sorted(zipped_lists)
        humans_fed_kcals_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_fat, humans_fed_fat)
        sorted_zipped_lists = sorted(zipped_lists)
        humans_fed_fat_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_protein, humans_fed_protein)
        sorted_zipped_lists = sorted(zipped_lists)
        humans_fed_protein_optimizer = [element for _, element in sorted_zipped_lists]

        return (
            humans_fed_kcals_optimizer,
            humans_fed_fat_optimizer,
            humans_fed_protein_optimizer,
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

The idea here is that the code is constantly creating objects with calories, fat, and
protein separately then passing these objects around to other places, so we might as
well create a class which has these 3 properties.

Note that occasionally, this class is instantiated with each nutrient set as an array
where each element of the array is a different month of the simulation, and the total
number of months is NMONTHS, which is also the length of each of the 3 arrays.

Created on Tue Jul 19

@author: morgan
"""
import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


class UnitConversions:
    """
    This class is used to convert units of nutrients
    """

    def __init__(self):
        self.NUTRITION_PROPERTIES_ASSIGNED = False

    # getters and setters

    def set_nutrition_requirements(
        self, kcals_daily, fat_daily, protein_daily, population
    ):
        """
        Returns the macronutrients of the food.

        This is a bit of a confusing function.

        It is normally run from a UnitConversions class in the Food child class

        that Food class contains one UnitConversions object which has had its nutrients
        assigned.

        Then, because this is the parent class, all the functions are inherited.

        So, running get_conversions() (the class function to get the conversions object
        in the child food class), this will obtain all the conversion data instantiated
        through the Food class.
        """

        self.days_in_month = 30

        # kcals per person
        self.kcals_monthly = kcals_daily * self.days_in_month

        # in thousands of tons (grams per ton == 1e6) per month
        self.fat_monthly = fat_daily / 1e6 * self.days_in_month / 1000

        # in thousands of tons (grams per ton == 1e6) per month per person
        self.protein_monthly = protein_daily / 1e6 * self.days_in_month / 1000

        # in billions of kcals per month for population
        self.billion_kcals_needed = self.kcals_monthly * population / 1e9
        # in thousands of tons per month for population
        self.thou_tons_fat_needed = self.fat_monthly * population
        # in thousands of tons per month for population
        self.thou_tons_protein_needed = self.protein_monthly * population

        self.population = population

        self.NUTRITION_PROPERTIES_ASSIGNED = True

    def get_units_from_list_to_total(self):
        """
        gets the units so that they reflect that of a single month
        """
        # remove the " each month" part of the units
        kcals_units = self.kcals_units.split(" each month")[0]

        # remove the " each month" part of the units
        fat_units = self.fat_units.split(" each month")[0]

        # remove the " each month" part of the units
        protein_units = self.protein_units.split(" each month")[0]

        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_total(self):
        """
        sets the units so that they reflect that of a single month
        """
        # remove the " each month" part of the units
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_total()

    def get_units_from_list_to_element(self):
        """
        gets the units so that they reflect that of a single month
        """
        # replace the " each month" part of the units with "per month"
        kcals_units = self.kcals_units.replace(" each month", " per month")

        # replace the " each month" part of the units with "per month"
        fat_units = self.fat_units.replace(" each month", " per month")

        # replace the " each month" part of the units with "per month"
        protein_units = self.protein_units.replace(" each month", " per month")

        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_element(self):
        """
        sets the units so that they reflect that of a single month
        """
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_element()

    def get_units_from_element_to_list(self):
        """
        gets the units so that they reflect that of a list of months
        """
        assert "each month" not in self.kcals_units
        assert "each month" not in self.fat_units
        assert "each month" not in self.protein_units

        # add " each month" to units to signify a food list
        kcals_units = self.kcals_units + " each month"

        # add " each month" to units to signify a food list
        fat_units = self.fat_units + " each month"

        # add " each month" to units to signify a food list
        protein_units = self.protein_units + " each month"

        return [kcals_units, fat_units, protein_units]

    def set_units_from_element_to_list(self):
        """
        sets the units so that they reflect that of a list of months
        """
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_element_to_list()

    def get_units(self):
        """
        update and return the unit values as a 3 element array
        """
        self.units = [self.kcals_units, self.fat_units, self.protein_units]

        return self.units

    def set_units(self, kcals_units, fat_units, protein_units):
        """
        Sets the units of the food (for example, billion_kcals,thousand_tons, dry
        caloric tons, kcals/capita/day, or percent of global food supply).
        default units are billion kcals, thousand tons fat, thousand tons protein
        For convenience and as a memory tool, set the units, and make sure that whenever
        an operation on a different food is used, the units are compatible

        """
        self.kcals_units = kcals_units
        self.fat_units = fat_units
        self.protein_units = protein_units

        self.units = [kcals_units, fat_units, protein_units]

    # examine properties of units

    def print_units(self):
        """
        Prints the units of the nutrients
        """
        print("    kcals: ", self.kcals_units)
        print("    fat: ", self.fat_units)
        print("    protein: ", self.protein_units)

    def is_a_ratio(self):
        if (
            "ratio" in self.kcals_units
            and "ratio" in self.fat_units
            and "ratio" in self.protein_units
        ):
            return True
        else:
            return False

    def is_units_percent(self):
        if (
            "percent" in self.kcals_units
            and "percent" in self.fat_units
            and "percent" in self.protein_units
        ):
            return True
        else:
            return False

    # CONVERSIONS BETWEEN UNITS

    def in_units_billions_fed(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to billions of people fed.
        """

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        kcal_conversion = 1 / conversions.kcals_monthly
        fat_conversion = 1 / conversions.fat_monthly / 1e9
        protein_conversion = 1 / conversions.protein_monthly / 1e9

        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )
        if (
            self.kcals_units == "billion kcals per month"
            and self.fat_units == "thousand tons per month"
            and self.protein_units == "thousand tons per month"
        ):
            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: billion people fed per/each month")
            print("    fat: billion people fed per/each month")
            print("    protein: billion people fed per/each month")
            exit(0)

    def in_units_percent_fed(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to percent of people fed.
        """

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        kcal_conversion = 100 / conversions.population / 1e9
        fat_conversion = 100 / conversions.population / 1e9
        protein_conversion = 100 / conversions.population / 1e9

        if (
            self.kcals_units == "billion people fed each month"
            and self.fat_units == "billion people fed each month"
            and self.protein_units == "billion people fed each month"
        ):
            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="percent people fed each month",
                fat_units="percent people fed each month",
                protein_units="percent people fed each month",
            )
        if (
            self.kcals_units == "billion people fed per month"
            and self.fat_units == "billion people fed per month"
            and self.protein_units == "billion people fed per month"
        ):
            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="percent people fed per month",
                fat_units="percent people fed per month",
                protein_units="percent people fed per month",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: billion people fed per/each month")
            print("    fat: billion people fed per/each month")
            print("    protein: billion people fed per/each month")
            exit(0)

    def in_units_kcals_grams_gram_per_capita(
        self, kcal_ratio, fat_ratio, protein_ratio
    ):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to kcals per person per day, grams per pseron per day, kcals per person per day.
        arguments:
            kcal ratio (float): kcal  per kg of the food being converted
            fat ratio (float): grams per kcal of the food being converted
            kcal ratio (float): grams per kcal of the food being converted

        """

        # getting this instance of the UnitConversions from the child class
        # allows us to get some previously set values like kcals monthly and days in
        # month
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        kcal_conversion = (
            1e9 / conversions.days_in_month / conversions.population * kcal_ratio
        )
        fat_conversion = kcal_conversion * fat_ratio
        protein_conversion = kcal_conversion * protein_ratio

        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):

            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="kcals per person per day each month",
                fat_units="grams per person per day each month",
                protein_units="grams per person per day each month",
            )
        if (
            self.kcals_units == "billion kcals per month"
            and self.fat_units == "thousand tons per month"
            and self.protein_units == "thousand tons per month"
        ):
            Food = self.get_Food_class()
            return Food(
                kcals=self.kcals * kcal_conversion,
                fat=self.fat * fat_conversion,
                protein=self.protein * protein_conversion,
                kcals_units="kcals per person per day",
                fat_units="grams per person per day",
                protein_units="grams per person per day",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: kcals per person per day OR per day each month")
            print("    fat: grams per person per day OR per day each month")
            print("    protein: grams per person per day OR per day each month")
            exit(0)

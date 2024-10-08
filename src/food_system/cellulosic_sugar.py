"""

Functions and constants relating to cellulosic sugar production

"""

import numpy as np

from src.food_system.food import Food


class CellulosicSugar:
    def __init__(self, constants_for_params):
        """
        Initializes the CellulosicSugar object with the given constants for parameters.

        This is based on:
        https://www.sciencedirect.com/science/article/abs/pii/S0960308521001620

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None

        """
        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = (
            constants_for_params["GLOBAL_POP"] * Food.conversions.kcals_monthly / 1e9
        )

        # number of months to run the model for
        self.NMONTHS = constants_for_params["NMONTHS"]
        # multiplier for industrial foods slope
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]

        # percentage of sugar waste
        self.SUGAR_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "SUGAR"
        ]
        self.SUGAR_WASTE_RETAIL = constants_for_params["WASTE_RETAIL"]

    # papers
    def calculate_monthly_cs_production(self, constants_for_params):
        """
        Calculates the monthly production of cellulosic sugar based on the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None

        """
        # check if cellulosic sugar should be added
        if constants_for_params["ADD_CELLULOSIC_SUGAR"]:
            # create a list of zeros for the industrial delay months
            industrial_delay_months = [0] * constants_for_params["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]
            # create a list of cellulosic sugar percentage of kcals for each month
            CELL_SUGAR_PERCENT_KCALS = list(
                np.append(
                    industrial_delay_months,
                    np.array([0.0] * 5 + [4.7] * 3 + [9.5] * 1000),
                )
                * 1
                / (1 - 0.12)
                * self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
            )

            # @li we need to be able to import by-country data here

            # calculate the production of cellulosic sugar per month in billion kcals
            production_kcals_CS_per_month_long = []
            for x in CELL_SUGAR_PERCENT_KCALS:
                production_kcals_CS_per_month_long.append(
                    x
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SUGAR_WASTE_DISTRIBUTION / 100)
                )
            production_kcals_CS_per_month_long = np.array(
                production_kcals_CS_per_month_long
            )
        else:
            # if cellulosic sugar should not be added, set the production to zero
            production_kcals_CS_per_month_long = np.zeros(
                constants_for_params["NMONTHS"]
            )
        # set the production of cellulosic sugar per month to the calculated values
        self.production_kcals_CS_per_month = production_kcals_CS_per_month_long[
            0 : self.NMONTHS
        ]

        # set the production of cellulosic sugar to a Food object
        self.production = Food(
            kcals=self.production_kcals_CS_per_month,
            fat=np.zeros(len(self.production_kcals_CS_per_month)),
            protein=np.zeros(len(self.production_kcals_CS_per_month)),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

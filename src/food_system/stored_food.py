"""
############################### Stored Food ###################################
##                                                                            #
##       Functions and constants relating to stocks and stored food           #
##                                                                            #
###############################################################################
"""

from src.food_system.food import Food


class StoredFood:
    def __init__(self, constants_for_params, outdoor_crops):
        """
        Initializes the StoredFood class, a child of the Food class.
        """
        super().__init__()

        self.end_of_month_stocks = [0] * 12  # initialize the array
        self.end_of_month_stocks[0] = constants_for_params["END_OF_MONTH_STOCKS"]["JAN"]
        self.end_of_month_stocks[1] = constants_for_params["END_OF_MONTH_STOCKS"]["FEB"]
        self.end_of_month_stocks[2] = constants_for_params["END_OF_MONTH_STOCKS"]["MAR"]
        self.end_of_month_stocks[3] = constants_for_params["END_OF_MONTH_STOCKS"]["APR"]
        self.end_of_month_stocks[4] = constants_for_params["END_OF_MONTH_STOCKS"]["MAY"]
        self.end_of_month_stocks[5] = constants_for_params["END_OF_MONTH_STOCKS"]["JUN"]
        self.end_of_month_stocks[6] = constants_for_params["END_OF_MONTH_STOCKS"]["JUL"]
        self.end_of_month_stocks[7] = constants_for_params["END_OF_MONTH_STOCKS"]["AUG"]
        self.end_of_month_stocks[8] = constants_for_params["END_OF_MONTH_STOCKS"]["SEP"]
        self.end_of_month_stocks[9] = constants_for_params["END_OF_MONTH_STOCKS"]["OCT"]
        self.end_of_month_stocks[10] = constants_for_params["END_OF_MONTH_STOCKS"][
            "NOV"
        ]
        self.end_of_month_stocks[11] = constants_for_params["END_OF_MONTH_STOCKS"][
            "DEC"
        ]

        # (nuclear event in mid-may)

        self.ratio_lowest_stocks_untouched = constants_for_params[
            "RATIO_STOCKS_UNTOUCHED"
        ]
        self.percent_stored_food_to_use = constants_for_params[
            "PERCENT_STORED_FOOD_TO_USE"
        ]
        self.CROP_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "CROPS"
        ]

        self.SF_FRACTION_FAT = outdoor_crops.OG_FRACTION_FAT
        self.SF_FRACTION_PROTEIN = outdoor_crops.OG_FRACTION_PROTEIN

    def calculate_stored_food_to_use(self, starting_month):
        """
        Calculates and returns total stored food available to use at start of
        simulation. While a baseline scenario will simply use the typical amount
        of stocks to keep the buffer at a typical usage, other more extreme
        scenarios should be expected to use a higher percentage of all stored food,
        eating into the typical buffer.
        Arguments:
            starting_month (int): the month the simulation starts on.
            1=JAN, 2=FEB, ...,  12=DEC.
            (NOT TO BE CONFUSED WITH THE INDEX)

        Returns:
            float: the total stored food in millions of tons dry caloric



        The stocks listed are tabulated at the end of the month.

        The minimum of any beginning month is a reasonable proxy for the very
        lowest levels stocks reach.

        Note:
            The optimizer will run through the stocks for the duration of
            each month. So, even starting at August (the minimum month), you would
            want to use the difference in stocks at the end of the previous month
            until the end of August to determine the stocks.
        """

        assert (
            starting_month >= 1 and starting_month <= 12
        ), "ERROR: starting month must be within [1,12]"
        starting_month_index = starting_month - 1  # convert to zero indexed
        ratio_lowest_stocks_untouched = self.ratio_lowest_stocks_untouched
        fraction_stored_food_to_use = self.percent_stored_food_to_use / 100
        assert (
            fraction_stored_food_to_use >= ratio_lowest_stocks_untouched
        ), "ERROR: fraction_stored_food_to_use must be greater or equal to the ratio_lowest_stocks_untouched"
        end_of_month_stocks = self.end_of_month_stocks

        # lowest stock levels in baseline scenario (if ratio_lowest_stocks_untouched == 1)
        lowest_stocks = min(end_of_month_stocks)

        # month before simulation start
        month_before_index = starting_month_index - 1

        stocks_at_start_of_month = end_of_month_stocks[month_before_index]

        # stores at the start of the simulation
        self.TONS_DRY_CALORIC_EQIVALENT_SF = (
            stocks_at_start_of_month * fraction_stored_food_to_use
            - lowest_stocks * ratio_lowest_stocks_untouched
        )
        assert (
            self.TONS_DRY_CALORIC_EQIVALENT_SF >= 0
        ), "ERROR: Negative stored food is impossible."
        # convert to billion kcals
        self.INITIAL_SF_KCALS = self.TONS_DRY_CALORIC_EQIVALENT_SF * 4e6 / 1e9

        # convert the stored food to billion kcals
        self.initial_available = Food(
            kcals=self.INITIAL_SF_KCALS * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            fat=(
                self.INITIAL_SF_KCALS
                * self.SF_FRACTION_FAT
                * (1 - self.CROP_WASTE_DISTRIBUTION / 100)
            ),
            protein=(
                self.INITIAL_SF_KCALS
                * self.SF_FRACTION_PROTEIN
                * (1 - self.CROP_WASTE_DISTRIBUTION / 100)
            ),
            kcals_units="billion kcals",
            fat_units="thousand tons",
            protein_units="thousand tons",
        )

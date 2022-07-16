#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file runs the scenarios to test if they can be run without creating
error. This is our end to end testing.


Created on Wed Jul 13 11:54:39 2022

@author: florian
"""
import os
import sys

# Change to the same location as the original source code, so the relative
# file paths still work
os.chdir("../src/scenarios")

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.scenarios import run_model_baseline
from src.scenarios import run_baseline_by_country_no_trade
from src.scenarios import run_model_no_resilient_foods
from src.scenarios import run_model_with_resilient_foods
from src.scenarios import monte_carlo


def test_run_model_baseline():
    """
    Runs the baseline model for testing

    Arguments:

    Returns:
        None
    """
    run_model_baseline.run_model_baseline(plot_figures=False)


def test_run_baseline_by_country_no_trade():
    """
    Runs the baseline by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_baseline_by_country_no_trade.run_baseline_by_country_no_trade(
        plot_figures=False
    )


def test_run_model_no_resilient_foods():
    """
    Runs the model without resilient food for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_resilient_foods.run_model_no_resilient_foods(
        plot_figures=False
    )


def test_run_model_with_resilient_foods():
    """
    Runs the model without resilient food for testing

    Arguments:

    Returns:
        None
    """
    run_model_with_resilient_foods.run_model_with_resilient_foods(
        plot_figures=False
    )


def test_run_monte_carlo():
    """
    Runs the monte carlo model for testing

    Arguments:

    Returns:
        None
    """
    #TBD
    pass

if __name__ == "__main__":
    test_run_model_baseline()
    test_run_baseline_by_country_no_trade()
    test_run_model_no_resilient_foods()
    test_run_model_with_resilient_foods()
    test_run_monte_carlo()

    print("All tests passed")
    sys.exit(0)
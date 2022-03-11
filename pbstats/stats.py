import numpy as np
import pandas as pd

def display_statistics_table(augmented_visit_df):
    flower_statistics = augmented_visit_df.groupby("Flower").agg({'Visit Duration (s)':['mean','count']})

    flower_statistics

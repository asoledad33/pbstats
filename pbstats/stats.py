import numpy as np
import pandas as pd

def show_statistics_table(augmented_visit_df):
    flower_statistics = augmented_visit_df.groupby("Flower").agg({'Visit Duration (s)':['mean','count']})

    return flower_statistics

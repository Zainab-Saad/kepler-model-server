import smogn
import pandas as pd
import numpy as np
import ImbalancedLearningRegression as iblr



Y = 'platform_power'

# Function to add Gaussian noise directly to the specified column
def add_gaussian_noise(df, column, mean=0, std=1):
    noise = np.random.normal(mean, std, df[column].shape)
    df[column] += noise
    return df

# Function to apply noise multiple times to all specified columns
def apply_noise_multiple_times(df, columns, mean=0, std=1, times=5):
    augmented_dfs = []
    for _ in range(times):
        noisy_df = df.copy()
        for column in columns:
            noisy_df = add_gaussian_noise(noisy_df, column, mean, std)
        augmented_dfs.append(noisy_df)
    return pd.concat(augmented_dfs, ignore_index=True)



def apply_smogn_augmentation(df):
    """
    refer to this:
    https://github.com/nickkunz/smogn/blob/master/examples/smogn_example_3_adv.ipynb
    """
    # Determine the min and max values for platform_power
    min_value = df['platform_power'].min()
    max_value = df['platform_power'].max()

    # Create a relevance matrix with realistic values
    rg_mtrx = [
        [min_value, 1, 0],    # over-sample at the lower end
        [(min_value + max_value) / 4, 0, 0],  # under-sample lower middle
        [(min_value + max_value) / 2, 0, 0],  # under-sample middle
        [max_value, 0, 0],    # under-sample at the higher end
    ]

  

    df_smogn = smogn.smoter(
    
    ## main arguments
    data = df,           ## pandas dataframe
    y = 'platform_power',          ## string ('header name')
    k = 7,                    ## positive integer (k < n)
    pert = 0.04,              ## real number (0 < R < 1)
    samp_method = 'extreme',  ## string ('balance' or 'extreme')
    drop_na_col = True,       ## boolean (True or False)
    drop_na_row = True,       ## boolean (True or False)
    replace = False,          ## boolean (True or False)

    ## phi relevance arguments
    rel_thres = 0.10,         ## real number (0 < R < 1)
    rel_method = 'manual',    ## string ('auto' or 'manual')
    # rel_xtrm_type = 'both', ## unused (rel_method = 'manual')
    # rel_coef = 1.50,        ## unused (rel_method = 'manual')
    rel_ctrl_pts_rg = rg_mtrx ## 2d array (format: [x, y])

)
    return df_smogn
     

def apply_iblr_augmentation(df):
    data_oversampled = iblr.ro(data = df, y = Y)
    return data_oversampled
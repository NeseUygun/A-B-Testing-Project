#####################################################
# Comparison of Conversion of Bidding Methods with AB Test
#####################################################

#####################################################
# Bussines Problem
#####################################################

# Meta recently introduced a new type of bidding called "average bidding" to an existing bidding type called "maximumbidding" as an alternative.
# One of our customers, X company,decided to test this new feature and the company wants to do an A/B test to see if it will bring more gain or not 
# A/B testing continues for 1 month and X company now expects you to analyze the results of this A/B test.
# The ultimate success criterion is Purchase for the company. Therefore, the focus should be on the Purchase metric for statistical testing.


#####################################################
# Dataset History
#####################################################

#In this data set, which includes the website information of a company, there is information such as the number of advertisements that users see and click, as well as earnings information from here.
# There are two separate data sets that contain control group and test group. These datasets are on separate pages of ab_testing.xlsxexcel. 
# Maximum Bidding was applied to the control group and AverageBidding was applied to the test group.

# impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase: Number of products purchased after ads clicked
# Earning: Earnings after purchased products

#####################################################
# Project Tasks
#####################################################

#####################################################
# Task 1:  Preparing and Analyzing Data
#####################################################

# Step 1: Read the data set ab_testing_data.xlsx consisting of control and test group data. Assign control and test group data to separate variables.

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("/Datasets/ab_testing.xlsx", sheet_name="Control Group")
dataframe_test = pd.read_excel("/Datasets/ab_testing.xlsx", sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Step 2: Analyze control and test group data.


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


# Step 3: After the analysis process, combine the control and test group data using the concat method.

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()



#####################################################
# Task 2:  Defining the A/B Test Hypothesis
#####################################################

# Step 1: Define the Hypothesis.

# H0 : M1 = M2 (There is no difference between the purchasing averages of the control group and the test group.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and the test group.)


# Adım 2: Analyze the purchase averages for the control and test group

df.groupby("group").agg({"Purchase": "mean"})



#####################################################
# Task 3: Performing Hypothesis Testing
#####################################################

# Step 1: Perform hypothesis checks before hypothesis testing. These are Assumption of Normality and Homogeneity of Variance.

# Test separately whether the control and test groups comply with the normality assumption, over the Purchase variable.
# Assumption of Normality :
# H0: Assumption of normal distribution is provided.
# H1: Normal distribution assumption is not provided
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CAN NOT REJECTED
# Is the assumption of normality according to the test result provided for the control and test groups?
#  Interpret the p-values is obtained.


test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO cannot be rejected. The values of the control group provide the assumption of normal distribution.


# Homogeneity of Variance :
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CANNOT REJECTED
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
# Is the assumption of normality provided according to the test result? Interpret the p-values obtained.

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO cannot be rejected. The values of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are homogeneous.

# Step 2: Select the appropriate test according to the Normality Assumption and Variance Homogeneity results

# Since the assumptions are provided, an independent two-sample t-test (parametric test) should be performed.
# H0: M1 = M2 (There is no statistically significant difference between the averages of purchasing the control group and test group.)
# H1: M1 != M2 (there is statistically significant difference between the averages of purchasing the control group and test group.)
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CANNOT REJECTED

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Step 3: Interpret whether there is a statistically significant difference between the averages of purchasing the control group and test group by considering the p_value

# p-value=0.3493
# HO cannot be rejected. There is no statistically significant difference between the purchasing averages of the control and test groups.


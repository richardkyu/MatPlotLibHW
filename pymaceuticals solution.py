
#%%
# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
load_mouse_drug_data = "data/mouse_drug_data.csv"
trial_data_clinical = "data/clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
m_df = pd.read_csv(load_mouse_drug_data)
clinical_df = pd.read_csv(trial_data_clinical)

# Combine the data into a single dataset
merged_dataset = pd.merge(clinical_df, m_df, how='outer', on='Mouse ID')

# Display the data table for preview
merged_dataset.head()

#%% [markdown]
# ## Tumor Response to Treatment

#%%
# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
t_avg = merged_dataset.groupby(['Drug', 'Timepoint']).mean()['Tumor Volume (mm3)']

# Convert to DataFrame
t_avg_df = pd.DataFrame(t_avg)


#%%
# Preview DataFrame
t_avg_df


#%%
# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
tu_error = merged_dataset.groupby(['Drug', 'Timepoint']).sem()['Tumor Volume (mm3)']
# Convert to DataFrame
tu_err_df = pd.DataFrame(tu_error)
# Preview DataFrame
tu_err_df.head()


#%%



#%%
# Minor Data Munging to Re-Format the Data Frames
reformat_data = t_avg_df.reset_index()
pivotting = reformat_data.pivot(index='Timepoint', columns='Drug')['Tumor Volume (mm3)']

reformat_err = tu_err_df.reset_index()
pivot_err = reformat_err.pivot(index='Timepoint', columns='Drug')['Tumor Volume (mm3)']


# Preview that Reformatting worked
display(pivotting.head())


#%%



#%%
# Generate the Plot (with Error Bars)
x_axis = np.arange(0, 50, 10)
x_limit = 45

plt.figure(figsize=(6,4))

plt.errorbar(pivotting.index, pivotting["Capomulin"], yerr=pivot_err["Capomulin"],             color="r", marker="o", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotting.index, pivotting["Infubinol"], yerr=pivot_err["Infubinol"],             color="b", marker="^", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotting.index, pivotting["Ketapril"],yerr=pivot_err["Ketapril"],             color="g", marker="s", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotting.index, pivotting["Placebo"],yerr=pivot_err["Placebo"],             color="k", marker="d", markersize=5, linestyle="dashed", linewidth=0.50)


# plt.ylim(20, 80)
# plt.xlim(0, 45)

# Set x and y axis labels including the title of the chart

plt.title("Tumor Response to Treatment")# Give plot main title
plt.xlabel("Time (Days)") # set text for the x axis
plt.ylabel("Tumor Volume (mm3)") # set text for the y axis

plt.style.use('seaborn-whitegrid')
plt.grid(linestyle="dashed")

plt.grid(linestyle="dashed")
plt.legend(loc='best', fontsize=12, fancybox=True)

# Save the figure
plt.savefig("TumorResponseTreatment.png")


#%%
# Show the Figure
plt.show()

#%% [markdown]
# ## Metastatic Response to Treatment

#%%
# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
meta_avg = merged_dataset.groupby(['Drug', 'Timepoint']).mean()['Metastatic Sites']

# Convert to DataFrame
meta_avg_df = pd.DataFrame(meta_avg)


#%%
# Preview DataFrame
meta_avg_df.head()


#%%
# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
meta_err = merged_dataset.groupby(['Drug', 'Timepoint']).sem()['Metastatic Sites']

# Convert to DataFrame
meta_err_df = pd.DataFrame(meta_err)


#%%
# Preview DataFrame
meta_err_df.head()


#%%
# Minor Data Munging to Re-Format the Data Frames
mavg_reformat = meta_avg_df.reset_index()
mavg_pivot = mavg_reformat.pivot(index='Timepoint', columns='Drug')['Metastatic Sites']

merr_reformat = meta_err_df.reset_index()
meror_pivot = merr_reformat.pivot(index='Timepoint', columns='Drug')['Metastatic Sites']


#%%
# Preview that Reformatting worked
pivotting.head()


#%%
# Generate the Plot (with Error Bars)

plt.errorbar(m_avg_pivot.index, m_avg_pivot["Capomulin"], yerr=meror_pivot["Capomulin"],             color="r", marker="o", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Infubinol"], yerr=meror_pivot["Infubinol"],             color="b", marker="^", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Ketapril"],yerr=meror_pivot["Ketapril"],             color="g", marker="s", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Placebo"],yerr=meror_pivot["Placebo"],             color="k", marker="d", markersize=5, linestyle="dashed", linewidth=0.50)


# Set x and y axis labels including the title of the chart
plt.title('Metastatic Spread During Treatment') # Give plot main title
plt.xlabel('Treatment Duration (Days)') # set text for the x axis
plt.ylabel('Metastatic Sites') # set text for the y axis

plt.style.use('seaborn-whitegrid')
plt.grid(linestyle="dashed")
plt.legend(loc='best', fontsize=12, fancybox=True)


# Save the Figure
plt.savefig("MetastaticSpreadDuringTreatment.png")


#%%
# Show the Figure
plt.show()

#%% [markdown]
# ## Survival Rates

#%%
# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
mice_count = merged_dataset.groupby(["Drug", "Timepoint"]).count()['Mouse ID']

# Convert to DataFrame
mice_count_df = pd.DataFrame({"Mouse Count": mice_count})



#%%
# Preview DataFrame
mice_count_df.head()


#%%
# Minor Data Munging to Re-Format the Data Frames
mice_reformat = mice_count_df.reset_index()
mice_pivot = mice_reformat.pivot(index='Timepoint', columns='Drug')['Mouse Count']


#%%
# Preview the Data Frame
mice_pivot.head()


#%%
# Generate the Plot (Accounting for percentages)
plt.plot(100 * mice_pivot["Capomulin"] / 25, "ro", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(100 * mice_pivot["Infubinol"] / 25, "b^", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(100 * mice_pivot["Ketapril"] / 25, "gs", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(100 * mice_pivot["Placebo"] / 25 , "kd", linestyle="dashed", markersize=6, linewidth=0.50)


plt.title("Survival During Treatment") # Give plot main title
plt.ylabel("Survival Rate (%)") # set text for the y axis
plt.xlabel("Time (Days)") # set text for the x axis
plt.grid(True)
plt.legend(loc="best", fontsize="small", fancybox=True)

# Save the Figure
plt.savefig("SurvivalDuringTreatment.png")


#%%
# Show the Figure
plt.show()

#%% [markdown]
# ## Summary Bar Graph

#%%
# Calculate the percent changes for each drug
percent_change =  100 * (pivotting.iloc[-1] - pivotting.iloc[0]) / pivotting.iloc[0]
pct_change_sem =  100 * (pivot_err.iloc[-1] - pivot_err.iloc[0]) / pivot_err.iloc[0]


#%%
# Display the data to confirm
display(percent_change)


#%%
# Store all Relevant Percent Changes into a Tuple
pct_changes = (percent_change["Capomulin"], 
               percent_change["Infubinol"], 
               percent_change["Ketapril"], 
               percent_change["Placebo"])


# Splice the data between passing and failing drugs
fig, ax = plt.subplots()
ind = np.arange(len(pct_changes))  
width = 1
rectsPass = ax.bar(ind[0], pct_changes[0], width, color='green')
rectsFail = ax.bar(ind[1:], pct_changes[1:], width, color='red')

# Orient widths. Add labels, tick marks, etc. 
ax.set_ylabel('% Tumor Volume Change')
ax.set_title('Tumor Change Over 45 Day Treatment')
ax.set_xticks(ind + 0.5)
ax.set_xticklabels(('Capomulin', 'Infubinol', 'Ketapril', 'Placebo'))
ax.set_autoscaley_on(False)
ax.set_ylim([-30,70])
ax.grid(True)

# Use functions to label the percentages of changes
def autolabelFail(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 3,
                '%d%%' % int(height),
                ha='center', va='bottom', color="white")

def autolabelPass(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., -8,
                '-%d%% ' % int(height),
                ha='center', va='bottom', color="white")

# Call functions to implement the function calls
autolabelPass(rectsPass)
autolabelFail(rectsFail)

# Save the Figure
fig.savefig("Tumor_Change.png")


#%%
# Show the Figure
fig.show()


#%%




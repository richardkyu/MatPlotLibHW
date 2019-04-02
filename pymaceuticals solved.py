#!/usr/bin/env python
# coding: utf-8

# In[2]:


# dependencies to use
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pprint import pprint

# load files from the data folder
mouse_drug_data = "data/mouse_drug_data.csv"
clinicaltrial_data = "data/clinicaltrial_data.csv"

# make dataframe into mouse and clinical trial from data folder.
m_df = pd.read_csv(mouse_drug_data)
clinical_df = pd.read_csv(clinicaltrial_data)

# merge the datasets on Mouse ID
merged_dataset = clinical_df.merge(m_df, how='outer', on='Mouse ID')

# display
merged_dataset.head()
#display(merged_dataset["Mouse ID"].value_counts().head())


#  ## Tumor Response to Treatment

# In[3]:


# mean tumor volume ->groupby -> time and drug
t_avg = merged_dataset.groupby(['Drug', 'Timepoint']).mean()['Tumor Volume (mm3)']

# conversion to dataframe object from groupby object
t_avg_df = pd.DataFrame(t_avg)


# In[4]:


# show the dataframe after conversion
display(t_avg_df)


# In[5]:


# groupby drug and timepoint for tumor groups
tu_error = merged_dataset.groupby(['Drug', 'Timepoint']).sem()['Tumor Volume (mm3)'] #SEM = standard error of mean
# conversion of groupby to dataframe object, same as above
t_err_df = pd.DataFrame(tu_error)



# In[6]:


#display
t_err_df.head()


# In[7]:


# reset and reformat datafames in order to make sure the data looks readable.
reformat_data = t_avg_df.reset_index()
pivotted = reformat_data.pivot(index='Timepoint', columns='Drug')['Tumor Volume (mm3)']

reformat_err = t_err_df.reset_index()
pivotted_err = reformat_err.pivot(index='Timepoint', columns='Drug')['Tumor Volume (mm3)']



# In[8]:


# display to check 
display(pivotted.head())


# In[9]:


# Generate the Plot (with Error Bars)
x_axis = np.arange(0, 50, 10)
x_limit = 45

plt.figure(figsize=(6,4))

plt.errorbar(pivotted.index, pivotted["Capomulin"], yerr=pivotted_err["Capomulin"], color="red", marker="o", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotted.index, pivotted["Infubinol"], yerr=pivotted_err["Infubinol"], color="blue", marker="^", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotted.index, pivotted["Ketapril"],yerr=pivotted_err["Ketapril"], color="green", marker="s", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(pivotted.index, pivotted["Placebo"],yerr=pivotted_err["Placebo"], color="k", marker="d", markersize=5, linestyle="dashed", linewidth=0.50)



# Chart formatting
plt.style.use('seaborn-whitegrid')
plt.grid(linestyle="dashed")

plt.title("Tumor Response to Treatment")# set title
plt.xlabel("Time (Days)") # set x axis
plt.ylabel("Tumor Volume (mm3)") # set y axis

plt.grid(linestyle="dashed")
plt.legend(loc='best', fontsize=12)

# Save the figure
plt.savefig("tumor_response_to_treatment.png")


# In[10]:


# Show the Figure
plt.show()


#  ## Metastatic Response to Treatment

# In[11]:


# use same method as the above tumor response to treatment
meta_avg = merged_dataset.groupby(['Drug', 'Timepoint']).mean()['Metastatic Sites']
meta_avg_df = pd.DataFrame(meta_avg)


# In[12]:


#display
meta_avg_df.head(20)


# In[13]:


#same method as above 
meta_err = merged_dataset.groupby(['Drug', 'Timepoint']).sem()['Metastatic Sites']
meta_err_df = pd.DataFrame(meta_err)


# In[14]:


#show
meta_err_df.head()


# In[15]:


# same reformatting method as for tumor treatment graphs
mavg_reformat = meta_avg_df.reset_index()
m_avg_pivot = mavg_reformat.pivot(index='Timepoint', columns='Drug')['Metastatic Sites']

merr_reformat = meta_err_df.reset_index()
merror_pivot = merr_reformat.pivot(index='Timepoint', columns='Drug')['Metastatic Sites']


# In[16]:


# show
mavg_reformat.head()


# In[17]:


# generate plot along with errorbars.

plt.errorbar(m_avg_pivot.index, m_avg_pivot["Capomulin"], yerr=merror_pivot["Capomulin"],  color="red", marker="o", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Infubinol"], yerr=merror_pivot["Infubinol"],  color="blue", marker="^", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Ketapril"],yerr=merror_pivot["Ketapril"], color="green", marker="s", markersize=5, linestyle="dashed", linewidth=0.50)
plt.errorbar(m_avg_pivot.index, m_avg_pivot["Placebo"],yerr=merror_pivot["Placebo"],color="k", marker="d", markersize=5, linestyle="dashed", linewidth=0.50)


# settings for the graph
plt.style.use('seaborn-whitegrid')
plt.grid(linestyle="dashed")
plt.legend(loc='best', fontsize=12)


# titles for the graph and axes
plt.title('Metastatic Spread During Treatment') 
plt.xlabel('Treatment Duration (Days)') 
plt.ylabel('Metastatic Sites') 


# save figure to folder
plt.savefig("metastatic_spread_during_treatment.png")


# In[ ]:


# show figure
plt.show()


#  ## Survival Rates

# In[18]:


# use the same method as for tumor treatment and metastatic sites
mice_counts = merged_dataset.groupby(["Drug", "Timepoint"]).count()['Mouse ID']
mice_counts_df = pd.DataFrame({"Mouse Count": mice_counts})



# In[19]:


# show 
#mice_count_df.head(10)
mice_counts_df.head(20)


# In[20]:


mice_reformat = mice_counts_df.reset_index()
mice_pivot = mice_reformat.pivot(index='Timepoint', columns='Drug')['Mouse Count']


# In[21]:


#show df
mice_pivot.head()


# In[24]:


# generate plot (100% /25 = 4)
plt.plot(mice_pivot["Capomulin"] *4, "ro", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(mice_pivot["Infubinol"] *4, "b^", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(mice_pivot["Ketapril"] *4, "gs", linestyle="dashed", markersize=5, linewidth=0.50)
plt.plot(mice_pivot["Placebo"] *4 , "kd", linestyle="dashed", markersize=5, linewidth=0.50)

plt.grid(True)
plt.legend()

plt.title("Survival During Treatment")
plt.ylabel("Survival Rate (%)")
plt.xlabel("Time (Days)")
# save the figure
plt.savefig("mice_survival_during_treatment.png")


# In[25]:


# show plot
plt.show()


#  ## Summary Bar Graph

# In[26]:


# store and calculate percent changes
percent_change = (pivotted.iloc[-1] - pivotted.iloc[0]) / pivotted.iloc[0] *100
pct_change_sem = (pivotted_err.iloc[-1] - pivotted_err.iloc[0]) / pivotted_err.iloc[0] *100


# In[27]:


# display % change
display(percent_change)


# In[28]:


# store % changes into a tuple
pct_change = (percent_change["Capomulin"], 
               percent_change["Infubinol"], 
               percent_change["Ketapril"], 
               percent_change["Placebo"])


# combine data between successful and failing drugs
fig, ax = plt.subplots()
ind = np.arange(len(pct_change))  
width = 1
rectsPass = ax.bar(ind[0], pct_change[0], width, color='green')
rectsFail = ax.bar(ind[1:], pct_change[1:], width, color='red')

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

# save figure to folder
fig.savefig("tumor_drug_success.png")


# In[29]:


# display figure
fig.show()


# In[ ]:






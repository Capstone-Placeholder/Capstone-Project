# import pandas and numpy
import pandas as pd
import numpy as np
# statistical analysis imports
from math import sqrt
from scipy import stats
# viz imports
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib as mpl
import seaborn as sns
from cycler import cycler
# default viz size settings
sns.set(rc={'figure.figsize':(14, 10)})
sns.set_context("talk", rc={"font.size":14,"axes.titlesize":18,"axes.labelsize":14}) 
plt.rc('figure', figsize=(14, 10))
plt.rc('font', size=12)
mpl.rcParams['font.size'] = 14
mpl.rcParams['figure.figsize'] = 14, 10
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.linestyle'] = '--'
mpl.rcParams['axes.prop_cycle'] = cycler(color=['deepskyblue', 'firebrick', 'darkseagreen', 'violet'])

def explicit_viz(df):
    '''
    This function produces a swarm plot on explicit tracks' and non-explicit tracks' popularity.
    '''
    #print('Does a track being explicit or not correlate with its popularity?')
    sns.catplot(x="explicit", y="popularity", kind="swarm", data=df, height=8, aspect=1)
    plt.title(label="Does a track being explicit or not correlate with its popularity?")
    plt.show()

def explicit_ttest(df, alpha=0.05):
    '''
    This function takes in a DataFrame and an alpha value (default is .05)
    and prints off the Independent T-Test to compare mean popularity
    of explicit tracks versus non-explicit tracks.
    '''
    print('Set the alpha/significance level:')
    print('  alpha =', alpha)
    
    print('\n---\n')
    
    print('Check for normal distribution:')
    sns.distplot(df.popularity)
    plt.show()
    
    print('---\n')
    
    print('Check values counts:')
    print(df.explicit.value_counts())
    
    print('\n---\n')
    
    print('Compare variances:')
    explicit_sample = df[df.explicit==True].popularity
    not_explicit_sample = df[df.explicit==False].popularity
    
    # if [results of lavenes variance test], then equal_var = __ (automate checking similar variance)
    print(explicit_sample.var())
    print(not_explicit_sample.var())
          
    print("They are of relatively equal variance, so we will set the argument of equal_var to True. After the MVP this will be done with the Levene test instead of by hand.")
    
    print('\n---\n')
          
    print("Compute test statistic and probability (t-statistic & p-value)")
    t, p = stats.ttest_ind(explicit_sample, not_explicit_sample, equal_var = True)
    print('Test statistic:', t, '\np-value:', p/2, '\nalpha:', alpha)
    
    print('\n---\n')
    
    null_hypothesis = "there is no significant difference between the mean popularity of explicit tracks and non-explicit tracks."
    if p/2 < alpha:
        print("We reject the hypothesis that", null_hypothesis)
    else:
        print("We fail to reject the null hypothesis.")
        
    print('\n---\n')
          
    print('mean of non-explicit songs:', not_explicit_sample.mean(), '\nmean of explicit songs:', explicit_sample.mean())

def corr_heatmap(train):
    '''
    This function creates a heatmap of the correlation of all features.
    Takes in a DataFrame as an argument.
    '''
    # put popularity in first position
    heatmap_data = train
    first_col = heatmap_data.pop("popularity")
    heatmap_data.insert(0, "popularity", first_col)

    # create correlation heatmap
    corr = heatmap_data.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    ax = sns.heatmap(corr, mask=mask, center=0, cmap=sns.diverging_palette(95, 220, n=250, s=93, l=35), square=True) 
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, horizontalalignment='right')
    plt.title('Which features have significant linear correlation?')
    ax

def danceability_viz(train):
    '''
    Produces visualizations that answer the question:
    Is there a difference in mean popularity across dancebility bins?
    '''
    # First Viz
    # visualizing each observation by release date and popularity
    plt.figure(figsize=(12,6))

    sns.scatterplot(x=train.danceability, y=train.popularity)
    # reference line for overall popularity average
    plt.axhline(train.popularity.mean(),linestyle='-',label='Train Popularity Average', color='black')
    plt.axvline(train.danceability.mean(), linestyle='--',label='Train Danceability Average', color='black')

    plt.title('Danceability vs. Popularity', size=15)

    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.show()

    # line break
    print("\n")

    # Second Viz
    # bin danceability for better visualizing
    train['dance_bins'] = pd.qcut(x=train.danceability, q=3, labels=['low','medium','high'])

    # to plot reference line of overall train average popularity
    popularity_rate = train.popularity.mean()

    plt.figure(figsize=(12,6))

    # plots the average of each features subgroups as bar plots
    sns.barplot('popularity', 'dance_bins', data=train, alpha=.8)
    plt.xlabel('')
    plt.ylabel('Danceability Bins', size=13)
    plt.title('Popularity Rate by Danceability', size=16)
    plt.axvline(popularity_rate, ls='--', color='grey', label='Overall Average')

    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.tight_layout()
    plt.show()

def release_dates_viz(train):
    ''''
    Produces visualizations that answer the question:
    Does a track's release year, release month, or release day have an impact on its popularity?
    '''
    # visualizing average popularity by each features category
    features = ['release_year', 'release_month', 'release_day']

    # to plot reference line of overall train average popularity
    avg_popularity = train.popularity.mean()

    # plots the average of each features subgroups as bar plots
    _, ax = plt.subplots(nrows=3, ncols=1, figsize=(16, 12), sharey=True)
    for i, feature in enumerate(features):
        
        sns.barplot(feature, 'popularity', data=train, ax=ax[i], alpha=.8)
        ax[i].set_xlabel('')
        ax[i].set_ylabel('Popularity Level', size=13)
        ax[i].set_title(feature, size=16)
        ax[i].axhline(avg_popularity, ls='--', color='grey')
        plt.tight_layout()
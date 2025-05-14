import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from scipy.stats import sem, ttest_ind




def add_columns(data):
    data['virus_bacteria_ratio'] = data['viral_reads'] / data['bacteria_reads']
    
def to_group1(filename):
    return filename.split('-')[1][-1]

def to_person1(filename):
    return filename.split('-')[0]

def get_comp1_data(data, full_title=False):
    comp1 = ["9092-U-virome_S11_L001",
    "9092-1Q-virome_S3_L001",
    "9092-2Z-virome_S1_L001",
    "2820-U-virome_S14_L001",
    "2820-2Q-virome_S8_L001",
    "2820-2Z-virome_S2_L001",
    "9324-U-virome_S12_L001",
    "9324-2Q-virome_S5_L001",
    "9324-2Z-virome_S4_L001",
    "0168-U-virome_S13_L001",
    "0168-1Q-virome_S7_L001",
    "0168-1Z-virome_S6_L001",
    "8466-U-virome_S17_L001",
    "8466-1Q-virome_S10_L001",
    "8466-2Z-virome_S9_L001"]

    name_map = {
        'U': 'A',
        'Q': 'A.0.2',
        'Z': 'A.0.1'
    }
    
    name_map_full = {
        'U': 'A (Baseline)',
        'Q': 'A.0.2 (All Prep Power Viral DNA/RNA kit)',
        'Z': 'A.0.1 (ZymoBIOMICS DNA/RNA Multiprep kit)'
    }
    
    comp1_data = data[data['filename'].isin(comp1)]
    comp1_data['Group'] = comp1_data.apply(lambda x: to_group1(x['filename']), axis=1)
    if full_title:
        comp1_data['Group'] = comp1_data.apply(lambda x: name_map_full[x['Group']], axis=1)
    else:
        comp1_data['Group'] = comp1_data.apply(lambda x: name_map[x['Group']], axis=1)

    comp1_data['Individual'] = comp1_data.apply(lambda x: to_person1(x['filename']), axis=1)
    return comp1_data

def to_group4(filename):
    return filename.split('-')[2].split('_')[0]

def to_person4(filename):
    return filename.split('-')[0]

def get_comp4_data(data, full_title=False):
    comp4 = ['S1-5393-VIROME_S1_L001',
    'S1-5393-viromeTruSeq',
    'S3-9504-VIROME_S3_L001',
    'S3-9504-viromeTruSeq',
    'S4-1876-VIROME_S4_L001',
    'S4-1876-viromeTruSeq',
    '14-2820AC-VIROME_S5_L001',
    '14-2820AC-viromeTruSeq',
    '15-8466AC-VIROME_S6_L001',
    '15-8466AC-viromeTruSeq']
    
    name_map = {
    'VIROME': 'A',
    'viromeTruSeq': 'A.3'
    }
    name_map_full = {
    'VIROME': 'A (Baseline)',
    'viromeTruSeq': 'A.3 (TruSeq Nano DNA Library Prep)'
    }

    comp4_data = data[data['filename'].isin(comp4)]
    comp4_data['Group'] = comp4_data.apply(lambda x: to_group4(x['filename']), axis=1)
    if full_title:
        comp4_data['Group'] = comp4_data.apply(lambda x: name_map_full[x['Group']], axis=1)
    else:
        comp4_data['Group'] = comp4_data.apply(lambda x: name_map[x['Group']], axis=1)
    comp4_data['Individual'] = comp4_data.apply(lambda x: to_person4(x['filename']), axis=1)
    return comp4_data
    
def to_group6(filename):
    return filename.split('-')[2]

def to_person6(filename):
    return filename.split('-')[0]

def get_comp6_data(data, full_title=False):
    comp6_data = data[data['filename'].str[0] == 'P']
    comp6_data = comp6_data[comp6_data['filename'].str[8:11] != 'Qds']
    
    name_map = {
    'I': 'A.4',
    'Q': 'A',
    'Ids': 'A.4.1'
    }
    name_map_full = {
    'I': 'A.4 (PureLink Viral RNA/DNA mini kit)',
    'Q': 'A (Baseline)',
    'Ids': 'A.4.1 (Purelink + cDNA synthesis)'
    }
        
    comp6_data['Group'] = comp6_data.apply(lambda x: to_group6(x['filename']), axis=1)
    if full_title:
        comp6_data['Group'] = comp6_data.apply(lambda x: name_map_full[x['Group']], axis=1)
    else:
        comp6_data['Group'] = comp6_data.apply(lambda x: name_map[x['Group']], axis=1)
    comp6_data['Individual'] = comp6_data.apply(lambda x: to_person6(x['filename']), axis=1)
    return comp6_data

def to_group2(filename):
    return filename.split('-')[0][1]

def to_person2(filename):
    return filename.split('-')[0][3]

def get_comp2_data(data, full_title=False):
    comp2 = ['SAC1-viromeR_S55_L001',
    'SAC2-viromeR_S56_L001',
    'SBC1-virome',
    'SBC2-virome']
    
    name_map = {
    'A': 'A',
    'B': 'A.1',
    }
    name_map_full = {
    'A': 'A (Baseline)',
    'B': 'A.1 (PEG-6000)',
    }

    comp2_data = data[data['filename'].isin(comp2)].drop_duplicates()
    comp2_data['Group'] = comp2_data.apply(lambda x: to_group2(x['filename']), axis=1)
    if full_title:
        comp2_data['Group'] = comp2_data.apply(lambda x: name_map_full[x['Group']], axis=1)
    else:
        comp2_data['Group'] = comp2_data.apply(lambda x: name_map[x['Group']], axis=1)
    comp2_data['Individual'] = comp2_data.apply(lambda x: to_person2(x['filename']), axis=1)
    return comp2_data
    
def to_group3(filename):
    return filename.split('-')[0][2]

def to_person3(filename):
    return filename.split('-')[0][3]

def get_comp3_data(data, full_title=False):
    comp3 = ['SAC1-viromeR_S55_L001',
    'SAC2-viromeR_S56_L001',
    'SAD1-viromeR_S61_L001',
    'SAD2-virome']
    
    name_map = {
    'C': 'A',
    'D': 'A.2',
    }
    name_map_full = {
    'C': 'A (Baseline)',
    'D': 'A.2 (MDA Amplification)',
    }

    comp3_data = data[data['filename'].isin(comp3)].drop_duplicates()
    comp3_data['Group'] = comp3_data.apply(lambda x: to_group3(x['filename']), axis=1)

    if full_title:
        comp3_data['Group'] = comp3_data.apply(lambda x: name_map_full[x['Group']], axis=1)
    else:
        comp3_data['Group'] = comp3_data.apply(lambda x: name_map[x['Group']], axis=1)

    comp3_data['Individual'] = comp3_data.apply(lambda x: to_person3(x['filename']), axis=1)
    return comp3_data
    

def calculate_fold_change(df, control_group, test_group, stat):
    control_mean = df[df['Group'] == control_group][stat].mean()
    test_mean = df[df['Group'] == test_group][stat].mean()
    fold_change = test_mean / control_mean
    return np.log(fold_change)

def calculate_p_value(df, control_group, test_group, stat):
    control_values = df[df['Group'] == control_group][stat]
    test_values = df[df['Group'] == test_group][stat]
    _, p_value = ttest_ind(control_values, test_values, equal_var=False)  # Use Welch's t-test
    return p_value

def calculate_fold_change_with_stats(df, control_group, test_group, stat):
    control_values = df[df['Group'] == control_group][stat]
    test_values = df[df['Group'] == test_group][stat]
    mean_control = np.mean(control_values)
    mean_test = np.mean(test_values)
    fold_change = mean_test / mean_control
    std_control = np.std(control_values)
    std_test = np.std(test_values)
    return fold_change, std_control, std_test

def calculate_individual_fold_changes(df, control_group, test_group, stat):
    control_values = df[df['Group'] == control_group].set_index('Individual')[stat]
    test_values = df[df['Group'] == test_group].set_index('Individual')[stat]
    # Align indices and calculate fold changes
    fold_changes = np.log2(test_values / control_values)
    return fold_changes.dropna()  # Drop NaN values due to mismatched individuals

def fold_change(dataframes, control_groups, group_labels, stats, stats_label):
# List of dataframes and their respective control groups

    # Initialize lists for terms, coefficients, and confidence intervals
    terms = []
    coefs = []
    lowers = []
    uppers = []
    groups = []

    # Keep track of the index to know where to draw separating lines
    index = 0
    separation_indices = []

    # Iterate over each dataframe and its control group
    for df, control_group, group_label in zip(dataframes, control_groups, group_labels):
        test_groups = df['Group'].unique()
        test_groups = test_groups[test_groups != control_group]

        for group in test_groups:
            for stat in stats:
                individual_fold_changes = calculate_individual_fold_changes(df, control_group, group, stat)
                fold_change_mean = np.mean(individual_fold_changes)
                fold_change_std = np.std(individual_fold_changes)
                
                terms.append(f"{stat} ({group})")
                coefs.append(fold_change_mean)
                
                std_error = fold_change_std / np.sqrt(len(individual_fold_changes))
                lowers.append(fold_change_mean - 1.96 * std_error)  # 95% CI lower bound
                uppers.append(fold_change_mean + 1.96 * std_error)  # 95% CI upper bound
                groups.append(group_label)
                index += 1
        
        separation_indices.append(index - 0.5)  # Store the index to draw separation lines

    # Plotting the forest plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot horizontal lines for confidence intervals
    for i in range(len(terms)):
        ax.plot([lowers[i], uppers[i]], [i, i], color='black')
        ax.plot(coefs[i], i, 'ro')  # Point estimate

    # Add vertical lines to separate different dataframes' comparisons
    for sep_index in separation_indices:
        ax.axhline(y=sep_index, color='black', linestyle='-', linewidth=1)

    # Formatting the plot
    ax.set_yticks(range(len(terms)))
    ax.set_yticklabels([f"{term.split()[1][1:-1]} [{group}]" for term, group in zip(terms, groups)])
    ax.axvline(x=0, linestyle='--', color='grey', linewidth=1)  # Reference line at 0
    ax.set_xlabel('Log Fold Change')
    ax.set_title(f'Log Fold Change of {stats_label} over baseline')

    plt.show()
    
def multiple_fold_changes(dataframes, control_groups, group_labels, stats, stats_labels, fold_change_sig=1, p_val=0.05, plot_controls=True, partial_stat_name=True):
    terms = []
    coefs = []
    lowers = []
    uppers = []
    groups = []
    significances = []
    control = []

    # Keep track of the index to know where to draw separating lines
    index = 0
    separation_indices = []

    # Iterate over each dataframe and its control group
    for df, control_group, group_label in zip(dataframes, control_groups, group_labels):
        test_groups = df['Group'].unique()
        if not plot_controls:
            test_groups = test_groups[test_groups != control_group]
        
        test_groups = list(test_groups)
        test_groups.insert(0, test_groups.pop(test_groups.index(control_group)))
    


        for group in test_groups:
            for stat in stats:
                
                individual_fold_changes = calculate_individual_fold_changes(df, control_group, group, stat)
                fold_change_mean = np.mean(individual_fold_changes)
                fold_change_std = np.std(individual_fold_changes)
                
                control_values = df[df['Group'] == control_group][stat].dropna()
                test_values = df[df['Group'] == group][stat].dropna()
                t_stat, p_value = ttest_ind(control_values, test_values, equal_var=False)
                
                terms.append(f"{stat} ({group})")
                coefs.append(fold_change_mean)
                control.append(control_group)
                
                std_error = fold_change_std / np.sqrt(len(individual_fold_changes))
                lowers.append(fold_change_mean - 1.96 * std_error)  # 95% CI lower bound
                uppers.append(fold_change_mean + 1.96 * std_error)  # 95% CI upper bound
                groups.append(group_label)
                significances.append((abs(fold_change_mean) >= fold_change_sig) and (p_value <= p_val))

                index += 1
        
        separation_indices.append(index+1)  # Store the index to draw separation lines
        
    num_stats = len(stats)
    fig, axs = plt.subplots(1, num_stats, figsize=(2*num_stats, 3), sharey=True)
    print(coefs)
    
    if num_stats == 1:
        axs = [axs]

    for stat_idx, (stat, stats_label) in enumerate(zip(stats, stats_labels)):
        ax = axs[stat_idx]
        # stat_terms = [term for term in terms if stat in term]
        stat_indices = [i for i, term in enumerate(terms) if term.startswith(stat)]


        for i in stat_indices:
            y_val = (int(i / len(stats)) * len(stats)) + len(stats) - 1
            # print(terms[i].split()[1][1:-1], control_groups[separation_indices[i]])
            if terms[i].split()[-1][1:-1] == control[i]:  # Check if it's the control group
                line_color = 'gray'  # Control group color
                marker_color = 'gray'  # Marker for the control group
            else:
                line_color = 'black' # Test group color
                marker_color = 'green' if significances[i] else 'red'   # Marker for significant/non-significant points
            
            ax.plot([lowers[i], uppers[i]], [y_val, y_val], color=line_color)  # Interval
            ax.plot(coefs[i], y_val, marker='o', mfc=marker_color, mec=marker_color)

        for sep_index in separation_indices:
            ax.axhline(y=sep_index, color='black', linestyle='-', linewidth=1)

        ax.set_yticks(stat_indices)
        ax.set_yticklabels([f"{term.split()[-1][1:-1]} [{group}]" for term, group in zip(terms, groups) if term.startswith(stat)], fontsize=8)
        

        ax.axvline(x=0, linestyle='--', color='grey', linewidth=1)  # Reference line at 0
        ax.set_xlabel('Log Fold Change', fontsize=8)
        ax.set_title(f'{stats_label}', fontsize=10)
        
        # for i, stat_index in enumerate(stat_indices):
        #     group_label = groups[stat_index]
        #     ax.text(-0.3, stat_index, f'{group_label}', va='center', ha='right', fontsize=8, transform=ax.get_yaxis_transform())

    plt.tight_layout()
    plt.show()
    
    return pd.DataFrame({'terms':terms, 'log2fold':coefs, 'low95':lowers, 'up95': uppers, 'group':groups})

def boxplot_graph(df, group, group2, data, data_labels, xlabel='',log=False):
    
    def format_func(value, tick_number):
        # Format the y-axis values to be consistent
        return f'{value:.1e}' if log else f'{value:.0f}'
    
    
    n_stats = len(data)
    fig, axes = plt.subplots(1, n_stats, figsize=(1.5 * n_stats, 2), sharex=True)

    if n_stats == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one statistic

    for ax, stat, label in zip(axes, data, data_labels):
        sns.boxplot(
            x=group, y=stat, data=df,
            # palette='pastel',
            width=0.6,
            ax=ax
        )

        sns.lineplot(
            x=group, y=stat, data=df,
            color='gray',
            markers=True,
            style=group2,
            dashes=False,
            linewidth=1,
            legend=False,
            ax=ax
        )
        
        ax.set_title(f'{label}', fontsize=10)
        ax.set_xlabel('')
        ax.set_ylabel(label, fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)
        sns.despine(ax=ax)
        
        ax.yaxis.set_major_formatter(FuncFormatter(format_func))

    plt.tight_layout()
    plt.show()
    
    

def boxplot_graph_full(datasets, group, group2, data, data_labels, row_labels=None, log=False):
    def format_func(value, tick_number):
        # Format the y-axis values to be consistent
        return f'{value:.1e}' if log else f'{value:.0f}'

    n_stats = len(data)
    n_datasets = len(datasets)
    fig, axes = plt.subplots(n_datasets, n_stats, figsize=(2 * n_stats, 1.5 * n_datasets), constrained_layout=True)

    if n_datasets == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one dataset

    for ax_row, df in zip(axes, datasets):
        for ax, stat, label in zip(ax_row, data, data_labels):
            sns.boxplot(
                x=group, y=stat, data=df,
                width=0.6,
                ax=ax
            )

            sns.lineplot(
                x=group, y=stat, data=df,
                color='gray',
                markers=True,
                style=group2,
                dashes=False,
                linewidth=1,
                legend=False,
                ax=ax
            )

            ax.set_xlabel('')  # Remove x-axis label
            ax.set_ylabel('')  # Remove x-axis label
            ax.tick_params(axis='both', which='major', labelsize=8)
            sns.despine(ax=ax)

            # Apply the y-axis formatter
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))

    # Add shared y-axis labels at the top
    for ax, label in zip(axes[0], data_labels):
        ax.annotate(label, xy=(0.5, 1.05), xytext=(0, 5),
                    xycoords='axes fraction', textcoords='offset points',
                    ha='center', va='baseline', fontsize=10)
        
    if row_labels:
        for ax, label in zip(axes, row_labels):
            ax[0].annotate(label, xy=(-0.1, 0.5), xytext=(-ax[0].yaxis.labelpad - 5, 0),
                           xycoords=ax[0].yaxis.label, textcoords='offset points',
                           ha='right', va='center', fontsize=10, rotation=90)

    plt.show()

from matplotlib.ticker import ScalarFormatter



def calculate_viral_families(df, threshold):
    viral_families = df.columns.difference(['filename', 'Group', 'Individual'])
    return df[viral_families].apply(lambda x: (x > threshold).sum(), axis=1)

def plot_viral_families(df, thresholds):
    groups = df['Group'].unique()
    results = []

    for threshold in thresholds:
        df['num_viral_families'] = calculate_viral_families(df, threshold)
        summary = df.groupby('Group')['num_viral_families'].agg(['mean', sem]).reset_index()
        summary['threshold'] = threshold
        results.append(summary)
    
    results = pd.concat(results)
    
    plt.figure(figsize=(5, 3))
    sns.set_palette('Set3')
    colors = sns.color_palette('Dark2', n_colors=len(groups))
    
    for group, color in zip(groups, colors):
        group_data = results[results['Group'] == group]
        plt.plot(group_data['threshold'], group_data['mean'], label=group, color=color)
        plt.fill_between(group_data['threshold'], 
                         group_data['mean'] - group_data['sem'], 
                         group_data['mean'] + group_data['sem'], 
                         color=color,
                         alpha=0.3)
        
    plt.xlabel('Threshold')
    plt.ylabel('Number of Viral Families')
    plt.yscale('log')
    plt.title('Average Number of Viral Families Above Threshold by Group')
    plt.legend(title='Group')
    plt.show()
    
def plot_viral_families_species(df_families, df_species, thresholds):
    groups = df_families['Group'].unique()
    results_families = []
    results_species = []

    for threshold in thresholds:
        df_families['num_viral_families'] = calculate_viral_families(df_families, threshold)
        summary_families = df_families.groupby('Group')['num_viral_families'].agg(['mean', sem]).reset_index()
        summary_families['threshold'] = threshold
        results_families.append(summary_families)
        
        df_species['num_viral_species'] = calculate_viral_families(df_species, threshold)
        summary_species = df_species.groupby('Group')['num_viral_species'].agg(['mean', sem]).reset_index()
        summary_species['threshold'] = threshold
        results_species.append(summary_species)
    
    results_families = pd.concat(results_families)
    results_species = pd.concat(results_species)
    
    plt.figure(figsize=(5, 3))

    palette = sns.color_palette("husl", len(groups))

    # Plot for viral families
    for group, color in zip(groups, palette):
        group_data_families = results_families[results_families['Group'] == group]
        plt.plot(group_data_families['threshold'], group_data_families['mean'], label=f'{group} Families', linestyle='-', color=color)
        plt.fill_between(group_data_families['threshold'], 
                         group_data_families['mean'] - group_data_families['sem'], 
                         group_data_families['mean'] + group_data_families['sem'], 
                         alpha=0.3, color=color)

    # Plot for viral species
    for group, color in zip(groups, palette):
        group_data_species = results_species[results_species['Group'] == group]
        plt.plot(group_data_species['threshold'], group_data_species['mean'], label=f'{group} Species', linestyle='--', color=color)
        plt.fill_between(group_data_species['threshold'], 
                         group_data_species['mean'] - group_data_species['sem'], 
                         group_data_species['mean'] + group_data_species['sem'], 
                         alpha=0.1, color=color)
        
    plt.xlabel('Threshold')
    plt.ylabel('Number of Viral Families/Species')
    plt.yscale('log')
    plt.title('Average Number of Viral Families/Species Above Threshold by Group')
    plt.legend(title='Group')
    plt.show()

def plot_viral_families_species_full(dfs_families, dfs_species, thresholds, group_names, overall_title):
    num_plots = len(dfs_families)
    fig, axes = plt.subplots(nrows=1, ncols=num_plots, figsize=(4*num_plots, 4))
    
    if num_plots == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one subplot
        

    
    for i, (df_families, df_species, group_name) in enumerate(zip(dfs_families, dfs_species, group_names)):
        groups = ['A'] + [g for g in df_families['Group'].unique() if g != 'A']
        results_families = []
        results_species = []        
        

        for threshold in thresholds:
            df_families['num_viral_families'] = calculate_viral_families(df_families, threshold)
            summary_families = df_families.groupby('Group')['num_viral_families'].agg(['mean', sem]).reset_index()
            summary_families['threshold'] = threshold
            results_families.append(summary_families)
            
            df_species['num_viral_species'] = calculate_viral_families(df_species, threshold)
            summary_species = df_species.groupby('Group')['num_viral_species'].agg(['mean', sem]).reset_index()
            summary_species['threshold'] = threshold
            results_species.append(summary_species)
        
        results_families = pd.concat(results_families)
        results_species = pd.concat(results_species)
        
        sns.set_palette('Dark2')
        colors = sns.color_palette('Dark2', n_colors=len(groups))

        ax = axes[i]

        # Plot for viral families
        for group, color in zip(groups, colors):

            group_data_families = results_families[results_families['Group'] == group]
            ax.plot(group_data_families['threshold'], group_data_families['mean'], label=group, linestyle='-', color=color)
            ax.fill_between(group_data_families['threshold'], 
                             group_data_families['mean'] - group_data_families['sem'], 
                             group_data_families['mean'] + group_data_families['sem'], 
                             alpha=0.3, color=color)

        # Plot for viral species
        for group, color in zip(groups, colors):
        
            group_data_species = results_species[results_species['Group'] == group]
            ax.plot(group_data_species['threshold'], group_data_species['mean'], linestyle='--', color=color)
            ax.fill_between(group_data_species['threshold'], 
                             group_data_species['mean'] - group_data_species['sem'], 
                             group_data_species['mean'] + group_data_species['sem'], 
                             alpha=0.1, color=color)
        
        if i == 0:
            ax.set_ylabel('Number of Viral Families / Species')
        ax.set_xlabel('Read Threshold')
        ax.set_yscale('log')
        ax.set_title(group_name)
        ax.legend(title='Group')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.ticklabel_format(style='plain', axis='y')
        ax.set_ylim(bottom=0.0, top=1000)
    
    plt.suptitle(overall_title, fontsize=10, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    
    
def calculate_viral_richness(df, threshold):
    viral_families = df.columns.difference(['filename', 'Group', 'Individual'])

    def shannon_index(reads):
        # Apply threshold
        reads_above_threshold = reads[reads > threshold]
        if reads_above_threshold.empty:
            return 0  # Return 0 if no families are above the threshold
        
        total_reads = np.sum(reads_above_threshold)
        proportions = reads_above_threshold / total_reads
        proportions = proportions[proportions > 0]  # Remove zero proportions to avoid log(0)
        shannon_index = -np.sum(proportions * np.log(proportions))
        return shannon_index
    
    return df[viral_families].apply(shannon_index, axis=1)

def calculate_viral_richness_simpson(df, threshold):
    viral_families = df.columns.difference(['filename', 'Group', 'Individual'])

    def simpson_index(reads):
        # Apply threshold
        reads_above_threshold = reads[reads > threshold]
        if reads_above_threshold.empty:
            return 0  # Return 0 if no families are above the threshold
        
        total_reads = np.sum(reads_above_threshold)
        proportions = reads_above_threshold / total_reads
        proportions = proportions[proportions > 0]  # Remove zero proportions to avoid division by zero
        
        # Calculate Simpson's Index: 1 - sum(p_i^2)
        simpson_index_value = 1 - np.sum(proportions ** 2)
        return simpson_index_value
    
    return df[viral_families].apply(simpson_index, axis=1)

def plot_richness_families_species_full(dfs_families, dfs_species, thresholds, group_names, overall_title):
    num_plots = len(dfs_families)
    fig, axes = plt.subplots(nrows=1, ncols=num_plots, figsize=(4*num_plots, 4))
    
    if num_plots == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one subplot
    
    for i, (df_families, df_species, group_name) in enumerate(zip(dfs_families, dfs_species, group_names)):
        groups = ['A'] + [g for g in df_families['Group'].unique() if g != 'A']
        results_families = []
        results_species = []

        for threshold in thresholds:
            df_families['num_viral_families'] = calculate_viral_richness(df_families, threshold)
            summary_families = df_families.groupby('Group')['num_viral_families'].agg(['mean', sem]).reset_index()
            summary_families['threshold'] = threshold
            results_families.append(summary_families)
            
            df_species['num_viral_species'] = calculate_viral_richness(df_species, threshold)
            summary_species = df_species.groupby('Group')['num_viral_species'].agg(['mean', sem]).reset_index()
            summary_species['threshold'] = threshold
            results_species.append(summary_species)
        
        results_families = pd.concat(results_families)
        results_species = pd.concat(results_species)
        
        sns.set_palette('Dark2')
        colors = sns.color_palette('Dark2', n_colors=len(groups))

        ax = axes[i]

        # Plot for viral families
        for group, color in zip(groups, colors):
            group_data_families = results_families[results_families['Group'] == group]
            ax.plot(group_data_families['threshold'], group_data_families['mean'], label=group, linestyle='-', color=color)
            ax.fill_between(group_data_families['threshold'], 
                             group_data_families['mean'] - group_data_families['sem'], 
                             group_data_families['mean'] + group_data_families['sem'], 
                             alpha=0.3, color=color)

        # Plot for viral species
        for group, color in zip(groups, colors):
            group_data_species = results_species[results_species['Group'] == group]
            ax.plot(group_data_species['threshold'], group_data_species['mean'], linestyle='--', color=color)
            ax.fill_between(group_data_species['threshold'], 
                             group_data_species['mean'] - group_data_species['sem'], 
                             group_data_species['mean'] + group_data_species['sem'], 
                             alpha=0.1, color=color)
        
        if i == 0:
            ax.set_ylabel('Shannon Index')
        ax.set_xlabel('Read Threshold')
        # ax.set_yscale('log')
        ax.set_title(group_name)
        ax.legend(title='Group')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        ax.ticklabel_format(style='plain', axis='y')
        # ax.set_ylim(bottom=0.0, top=1000)
    
    plt.suptitle(overall_title, fontsize=10, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

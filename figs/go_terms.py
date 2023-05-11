import os
import pandas as pd

seqscreen_reports = '../../AECC_patients_data/taxonkit/fast/'

go_terms_data = pd.DataFrame()

for i, file in enumerate(os.listdir(seqscreen_reports)):
    print(f'[{i}] {file}')
    file_path = os.path.join(seqscreen_reports, file)
    
    data = pd.read_csv(file_path, delimiter='\t')
    viral_test = data.dropna()
    # viral_test = viral_test[viral_test['Unnamed: 45'].str.contains('Viruses')]
    
    go_terms = viral_test.iloc[:, 8:40]
    go_terms = go_terms[go_terms['disable_organ'] != '-'].astype('int').sum(axis=0)
    go_terms.name = file
    
    go_terms_data = go_terms_data.append(go_terms)
    
go_terms_data.to_csv('go_terms_counts.csv')

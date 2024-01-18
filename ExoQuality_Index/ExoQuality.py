#libraries
from importlib.metadata import version
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import math
import os 
import glob
from sklearn.preprocessing import QuantileTransformer
import scipy as scipy


#Dependency check

required = sorted({'0.12.2', '1.23.5', '1.3.0', '1.3.4', '1.7.0', '3.7.2'})
versions = sorted({version('seaborn'), version('matplotlib'),
                   version('numpy'), version('pandas'),
                   version('scikit-learn'),version('scipy')})

#do the check step
try:
    for i,j in zip(required, versions):
        if i > j:
            print(f'mismatch between required {i} and user version {j}')
            print('Dependency mismatch but still may work')
        else:
            print(f'match found: required {i} equals user version {j}')
except Exception as e:
    print(f'Error occured: {e}')
    
    
print('Moving onto loading the dataset')

####################

#Set the directory and grab the files
directory=os.getcwd()
files = glob.glob(os.path.join(directory, '*.csv')) #THIS WILL FIND ALL CSV FILES, SO BE AWARE THAT 
                                                    #THE NEXT BLOCK WILL LOAD THE FIRST ONE IT FINDS

#now to load, process, and do the calculation with the CSV file into python
for file in files:
    try:
        df=pd.read_csv(file)
        print(f'Successfully loaded the file: {os.path.basename(file)}')
        
        #read the columns to separate between numeric and identifier 
        numeric_df = df.select_dtypes(exclude=['object'])
        method = df['Method'] #lil messy but its fine
        IDX=df['ID'] #lil messy but its fine
        nmdf_names = numeric_df.columns
        
        #now onto the processing
        transformed = pd.DataFrame(QuantileTransformer(output_distribution='uniform', 
                                                       random_state=389362).fit_transform(numeric_df), 
                                   columns=nmdf_names)
        
        transformed['Method']=method
        transformed['ID']=IDX
        print('Processing complete, onto plotting')
        
        #do the plotting
        ##NOTE YOU CAN SET A CJUSTOM PALETTE AS DESIRED.
        #sns.set_context("paper", font_scale=3)
        #g = sns.pairplot(data=transformed, hue='Method', height=3, aspect=1, plot_kws={"s":80})
        #for ax in g.axes.flat:
            #ax.set_xlabel(ax.get_xlabel(), fontweight='bold')
            #ax.set_ylabel(ax.get_ylabel(), fontweight='bold')
        #plt.savefig('SPLOM.png')
            
            
        #now we're going to do the exoquality calculation for each method then collate
        method_list = transformed['Method'].unique() #list of methods
        ID_list = transformed['ID'].unique() #list of IDs
        
        #storage dictionary
        mdata = {}
        
         
        #now do a loop
        for method in method_list:
            #initialize the dictionary corresponding to each method and subsequent result
            md = {'Method': str(method), 'Results':[]}
            
            #grab a method,
            transformed_meth=transformed[transformed['Method'].str.contains(str(method))]  
            
            
            #grab the ID
            for ID in ID_list:
                trans_meth_id = transformed_meth[transformed_meth['ID'].str.contains(str(ID))]
                trans_meth_num = trans_meth_id.select_dtypes(exclude=['object']) #grab the numeric data        
                smsd = np.sum(trans_meth_num.std())
                md['Results'].append({'ID':str(ID), 'SD':smsd})
        
            #tabulate the results
            mdata[str(method)] = md
          
        #results - base
        for method,data in mdata.items():
            print(f"Method: {data['Method']}")
            for result in data['Results']:
                print (f" ID:{result['ID']}, SD: {result['SD']}")
         
        
        # results as a table
        print(mdata.items())
                                                                  
        
    except pd.errors.EmptyDataError:
        print(f'Empty CSV file - {os.path.basename(file)}')
        break
        
    except pd.errors.ParserError:
        print(f'Bad CSV - {os.path.basename(file)}')
        break
        
    except Exception as e:
        print(f'A general error occured {e}')
        break 
        
        
        




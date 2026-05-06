import  kagglehub
import  pandas as pd
import os

def data_preparing(dataset_id):
    try:

        download = kagglehub.dataset(dataset_id) # download file
        files = [f for f in os.listdir(download) if f.endswith('.csv')] # find file in folder
        if not files:
            return 'Error: CSV file not found'

        csv_file = os.path.join(download, files[0])

        df = pd.read_csv(csv_file)
        df_clean = df.drop_duplicates().dropna()
        output_name = 'Final_Data_For_Visualisation.csv'
        df_clean.to_csv(output_name, index = False)

        return  f'Success , file downloaded, name {output_name}'
    except Exception as e :
        return  f"Error Python: {str(e)}"




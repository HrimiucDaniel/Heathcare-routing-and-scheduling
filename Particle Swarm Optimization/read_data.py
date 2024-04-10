import pandas as pd


def read_data(filename):
    nurses_df = pd.read_excel(filename, sheet_name='nurses')
    patients_df = pd.read_excel(filename, sheet_name='patients')
    nurses_id = nurses_df['N'].tolist()
    nurses_qualifications = nurses_df['Q'].tolist()
    nurses_Time = nurses_df['Time'].tolist()

    hospital_x = patients_df['x'].values[0]
    hospital_y = patients_df['y'].values[0]
    hospital_early_time = 0
    hospital_late_time = 1000

    patients_id = patients_df['n'].tolist()[1:]
    patients_x = patients_df['x'].tolist()[1:]
    patients_y = patients_df['y'].tolist()[1:]
    patients_early_time = patients_df['et'].tolist()[1:]
    patients_late_time = patients_df['lt'].tolist()[1:]
    patients_duration = patients_df['sd'].tolist()[1:]
    patients_visits = patients_df['f'].tolist()[1:]
    patients_qualification = patients_df["Q'"].tolist()[1:]
    return nurses_id, nurses_qualifications, nurses_Time, hospital_x, hospital_y, hospital_early_time, \
           hospital_late_time, patients_id, patients_x, patients_y, patients_early_time, patients_late_time, \
           patients_duration, patients_visits, patients_qualification

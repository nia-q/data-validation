import pandas as pd
from read_ms_sf_df import read_ms_sf_df


def validate_data(ms_path, sf_path, output_path):
    #create tuple of ms and sf df
    ms_sf_df = read_ms_sf_df(ms_path, sf_path)
    #assign frst df to ms_df
    ms_df = ms_sf_df[0]
    #assign second df to sf_df
    sf_df = ms_sf_df[1]

    # check raw count of students in mainstay data
    ms_count = len(ms_df['id'])

    # check raw count of students in salesforce data
    sf_count = len(sf_df['id'])

    # find fellows on salesforce but not on Mainstay
    sf_only = sf_df.loc[~sf_df['id'].isin(ms_df['id'])]

    # only sf count
    sfo_count = len(sf_only)

    # find fellows on mainstay not on salesforce
    ms_only = ms_df.loc[~ms_df['id'].isin(sf_df['id'])]

    # only ms count
    mso_count = len(ms_only)

    # final ms count
    f_ms_count = ms_count - mso_count

    # final sf count
    f_sf_count = sf_count - sfo_count

    # write results to sf
    stats_df = pd.DataFrame({'raw mainstay count': [ms_count],
                             'num students mainstay only': [mso_count],
                             'final mainstay count': [f_ms_count],
                             'raw salesforce count': [sf_count],
                             'num students salesforce only': [sfo_count],
                             'final salesforce count': [f_sf_count]})

    # create master data frame joined on id (ie only returning students in both datasets)
    df = pd.merge(ms_df, sf_df, on='id', suffixes=('_ms', '_sf'))

    # order columns in combined dataframe
    df = df[['id',
             'First Name_ms',
             'First Name_sf',
             'Last Name_ms',
             'Last Name_sf',
             'Phone MS',
             'Phone SF',
             'DSS MS',
             'DSS SF',
             'College MS',
             'College SF',
             'College Type MS',
             'College Type SF',
             'Enrollment MS',
             'Enrollment SF',
             'College Name MS',
             'College Name SF']]

    college_filter = df['College MS'] == df['College SF']
    ct_filter = df['College Type MS'] == df['College Type SF']
    enroll_filter = df['Enrollment MS'] == df['Enrollment SF']
    phone_filter = df['Phone MS'] == df['Phone SF']
    dss_filter = df['DSS MS'] == df['DSS SF']
    college_n_filter = df['College Name MS'] == df['College Name SF']

    df['college_match'] = college_filter
    df['college type_match'] = ct_filter
    df['enrollment_match'] = enroll_filter
    df['phone match'] = phone_filter
    df['dss match'] = dss_filter
    df['college name match'] = college_n_filter



    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    stats_df.to_excel(writer, sheet_name="Data Validation Stats", index=False)
    ms_only.to_excel(writer, sheet_name="Mainstay Only Students", index=False)
    sf_only.to_excel(writer, sheet_name="Salesforce Only Students", index=False)
    df.to_excel(writer, sheet_name="Combined MS.SF Data Set", index=False)

    # Get the xlsxwriter workbook object
    workbook = writer.book

    # Get the xlsxwriter worksheet object

    # autofit each sheet
    worksheet = writer.sheets["Data Validation Stats"]
    worksheet.autofit()

    worksheet = writer.sheets["Mainstay Only Students"]
    worksheet.autofit()

    worksheet = writer.sheets["Salesforce Only Students"]
    worksheet.autofit()

    worksheet = writer.sheets["Combined MS.SF Data Set"]
    worksheet.autofit()
    writer.close()


ms_path = r'C:\Users\Nia Quinones\OneDrive - OneGoal\Desktop\Data Validation\2023 DV\Week\{}.csv'.format(
    input("What is the MS path?"))
sf_path = r'C:\Users\Nia Quinones\OneDrive - OneGoal\Desktop\Data Validation\2023 DV\Week\{}.csv'.format(
    input("What is the SF path?"))
output_path = r'C:\Users\Nia Quinones\OneDrive - OneGoal\Desktop\Data Validation\2023 DV\Week\{}.xlsx'.format(
    input("What is the Output path?"))
validate_data(ms_path=ms_path, sf_path=sf_path, output_path=output_path)

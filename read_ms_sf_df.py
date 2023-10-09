import pandas as pd


def read_ms_sf_df(ms_path, sf_path):
    # create mainstay df
    ms_df = pd.read_csv(ms_path,
                        usecols=['First Name',
                                 'Last Name',
                                 'CRM ID',
                                 'Phone',
                                 'Direct Support Staff (Custom)',
                                 'Institution Name (Custom)',
                                 'College Type (Custom)',
                                 'College/University (Custom)',
                                 'Enrolled/Not Enrolled (Custom)'])

    # rename mainstay df columns
    ms_df.rename(columns={'CRM ID': 'id',
                          'College/University (Custom)': 'College MS',
                          'College Type (Custom)': 'College Type MS',
                          'Enrolled/Not Enrolled (Custom)': 'Enrollment MS',
                          'Phone': 'Phone MS',
                          'Direct Support Staff (Custom)': 'DSS MS Code',
                          'Institution Name (Custom)': 'College Name MS'}, inplace=True)

    # create salesforce df
    sf_df = pd.read_csv(sf_path,
                        usecols=['First Name',
                                 'Last Name',
                                 'Case Safe ID',
                                 'Mobile Phone',
                                 'Direct Support Staff: Full Name',
                                 'College/University: Organization Name',
                                 'College/University: Case Safe ID',
                                 'College Type',
                                 'Enrolled/Not Enrolled'])

    # rename salesforce df columns
    sf_df.rename(columns={'Case Safe ID': 'id',
                          'College/University: Case Safe ID': 'College SF',
                          'College Type': 'College Type SF',
                          'Enrolled/Not Enrolled': 'Enrollment SF',
                          'Mobile Phone': 'Phone SF',
                          'Direct Support Staff: Full Name': 'DSS SF',
                          'College/University: Organization Name': 'College Name SF'}, inplace=True)

    # cleaning salesforce phone numbers to match mainstay phone numbers
    sf_df['Phone SF'] = sf_df['Phone SF'].str.replace("-", "").str.replace("(", "", regex=True).str.replace(")", "", regex=True).str.replace(" ", "")

    # cleaning mainstay phone numbers: make mainstay phone numbers strings to match salesforce phone number data type
    ms_df['Phone MS'] = ms_df['Phone MS'].fillna(0).apply(int).apply(str)


    # create dss code dictionary
    dss_dict = {'0058X00000FSEACQA5': 'Advisor 1',
                '0058X00000FcgeKQAR': 'Advisor 2',
                '0050V000007NRW4QAO': 'Advisor 3',
                '0058X00000Fc1YlQAJ': 'Advisor 4',
                '0058X00000Fke6cQAB': 'Advisor 5',
                '0051L00000Em6qfQAB': 'Advisor 6',
                '0058X00000EwzdRQAR': 'Advisor 7'}

    # create DSS column in MS dataframe that aligns to the salesforce df
    ms_df['DSS MS'] = ms_df['DSS MS Code'].map(dss_dict)

    # make salesforce and mainstay DSS NaN values equal to Blank
    sf_df['DSS SF'].fillna("Blank", inplace=True)
    ms_df['DSS MS'].fillna("Blank", inplace=True)


    # return tuple of mainstay and salesforce dfs
    return ms_df, sf_df
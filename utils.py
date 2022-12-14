import pandas as pd

###### TOC ##########
#1 getMIWindData() - gets the wind data in a Pandas Dataframe
#2   getHourlyPowerData() - given a link, downloads POWER data, puts in dataframe w/ datetime index
#3 

#1
def getMIWindData():
    '''
    Gets wind related atmospheric data from NASA's POWER website for a location in small town Michigan
    
    Returns: Pandas Dataframe with datetime index
    '''
    #set link for 
    link = "https://power.larc.nasa.gov/api/temporal/hourly/point?Time=LST&parameters=T2M,PS,WS50M,WD50M&community=RE&longitude=-85.9654&latitude=44.6385&start=20110401&end=20210331&format=CSV"
    #return dataframe
    return getHourlyPOWERData(link)

#2 - Lots to do to improve this one...not actually a good, reusable function
def getHourlyPOWERData(link):
    '''
    Given a CSV-type URL for NASA's POWER website, returns a formatted dataframe with a datetime index.
    Assumes hourly data is requested. 
    
    Returns: Pandas DataFrame w/ Datetime index 
    Parameters: 
        (R) link: URL dynamically generated by NASA's POWER interface. Use CSV setting in GUI
        
    IMPROVEMENTS:
    So this is a bit ugly as it assumes 12 header rows (which is probably only the case when 4 parameters are chosen).
    - Create function to get last line of header
    - - For NASA site, that is with "-END HEADER-", however ideally I will functionize it to:
    - - - handle any string to indicate last line of metadata
    - - - handle any string to indicate first line of actual data
    - - - handle any string to indicate prefix of metadata
    - This will also mean we won't take a link, but rather will download the data, then open the file to find the header
    - ALT: mayb be able to calculate rows to skip via parameter count in link (Still assumes standard # of metadata lines)
    '''
    #get last row of metadata
    meta_end = 12
    #read the data
    df = pd.read_csv(link,skiprows=meta_end)
    
    #Make new datetime column
    df['dt'] = df.YEAR.astype(str) + '-' + df.MO.astype(str).str.pad(2,side='left',fillchar='0') + '-' + df.DY.astype(str).str.pad(2,side='left',fillchar='0') + ' ' + df.HR.astype(str).str.pad(2,side='left',fillchar='0')
    #Convert column to datetime
    df.dt = pd.to_datetime(df.dt,format='%Y-%m-%d %H')
    
    #set index, sort and return dt
    return df.set_index('dt').sort_index()
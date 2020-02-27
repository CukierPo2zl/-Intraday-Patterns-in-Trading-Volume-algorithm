
def pop_row(df, limit):
    _filter = df['hour']!=limit
    df = df[_filter]
    return df.reset_index(drop=True)

def get_by_hour(df, hour):
    tmp = df['hour']==hour
    return df[tmp]

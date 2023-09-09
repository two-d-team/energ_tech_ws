import pandas as pd
import streamlit as st
def transform(df):
    df = df.copy()
    df.loc[:, 'PERIOADA'] = pd.to_datetime(df.PERIOADA, format='%Y-%m-%d')
    df.loc[:, 'CONTRACT_START_DATE'] = pd.to_datetime(df.CONTRACT_START_DATE, format='%Y-%m-%d')
    df.loc[:, 'CONTRACT_EXPIRATION_DATE'] = pd.to_datetime(df.CONTRACT_EXPIRATION_DATE, format='%Y-%m-%d')
    df.loc[:, 'LUNA_INCIDENT'] = pd.to_datetime(df.LUNA_INCIDENT, format='%Y-%m-%d')
    df.loc[:, 'LUNA_APEL'] = pd.to_datetime(df.LUNA_APEL, format='%Y-%m-%d')

    # st.write(df.head())
    # st.write(df.info())

    return df
#   # df.loc[df.CONTRACT_EXPIRATION_DATE.isna(), 'CONTRACT_EXPIRATION_DATE'] = datetime.datetime(2050, 12, 31)
#   st.write(df.info())
#   df.loc[:, 'PRET_ABON'] = df['PRET_ABON'].str.replace(',', '.')
#   df.loc[:, 'PRET_ABON'] = df['PRET_ABON'].astype('float')

#   df.loc[df.QNT_PORT_REZ.isna(), 'QNT_PORT_REZ'] = 0
#   df.loc[:, 'QNT_PORT_REZ'] = df['QNT_PORT_REZ'].astype('int')

#   df.loc[df.CONTRACT_LENGTH.isna(), 'CONTRACT_LENGTH'] = 0

#   df.loc[:, 'AVG_PERCEPTION'] = df['AVG_PERCEPTION'].str.replace(',', '.')
#   df.loc[:, 'AVG_PERCEPTION'] = df['AVG_PERCEPTION'].astype('float')

#   df.loc[df.SUMA_ACHITARII.isna(), 'SUMA_ACHITARII'] = '0'
#   df.loc[:, 'SUMA_ACHITARII'] = df['SUMA_ACHITARII'].str.replace(',', '.')
#   df.loc[:, 'SUMA_ACHITARII'] = df['SUMA_ACHITARII'].astype('float')

# #   st.write(df.SUMA_ACHITARII)
# #   st.write(df.SUMA_ACHITARII.isna().sum())

#   df.loc[df.IPTV_STB_QUANTITY.isna(), 'IPTV_STB_QUANTITY'] = -1

#   df = df.drop(["CREANTE_REST",  
#               "LUNA_SUSPENDARI",
#               "QNT_SUSP",
#               "IPTV_STB_QUANTITY" ], axis = 1) 

#   # NUll == 0 apeluri 
#   df.QNT_APELARI.fillna(0,inplace=True)   
#   # NUll ==  0 rezilieri la nivel de router 
#   df.QNT_PORT_REZ.fillna(0,inplace=True)    
#   # NULL == 0  incidente 
#   df.QNT_INCEDENT.fillna(0,inplace=True)

#   return df


def get_recommended_package(df, package):
    # return '...'
    df['prev_INET_PACK'] = df.INET_PACK.shift()
    df.loc[df.ACCOUNTID != df.shift().ACCOUNTID, 'prev_INET_PACK'] = None
    df['prev_IPTV_PACK'] = df.IPTV_PACK.shift()
    shifts = df[(~df.prev_INET_PACK.isna()) & (df['INET_PACK'] != df['prev_INET_PACK'])]
    shifts =  shifts[['prev_INET_PACK', 'INET_PACK']].value_counts().rename('count').reset_index()
    shifts['name'] = shifts.apply(lambda row: f"{row['prev_INET_PACK']}-{row['INET_PACK']} ", axis=1)
    migr_popularity_matrix = shifts.pivot(index='prev_INET_PACK', columns='INET_PACK', values='count')

    recommendations = migr_popularity_matrix.idxmax(axis=1)

    if ((~pd.isna(package)) & (package in recommendations)):
       return recommendations.loc[package]
    else:
        top_packs = df.groupby(['ACCOUNTID']).INET_PACK.last().value_counts(ascending=False)[:2].index.values

        if package != top_packs[0]:
           return top_packs[0]
           
        return top_packs[1]
    

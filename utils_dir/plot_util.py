import datetime
import pandas
import seaborn
import streamlit

import altair as alt

from plotly import express

seaborn.set()


@streamlit.cache 
def load_data():
    data_frame = pandas.read_csv("../data/train_all_df.csv", sep=",")

    return data_frame


def get_count_plot(data_frame, column):
    value = data_frame.groupby(column)["IS_CHURN"].mean()
    figure = express.bar(value/100, color=value.index, width=500, height=500)
    figure.update_layout(xaxis_title=column, yaxis_title="Churn Rate")

    return figure


def get_pie_chart(data_frame, column):
    value = data_frame[column].value_counts(normalize=True)
    figure = express.pie(values=value.values, names=value.index, height=450, width=450)

    return figure


def get_histogram(data_frame, column, set_hue=None):
    figure = express.histogram(data_frame, x=column)

    return figure


def show_plots(data_frame, last_df, features):
    df = data_frame

    # --- #
    streamlit.write("Top packages by monthly pay")
    col1, col2 = streamlit.columns(2)
    tvpack_months = df.groupby('IPTV_PACK').agg({
        'PERIOADA': ['max', 'min']
    })
    tvpack_months.columns = tvpack_months.columns.droplevel()


    tvpack_months['months'] = (tvpack_months['max'] - tvpack_months['min']).dt.days //30
    tvpack_sum = df.groupby('IPTV_PACK').SUMA_ACHITARII.sum()
    top_tvpackages = tvpack_sum.div(tvpack_months['months']).sort_values(ascending=False).head(5).rename('IPTV')
    col1.bar_chart(top_tvpackages)

    inet_months = df.groupby('INET_PACK').agg({
        'PERIOADA': ['max', 'min']
    })
    inet_months.columns = inet_months.columns.droplevel()

    inet_months['months'] = (inet_months['max'] - inet_months['min']).dt.days //30
    inetpack_sum = df.groupby('INET_PACK').SUMA_ACHITARII.sum()
    top_inetpackages = inetpack_sum.div(inet_months['months']).sort_values(ascending=False)
    top_inetpackages = top_inetpackages[top_inetpackages < 1e9].head(5).rename('INET')
    col2.bar_chart(top_inetpackages)

    # iptv
    # df_temp = df.groupby(['PERIOADA', 'IPTV_PACK']).size().reset_index()
    # df_temp = df_temp.pivot(values=0, index='PERIOADA', columns='IPTV_PACK')

    # top_iptv_churn = last_df.groupby('IPTV_PACK').size().sort_values(ascending=False).index[:10]
    # df_temp = df_temp[top_iptv_churn].fillna(0)
    # streamlit.line_chart(df_temp)

    # inet

    df_temp2 = df.groupby(['PERIOADA', 'INET_PACK']).size().reset_index()
    df_temp2 = df_temp2.pivot(values=0, index='PERIOADA', columns='INET_PACK')

    top_inet_churn = last_df.groupby('INET_PACK').size().sort_values(ascending=False).index[:10]
    df_temp2 = df_temp2[top_inet_churn].fillna(0)
    streamlit.write('### INET Packs customers through time')

    streamlit.line_chart(df_temp2)
    col1, col2 = streamlit.columns(2)

    customers_cnt = df.groupby('PERIOADA').size().rename('customers')
    customers_cnt = pandas.DataFrame({
        'month': customers_cnt.index,
        'value': customers_cnt
    })
    line_chart = alt.Chart(customers_cnt).mark_line(interpolate='basis').encode(
        alt.X('month', title='Year'),
        alt.Y('value', title='Count')
    ).properties(
        title='Active customers per month'
    )
    col1.altair_chart(line_chart)

    churn_ratio_cnt = last_df[last_df.IS_CHURN == 1].groupby('PERIOADA').ACCOUNTID.nunique()
    users_per_month = df.groupby('PERIOADA').ACCOUNTID.nunique()
    churns_ratio_per_month = churn_ratio_cnt.div(users_per_month) * 100

    churn_ratio_cnt = pandas.DataFrame({
        'month': churns_ratio_per_month.index,
        'value': churns_ratio_per_month
    })
    cr_line_chart = alt.Chart(churn_ratio_cnt).mark_line(interpolate='basis').encode(
        alt.X('month', title='Year'),
        alt.Y('value', title='Churn ratio %')
    ).properties(
        title='Monthly churn ratio %'
    )
    col2.altair_chart(cr_line_chart)

    ### 
    last_df.loc[:, 'IS_CHURN_INET'] = last_df.apply(lambda row: (pandas.isna(row['INET_PACK']) & row['IS_CHURN']), axis=1)
    last_df.loc[:, 'IS_CHURN_IPTV'] = last_df.apply(lambda row: (pandas.isna(row['IPTV_PACK']) & row['IS_CHURN']), axis=1)

    s1 = last_df.groupby(['PERIOADA']).IS_CHURN_IPTV.sum()
    s2 = last_df.groupby(['PERIOADA']).IS_CHURN_INET.sum()

    pack_ratio_df = pandas.DataFrame({
        'iptv': s1,
        'inet': s2
    }).rename_axis('Perioada')

    streamlit.write('### Churned customers for each packet by month')
    streamlit.line_chart(pack_ratio_df)
    # streamlit.altair_chart(pr_line_chart)

    # suma achitarii
    suma_ac_per_month = df.groupby('PERIOADA').SUMA_ACHITARII.sum()
    suma_ac_per_month = pandas.DataFrame({
        'month': suma_ac_per_month.index,
        'value': suma_ac_per_month
    })
    sa_line_chart = alt.Chart(suma_ac_per_month).mark_line(interpolate='basis').encode(
        alt.X('month', title='Year'),
        alt.Y('value', title='MDL')
    ).properties(
        title='Total pay per month'
    )


    # contract type
    contract_churn = df.groupby(['ACCOUNTID']).last().groupby(['CONTRACT_LENGTH', 'IS_CHURN']).size().unstack()
    contract_churn = contract_churn[contract_churn.index != 6]

    contract_churn = contract_churn.div(contract_churn.sum(axis=1), axis=0).rename(columns={
        0: 'NO CHURN', 
        1: 'CHURN'
    })


    streamlit.write('### Churn distribution by feature')
    
    col1, col2 = streamlit.columns(2)
    col1.write('Contract length')
    col1.bar_chart(contract_churn)

    qnt_luni_dator = df.groupby(['ACCOUNTID']).agg({
        'LUNI_DATOR': max,
        'IS_CHURN': lambda x: x.iloc[-1]
    }).groupby(['LUNI_DATOR', 'IS_CHURN']).size().unstack()

    qnt_luni_dator = qnt_luni_dator.div(qnt_luni_dator.sum(axis=1), axis=0)


    col2.write('Max debt months')
    col2.bar_chart(qnt_luni_dator)

    # concurenti
    col1, col2 = streamlit.columns(2)

    concurenti_churn = df.groupby(['ACCOUNTID']).last().groupby(['CONCURENTI', 'IS_CHURN']).size().unstack()
    concurenti_churn = concurenti_churn.div(concurenti_churn.sum(axis=1), axis=0)
    concurenti_churn = concurenti_churn.div(concurenti_churn.sum(axis=1), axis=0).rename(columns={
        0: 'NO CHURN', 
        1: 'CHURN'
    })
    col2.write('Competitors')
    col2.bar_chart(concurenti_churn)

    # tehnologie
    tehnologia_churn = df.groupby(['ACCOUNTID']).last().groupby(['TECHNOLOGY', 'IS_CHURN']).size().unstack()
    tehnologia_churn.div(tehnologia_churn.sum(axis=1), axis=0)
    tehnologia_churn = tehnologia_churn.div(tehnologia_churn.sum(axis=1), axis=0).rename(columns={
        0: 'NO CHURN', 
        1: 'CHURN'
    })
    col1.write('Technology')
    col1.bar_chart(tehnologia_churn)




    
    last_sample = df[df.PERIOADA == datetime.datetime(2022, 12, 31)]
    # only_inet_pack = ((~last_sample.IPTV_PACK.isna()) & (last_sample.INET_PACK.isna())).sum()
    # only_tv_pack = (last_sample.IPTV_PACK.isna() & (~last_sample.INET_PACK.isna())).sum()
    # both_pack = ((~last_sample.IPTV_PACK.isna()) & (~last_sample.INET_PACK.isna())).sum()


    #
    groups = df.groupby(['PERIOADA'])

    pack_dist_time_list = []

    for name, group in groups:
        inet_count = (group.INET_PACK.isna() & ~group.IPTV_PACK.isna()).sum()
        iptv_count = (~group.INET_PACK.isna() & group.IPTV_PACK.isna()).sum()
        both_count = (~group.INET_PACK.isna() & ~group.IPTV_PACK.isna()).sum()

        pack_dist_time_list.append([name, iptv_count, inet_count, both_count])

    pack_dist_time_df = pandas.DataFrame(pack_dist_time_list, columns=['perioada', 'iptv', 'inet', 'both']).set_index('perioada')

    pack_dist_time_df = pack_dist_time_df.div(pack_dist_time_df.sum(axis=1), axis=0)
    pack_dist_time_df = pandas.DataFrame(pack_dist_time_list, columns=['perioada', 'iptv', 'inet', 'both']).set_index('perioada')
    pack_dist_time_df = pack_dist_time_df.div(pack_dist_time_df.sum(axis=1), axis=0) * 100


    # debts
    s = df.groupby(['PERIOADA']).agg({
        'LUNI_DATOR': lambda x: x[(x != 0) & (~x.isna())].shape[0],
        'ACCOUNTID': len
    })

    s = s['LUNI_DATOR'].div(s['ACCOUNTID']) * 100

    streamlit.write('### % of customers with debts')
    streamlit.line_chart(s)

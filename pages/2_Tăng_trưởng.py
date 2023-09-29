import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'Tăng trưởng', layout = 'wide', page_icon = ':trophy:')

df = pd.read_csv('dataset/Vinasoy.csv')

df['Mã NV'] = df['Mã NV'].astype('str')
df['Mã NPP'] = df['Mã NPP'].astype('str')

df['Tháng'] = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.month
df['Năm']  = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).dt.year

df['Tháng - năm'] = df['Năm'].astype('str')  + ' - ' + df['Tháng'].astype('str')
df['Tháng - năm'] = df['Tháng - năm'].map({'2022 - 8': '2022 - 08',
                                   '2023 - 8': '2023 - 08',
                                   '2022 - 9': '2022 - 09',
                                   '2023 - 9': '2023 - 09',
                                   '2022 - 7': '2022 - 07',
                                   '2023 - 7': '2023 - 07',
                                   '2022 - 6': '2022 - 06',
                                   '2023 - 6': '2023 - 06',
                                   '2022 - 5': '2022 - 05',
                                   '2023 - 5': '2023 - 05',
                                   '2022 - 4': '2022 - 04',
                                   '2023 - 4': '2023 - 04',
                                   '2022 - 3': '2022 - 03',
                                   '2023 - 3': '2023 - 03',
                                   '2022 - 2': '2022 - 02',
                                   '2023 - 2': '2023 - 02',
                                   '2022 - 1': '2022 - 01',
                                   '2023 - 1': '2023 - 01',
                                   '2022 - 10': '2022 - 10',
                                   '2023 - 10': '2023 - 10',
                                   '2022 - 11': '2022 - 11',
                                   '2023 - 11': '2023 - 11',
                                   '2022 - 12': '2022 - 12',
                                   '2023 - 12': '2023 - 12',})

df['Mã hệ thống'] = df['Tên KH'].str.split(' ').agg(lambda x: x[0])
df['Hệ thống'] = df['Mã hệ thống'].map({'VMP': 'Vincommerce',
                                        'VM': 'Vincommerce',
                                        'Coopfood': 'Sài Gòn Coop',
                                        'MM': 'Mega Market',
                                        'BigC': 'BigC và Go!',
                                        'Lotte': 'Lotte Mart',
                                        'Coopmart': 'Sài Gòn Coop',
                                        'BHX': 'Bách Hóa Xanh'})

df['Ngày lấy đơn'] = df['Ngày lấy đơn'].str.split(' ').agg(lambda x: x[0])

col1, col2 = st.sidebar.columns(2)

with col1:
    months = st.radio('Chọn tháng: ', df['Tháng - năm'].sort_values(ascending = True).unique())

with col2:
    growth_month = st.radio('Chọn tháng so sánh: ', df['Tháng - năm'].sort_values(ascending = True).unique())

systems = st.sidebar.radio('Chọn hệ thống: ', df['Hệ thống'].sort_values(ascending = True).unique())

df_system = df[df['Tháng - năm'] == months]
df_system = df_system[df_system['Hệ thống'] == systems]

df_new = df[df['Tháng - năm'] == growth_month]
df_new = df_new[df_new['Hệ thống'] == systems]

growth = format(round((df_system['Thành tiền'].sum() - df_new['Thành tiền'].sum()) / df_new['Thành tiền'].sum(), 2), '.2%')

sys = df_system.groupby(by = 'Ngày lấy đơn').agg({'Thành tiền': 'sum'}).reset_index()

df_total = df[df['Tháng - năm'] == months]
df_total_new = df[df['Tháng - năm'] == growth_month]
total_growth = (df_total['Thành tiền'].sum() - df_total_new['Thành tiền'].sum()) / df_total_new['Thành tiền'].sum()

col6, col7, col8 = st.columns(3)

with col7:
    st.metric(label = 'Tổng doanh số toàn khu vực ' + months + ' (VNĐ)', value = format(df_total['Thành tiền'].sum(), ','), delta = format(round(total_growth, 2), '.2%'))


df_total['Nhóm sản phẩm'] = df_total['Tên sản phẩm'].map({
    'Fa.36h': 'Hộp nguyên chất',
    'Fl.36h': 'Hộp nguyên chất',
    'Fa.10h': 'Hộp 1 lít',
    'Ca.10h': 'Hộp 1 lít',
    'Fa.40b': 'Bịch nguyên chất',
    'Fl.40b': 'Bịch nguyên chất',
    'Ft.36h': 'Nguyên chất vị mới',
    'Fc.36h': 'Nguyên chất vị mới',
    'Fc.40b': 'Nguyên chất vị mới',
    'Fs.36h': 'Nguyên chất vị mới',
    'Fs.40b': 'Nguyên chất vị mới',
    'Fg.36h': 'Nguyên chất vị mới',
    'Ca.36h': 'Hộp canxi',
    'Ca.40b': 'Bịch canxi',
    'Cl.36h': 'Hộp canxi',
    'Cl.40b': 'Bịch canxi',
    'Cf.36h': 'Canxi vị mới',
    'Ch.36h': 'Canxi vị mới',
    'Cs.36h': 'Canxi vị mới',
    'Cp.36h': 'Canxi vị mới',
    'Cp.40b': 'Canxi vị mới',
    'Ct.36h': 'Canxi vị mới',
    'Ct.40b': 'Canxi vị mới',
    'Fd.36h': 'Fami go',
    'Fd.40b': 'Fami go',
    'Fm.36h': 'Fami go',
    'Fm.40b': 'Fami go',
    'Vo.30h': 'Sữa chua uống',
    'Vs.30h': 'Sữa chua uống',
    'Vp.30h': 'Sữa chua uống',
})

df_total_new['Nhóm sản phẩm'] = df_total_new['Tên sản phẩm'].map({
    'Fa.36h': 'Hộp nguyên chất',
    'Fl.36h': 'Hộp nguyên chất',
    'Fa.10h': 'Hộp 1 lít',
    'Ca.10h': 'Hộp 1 lít',
    'Fa.40b': 'Bịch nguyên chất',
    'Fl.40b': 'Bịch nguyên chất',
    'Ft.36h': 'Nguyên chất vị mới',
    'Fc.36h': 'Nguyên chất vị mới',
    'Fc.40b': 'Nguyên chất vị mới',
    'Fs.36h': 'Nguyên chất vị mới',
    'Fs.40b': 'Nguyên chất vị mới',
    'Fg.36h': 'Nguyên chất vị mới',
    'Ca.36h': 'Hộp canxi',
    'Ca.40b': 'Bịch canxi',
    'Cl.36h': 'Hộp canxi',
    'Cl.40b': 'Bịch canxi',
    'Cf.36h': 'Canxi vị mới',
    'Ch.36h': 'Canxi vị mới',
    'Cs.36h': 'Canxi vị mới',
    'Cp.36h': 'Canxi vị mới',
    'Cp.40b': 'Canxi vị mới',
    'Ct.36h': 'Canxi vị mới',
    'Ct.40b': 'Canxi vị mới',
    'Fd.36h': 'Fami go',
    'Fd.40b': 'Fami go',
    'Fm.36h': 'Fami go',
    'Fm.40b': 'Fami go',
    'Vo.30h': 'Sữa chua uống',
    'Vs.30h': 'Sữa chua uống',
    'Vp.30h': 'Sữa chua uống',
})

total_flavor = df_total.groupby(by = 'Nhóm sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
total_flavor_new = df_total_new.groupby(by = 'Nhóm sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
total_flavor_new = total_flavor_new.rename(columns = {'Hàng bán (Thùng)': 'Hàng bán'})

final_flavor = total_flavor.set_index('Nhóm sản phẩm').join(total_flavor_new.set_index('Nhóm sản phẩm')).reset_index()
final_flavor['Tăng trưởng (%)'] = (final_flavor['Hàng bán (Thùng)'] - final_flavor['Hàng bán']) / final_flavor['Hàng bán']

st.subheader('Tăng trưởng theo nhóm sản phẩm')
barChart_growth_flavor = px.bar(final_flavor, x = final_flavor['Nhóm sản phẩm'], y = final_flavor['Tăng trưởng (%)'])
st.plotly_chart(barChart_growth_flavor, use_container_width = True, height = 200)
st.markdown('---')

center,centerr,centerrr = st.columns(3)
with centerr:
    st.header(systems)

col3, col4, col5 = st.columns(3)
with col3:
    # Metrics
    st.metric(label = 'Tổng doanh số ' + months + ' (VNĐ)', value  = (format(df_system['Thành tiền'].sum(), ',')) , delta = growth,)
with col4:
    quality = df_system.groupby(by = 'Ngày lấy đơn').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    quantity = quality['Ngày lấy đơn'].nunique()
    quality_order = round(quality['Hàng bán (Thùng)'].sum() / quantity, 2)

    quality2 = df_new.groupby(by = 'Ngày lấy đơn').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    quantity2 = quality2['Ngày lấy đơn'].nunique()
    quality_order2 = round(quality2['Hàng bán (Thùng)'].sum() / quantity2, 2)

    quality_order_growth = (quality_order - quality_order2) / quality_order2

    st.metric(label = 'Chất lượng đơn hàng ' + months + ' (Thùng/đơn)', value = quality_order , delta = format(round(quality_order_growth, 2), '.2%'))

with col5:
    quan_final = (quantity - quantity2) / quantity2
    st.metric(label = 'Đơn hàng thành công '+ months + ' (Đơn)', value = quantity, delta = format(round(quan_final, 2), '.2%'))
    

# Line chart
st.subheader('Doanh số theo ngày')
lineChart = px.line(sys, x = sys['Ngày lấy đơn'], y = sys['Thành tiền'])
st.plotly_chart(lineChart, use_container_width = True, height = 200)

# Group of SKUs

df_system['Hương vị'] = df_system['Tên sản phẩm'].map({
    'Fa.36h': 'Hộp nguyên chất',
    'Fl.36h': 'Hộp nguyên chất',
    'Fa.10h': 'Hộp 1 lít',
    'Ca.10h': 'Hộp 1 lít',
    'Fa.40b': 'Bịch nguyên chất',
    'Fl.40b': 'Bịch nguyên chất',
    'Ft.36h': 'Nguyên chất vị mới',
    'Fc.36h': 'Nguyên chất vị mới',
    'Fc.40b': 'Nguyên chất vị mới',
    'Fs.36h': 'Nguyên chất vị mới',
    'Fs.40b': 'Nguyên chất vị mới',
    'Fg.36h': 'Nguyên chất vị mới',
    'Ca.36h': 'Hộp canxi',
    'Ca.40b': 'Bịch canxi',
    'Cl.36h': 'Hộp canxi',
    'Cl.40b': 'Bịch canxi',
    'Cf.36h': 'Canxi vị mới',
    'Ch.36h': 'Canxi vị mới',
    'Cs.36h': 'Canxi vị mới',
    'Cp.36h': 'Canxi vị mới',
    'Cp.40b': 'Canxi vị mới',
    'Ct.36h': 'Canxi vị mới',
    'Ct.40b': 'Canxi vị mới',
    'Fd.36h': 'Fami go',
    'Fd.40b': 'Fami go',
    'Fm.36h': 'Fami go',
    'Fm.40b': 'Fami go',
    'Vo.30h': 'Sữa chua uống',
    'Vs.30h': 'Sữa chua uống',
    'Vp.30h': 'Sữa chua uống',
})

st.subheader('Sản lượng theo hương vị')

flavors = df_system.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
flavors = flavors.sort_values('Hàng bán (Thùng)', ascending = False)
barChart = px.bar(flavors, x = flavors['Hương vị'], y = flavors['Hàng bán (Thùng)'])
st.plotly_chart(barChart, use_container_width = True, height = 200)

df_new['Hương vị'] = df_new['Tên sản phẩm'].map({
    'Fa.36h': 'Hộp nguyên chất',
    'Fl.36h': 'Hộp nguyên chất',
    'Fa.10h': 'Hộp 1 lít',
    'Ca.10h': 'Hộp 1 lít',
    'Fa.40b': 'Bịch nguyên chất',
    'Fl.40b': 'Bịch nguyên chất',
    'Ft.36h': 'Nguyên chất vị mới',
    'Fc.36h': 'Nguyên chất vị mới',
    'Fc.40b': 'Nguyên chất vị mới',
    'Fs.36h': 'Nguyên chất vị mới',
    'Fs.40b': 'Nguyên chất vị mới',
    'Fg.36h': 'Nguyên chất vị mới',
    'Ca.36h': 'Hộp canxi',
    'Ca.40b': 'Bịch canxi',
    'Cl.36h': 'Hộp canxi',
    'Cl.40b': 'Bịch canxi',
    'Cf.36h': 'Canxi vị mới',
    'Ch.36h': 'Canxi vị mới',
    'Cs.36h': 'Canxi vị mới',
    'Cp.36h': 'Canxi vị mới',
    'Cp.40b': 'Canxi vị mới',
    'Ct.36h': 'Canxi vị mới',
    'Ct.40b': 'Canxi vị mới',
    'Fd.36h': 'Fami go',
    'Fd.40b': 'Fami go',
    'Fm.36h': 'Fami go',
    'Fm.40b': 'Fami go',
    'Vo.30h': 'Sữa chua uống',
    'Vs.30h': 'Sữa chua uống',
    'Vp.30h': 'Sữa chua uống',
})

flavors_new = df_new.groupby(by = 'Hương vị').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
flavors_new = flavors_new.sort_values('Hàng bán (Thùng)', ascending = False)
flavors_new = flavors_new.rename(columns = {'Hàng bán (Thùng)': 'Hàng bán'})

flavors_growth = flavors.set_index('Hương vị').join(flavors_new.set_index('Hương vị')).reset_index()

flavors_growth['Tăng trưởng (%)'] = (flavors_growth['Hàng bán (Thùng)'] - flavors_growth['Hàng bán']) / flavors_growth['Hàng bán']
st.subheader('Tăng trưởng theo nhóm sản phẩm')
barChart_growth = px.bar(flavors_growth, x = flavors_growth['Hương vị'], y = flavors_growth['Tăng trưởng (%)'])
st.plotly_chart(barChart_growth, use_container_width = True, height = 200)

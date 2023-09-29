import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'Dashboard', layout = 'wide', page_icon = ':trophy:')
st.sidebar.title('MY DASHBOARD')

upload = st.file_uploader('Upload your file here: ', ['csv'])
if upload:
    df = pd.read_csv(upload)
    os.makedirs('dataset', exist_ok=True) 
    df.to_csv('dataset/' + upload.name, index = False, encoding = 'utf-8')
    new_df = pd.read_csv('dataset/' + upload.name)
    # st.write(new_df)

    col1, col2 = st.columns((2))

    df['Ngày lấy đơn'] = pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)

    startDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).min()
    endDate = (pd.to_datetime(df['Ngày lấy đơn'], dayfirst = True)).max()

    # Process
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
    
    SBM = df.groupby(by = 'Tháng - năm').agg({'Thành tiền': 'sum'}).reset_index()
    months = st.subheader('Hoàn thành tiến độ tháng')
    # process['Hoàn thành'] = process['Thành tiền'] / process['Target'].astype('float64') * 100

    # months = st.radio('Chọn tháng: ', process['Month'])
    # st.table(process[process['Month'] == months])

    with col1:
        date1 = pd.to_datetime(st.sidebar.date_input('Từ ngày: ', startDate), dayfirst = True)

    with col2:
        date2 = pd.to_datetime(st.sidebar.date_input('Đến ngày: ', endDate), dayfirst = True)

    df = df[(df['Ngày lấy đơn'] >= date1) & (df['Ngày lấy đơn'] <= date2)].copy()

    # Line chart   
    lineChart = px.line(SBM, x = SBM['Tháng - năm'], y = SBM['Thành tiền'])
    st.plotly_chart(lineChart, use_container_width = True, height = 200)


    col3, col4 = st.columns((2))

    with col3:
            
        # Bar chart by Suppliers

        sup = df.groupby(by = 'Tên NPP').agg({'Thành tiền': 'sum'}).reset_index()

        barChartSuppliers = px.bar(sup, sup['Tên NPP'], sup['Thành tiền'], title = 'DOANH SỐ BÁN RA THEO NHÀ PHÂN PHỐI')
        st.plotly_chart(barChartSuppliers, use_container_width = True, height = 200)

    with col4:
        # Pie chart

        sys = df['Tên KH'].str.split(' ')
        system = sys.agg(lambda x: x[0])
        df['Hệ thống'] = system
        systems = df.groupby(by = 'Hệ thống').agg({'Thành tiền': 'sum'}).reset_index()
        systems['Hệ thống'] = systems['Hệ thống'].map({
            'BHX': 'Bách Hóa Xanh',
            'VMP': 'Vincommerce',
            'Lotte': 'Lotte Mart',
            'MM': 'Mega Market',
            'VM': 'Vincommerce',
            'BigC': 'BigC và Go!',
            'Coopfood': 'Sài Gòn Coop',
            'Coopmart': 'Sài Gòn Coop'
        })
        pieChart = px.pie(systems, values = systems['Thành tiền'], names = systems['Hệ thống'], title = 'TỶ LỆ ĐÓNG GÓP CỦA CÁC HỆ THỐNG SIÊU THỊ')
        st.plotly_chart(pieChart, use_container_width = True, height = 200)


    # Sorting by SKUs

    skus = df.groupby(by = 'Tên sản phẩm').agg({'Hàng bán (Thùng)': 'sum'}).reset_index()
    skus = skus.sort_values('Hàng bán (Thùng)', ascending = True)

    barChartSkus = px.bar(skus, y = skus['Tên sản phẩm'], x = skus['Hàng bán (Thùng)'], title = 'Sản lượng bán ra theo SKUs', orientation = 'h')
    st.plotly_chart(barChartSkus, use_container_width = True, height = 1000)
else:
    st.warning('Please upload your file to continue!')
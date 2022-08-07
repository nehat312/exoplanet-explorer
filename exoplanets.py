## LIBRARY IMPORTS ##
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly as ply
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from PIL import Image

# import dash as dash
# from dash import dash_table
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output
# from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc

# import scipy.stats as stats
# import statistics


## VISUAL SETTINGS ##

# pd.options.display.float_format = '${:,.2f}'.format
# pd.set_option('display.max_colwidth', 200)


## DATA IMPORTS ##

engine_csv = r'https://raw.githubusercontent.com/nehat312/prop-swap/main/data/engine.csv'
all_investor_idx = pd.read_csv(engine_csv) #, header=0, index_col=0 #, encoding='utf-8'

abspath_curr = ''

planetary_systems = abspath_curr + '/data/NASA_Planetary_Systems-4-24-22'
exoplanets = abspath_curr + '/data/NASA_Exoplanets-4-22-22'

#planetary_systems = pd.read_csv(planetary_systems + '.csv', index_col='pl_name')
#exoplanets = pd.read_csv(exoplanets + '.csv', index_col='pl_name')

## VARIABLE ASSIGNMENT

all_investor_idx = all_investor_idx.sort_values(by='TTL_VOL_RANK')

investor_cols = ['INVESTOR', 'INVESTOR_TYPE', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', 'C-SUITE']
mf_cols = ['INVESTOR', 'INVESTOR_TYPE', 'MF_AVG_PRICE_MM', 'MF_UNITS_PROP', 'MF_AVG_PPU',  'MF_QUALITY', 'MF_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE'] # AVG_QUALITY, 'TTL_VOL_RANK', 'TTL_SF_RANK',
sc_cols = ['INVESTOR', 'INVESTOR_TYPE', 'SC_AVG_PRICE_MM', 'SC_SF_PROP', 'SC_AVG_PSF',  'SC_QUALITY', 'SC_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE']
nnn_cols = ['INVESTOR', 'INVESTOR_TYPE', 'NNN_AVG_PRICE_MM', 'NNN_SF_PROP', 'NNN_AVG_PSF',  'NNN_QUALITY', 'NNN_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE']
mall_cols = ['INVESTOR', 'INVESTOR_TYPE', 'MALL_AVG_PRICE_MM', 'MALL_SF_PROP', 'MALL_AVG_PSF',  'MALL_QUALITY', 'MALL_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE']
ss_cols = ['INVESTOR', 'INVESTOR_TYPE', 'SS_AVG_PRICE_MM', 'SS_SF_PROP',  'SS_AVG_PSF',  'SS_QUALITY', 'SS_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE']
ind_cols = ['INVESTOR', 'INVESTOR_TYPE', 'IND_AVG_PRICE_MM', 'IND_SF_PROP', 'IND_AVG_PSF',  'IND_QUALITY', 'IND_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', ]
fs_cols = ['INVESTOR', 'INVESTOR_TYPE', 'FS_AVG_PRICE_MM', 'FS_KEYS_PROP', 'FS_AVG_PPK',  'FS_QUALITY', 'FS_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', ]
ls_cols = ['INVESTOR', 'INVESTOR_TYPE', 'LS_AVG_PRICE_MM', 'LS_KEYS_PROP', 'LS_AVG_PPK',  'LS_QUALITY', 'LS_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', ]
cbd_cols = ['INVESTOR', 'INVESTOR_TYPE', 'CBD_AVG_PRICE_MM', 'CBD_SF_PROP', 'CBD_AVG_PSF',  'CBD_QUALITY', 'CBD_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', ]
sub_cols = ['INVESTOR', 'INVESTOR_TYPE', 'SUB_AVG_PRICE_MM', 'SUB_SF_PROP', 'SUB_AVG_PSF',  'SUB_QUALITY', 'SUB_VOL_RANK', 'CITY', 'STATE', 'COUNTRY', 'MSA', 'WEBSITE', ]


# #%%

#####################
### STREAMLIT APP ###
#####################

## CONFIGURATION ##
st.set_page_config(page_title="EXOPLANET-EXPLORER") #, page_icon=":smirk:"

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)


## INTRODUCTION ##
st.container()

st.title('EXOPLANET EXPLORER')
st.subheader('*NASA-CalTECH Archives*')

prop_params_header = st.header('INPUT PARAMETERS:')

sector = st.selectbox('PARAMS:',
                      ('TBU',
                       'TBU'
                       'TBU'
                       'TBU'
                       'TBU')
                      )

# st.sidebar.xyz

with st.form('PARAMS FORM'):
    if sector == "MULTIFAMILY":
        prop_size = st.number_input('*TOTAL MF UNITS [25-1,000 UNITS]', min_value=25, max_value=500, step=25, value=100) #list(range(25,750,25)))
        min_prop_price = st.number_input('*MINIMUM VALUATION [$0MM-$100MM]', min_value=0, max_value=100, value=10, step=5)
        prop_qual = st.selectbox('*PROPERTY QUALITY [1-5]:', list(range(1, 6, 1)))


    params_submit = st.form_submit_button('FORM SUBMIT')

    @st.cache(persist=True, allow_output_mutation=True)
    def filter_buyers(sector, prop_size, min_prop_price, prop_qual):
      if sector == 'MULTIFAMILY':
        for investors in all_investor_idx:
          mf_size_filter = all_investor_idx[all_investor_idx.MF_UNITS_PROP >= prop_size]
          mf_min_price_filter = mf_size_filter[mf_size_filter.MF_AVG_PRICE_MM >= min_prop_price]
          mf_qual_filter = mf_min_price_filter[(mf_min_price_filter.MF_QUALITY >= (prop_qual-1)) & (mf_min_price_filter.MF_QUALITY <= (prop_qual+1))]
          mf_buyer_recs = mf_qual_filter.sort_values(by = 'MF_VOL_RANK', ascending = True)[:50]
          mf_buyer_recs = pd.DataFrame(data = mf_buyer_recs, columns = mf_cols)
        return mf_buyer_recs
      elif sector == 'STRIP CENTER':
        for investors in all_investor_idx:
          sc_size_filter = all_investor_idx[all_investor_idx['SC_SF_PROP'] >= prop_size]
          sc_min_price_filter = sc_size_filter[sc_size_filter['SC_AVG_PRICE_MM'] >= min_prop_price]
          sc_qual_filter = sc_min_price_filter[(sc_min_price_filter['SC_QUALITY'] >= (prop_qual-1)) & (sc_min_price_filter['SC_QUALITY'] <= (prop_qual+1))]
          sc_buyer_recs = sc_qual_filter.sort_values(by = 'SC_VOL_RANK', ascending = True)[:50]
          sc_buyer_recs = pd.DataFrame(data = sc_buyer_recs, columns = sc_cols)
        return sc_buyer_recs


## TARGET INVESTOR DATAFRAME ##
    if params_submit:
        buyer_rec_df = filter_buyers(sector, prop_size, min_prop_price, prop_qual)

        # st.write("TARGETED INVESTOR POOL:")
        # st.dataframe(buyer_rec_df)
            # buyer_rec_df = buyer_rec_df.set_index('INVESTOR')

        ## DATAFRAME STYLING ##

        # def df_style_map(val):
        #     if val == 'United States':
        #         color = 'black'
        #     else:
        #         color = 'pink'
        #         return f'background-color: {color}'
        #
        # st.dataframe(buyer_rec_df.style.applymap(df_style_map, subset=['COUNTRY']))

        ## STYLE DICTIONARY ##

        YlOrRd = px.colors.sequential.YlOrRd
        Mint = px.colors.sequential.Mint
        Electric = px.colors.sequential.Electric
        Sunsetdark = px.colors.sequential.Sunsetdark
        Sunset = px.colors.sequential.Sunset
        Tropic = px.colors.diverging.Tropic

        chart_labels = {'INVESTOR_TYPE': 'INVESTOR TYPE',

                        }


## VALUATION METRICS ##
        if sector == 'MULTIFAMILY':
            per_unit_valuation = round(buyer_rec_df['MF_AVG_PPU'].mean())
            prop_valuation = per_unit_valuation * prop_size
            st.write(f'ESTIMATED PROPERTY VALUATION: ${(prop_valuation / 1_000_000):.2f}MM or {per_unit_valuation:.0f}/UNIT')
            # st.metric('ESTIMATED PROPERTY VALUATION: $', (prop_valuation / 1_000_000))
            # st.metric('ESTIMATED PROPERTY VALUATION: $/UNIT', per_unit_valuation)
            st.write("TARGETED INVESTOR POOL:")
            st.dataframe(buyer_rec_df)

            mf_chart_1 = px.scatter(buyer_rec_df, #all_investor_idx
                                    x=buyer_rec_df['MF_AVG_PRICE_MM'],
                                    y=buyer_rec_df['MF_AVG_PPU'],
                                    # color=buyer_rec_df['INVESTOR_TYPE'],
                                    color=buyer_rec_df['MF_AVG_PPU'],
                                    color_continuous_scale=Sunsetdark, #'YlOrRd', #'Tropic',
                                    color_discrete_sequence=Sunsetdark,
                                    hover_name=buyer_rec_df['INVESTOR'],
                                    hover_data=buyer_rec_df[['MSA']],
                                    title='TARGETED INVESTOR POOL',
                                    labels=chart_labels,
                                    )

            st.plotly_chart(mf_chart_1, use_container_width=False, sharing="streamlit")


            mf_chart_2 = px.bar(buyer_rec_df,
                                x=buyer_rec_df['INVESTOR'],
                                y=buyer_rec_df['MF_AVG_PPU'],
                                color=buyer_rec_df['INVESTOR_TYPE'],
                                color_continuous_scale=Tropic,
                                color_discrete_sequence=Tropic,
                                # category_orders={'total descending'},
                                hover_name=buyer_rec_df['INVESTOR'],
                                hover_data=buyer_rec_df[['MSA']],
                                labels=chart_labels,
                                barmode='relative',
                                # size=buyer_rec_df['SC_VOL_RANK'],
                                height=500,
                                # width=400,
                                )

            st.plotly_chart(mf_chart_2, use_container_width=False, sharing="streamlit")



            #pattern_shape = "nation", pattern_shape_sequence = [".", "x", "+"]

            # fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
            #        category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})

            # fig = px.scatter_matrix(df, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")

            # fig = px.parallel_categories(df, color="size", color_continuous_scale=px.colors.sequential.Inferno)

            # fig = px.parallel_coordinates(df, color="species_id", labels={"species_id": "Species",
            #                   "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
            #                   "petal_width": "Petal Width", "petal_length": "Petal Length", },
            #                     color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)


#######################
## TABLEAU EMBEDDING ##
#######################

# def main():
#     html_temp = """<div class='tableauPlaceholder' id='viz1659419844202' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;MS&#47;MS874Y84Y&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;MS874Y84Y' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;MS&#47;MS874Y84Y&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1659419844202');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
#     components.html(html_temp, height=600) #width=400,
#
# if __name__ == "__main__":
#     main()

# ## IMAGE EMBEDDING ##
# test_img = Image.open('ROTATE.jpg')
# st.image(test_img)

## EXTERNAL LINKS ##

left_column, right_column = st.columns(2)
left_button = left_column.button('GITHUB REPOSITORY')
right_button = right_column.button('CONTACT INFORMATION')
if left_button:
    left_column.write('https://github.com/nehat312/exoplanet-explorer')
if right_button:
    right_column.write('')
    # left_column.write('https://public.tableau.com/shared/S4GKR7QYB?:display_count=n&:origin=viz_share_link')




# st.success('')
# st.warning('')
# st.write('*~BETA MODE~*')

st.stop()


### SCRATCH NOTES



# CONFIG TEMPLATE
    # st.set_page_config(page_title="CSS hacks", page_icon=":smirk:")
    #
    # c1 = st.container()
    # st.markdown("---")
    # c2 = st.container()
    # with c1:
    #     st.markdown("Hello")
    #     st.slider("World", 0, 10, key="1")
    # with c2:
    #     st.markdown("Hello")
    #     st.slider("World", 0, 10, key="2")

# STYLE WITH CSS THROUGH MARKDOWN
    # st.markdown("""
    # <style>
    # div[data-testid="stBlock"] {
    #     padding: 1em 0;
    #     border: thick double #32a1ce;
    # }
    # </style>
    # """, unsafe_allow_html=True)


# STYLE WITH JS THROUGH HTML IFRAME
    # components.html("""
    # <script>
    # const elements = window.parent.document.querySelectorAll('div[data-testid="stBlock"]')
    # console.log(elements)
    # elements[0].style.backgroundColor = 'paleturquoise'
    # elements[1].style.backgroundColor = 'lightgreen'
    # </script>
    # """, height=0, width=0)


# st.markdown("""
#             <style>
#             div[data-testid="stBlock"] {padding: 1em 0; border: thick double #32a1ce; color: blue}
#             </style>
#             """,
#             unsafe_allow_html=True)

# style={'textAlign': 'Center', 'backgroundColor': 'rgb(223,187,133)',
#                                            'color': 'black', 'fontWeight': 'bold', 'fontSize': '24px',
#                                            'border': '4px solid black', 'font-family': 'Arial'}),


#st.spinner()
#with st.spinner(text='CONNECTING'):
#    time.sleep(5)
#    st.success('LIVE')

#streamlit. slider ( label , min_value=None , max_value=None , value=None , step=None , format=None , key=None )
## LIBRARY IMPORTS ##
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np

import plotly as ply
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from PIL import Image

# import matplotlib.pyplot as plt
# import seaborn as sns
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


## DIRECTORY CONFIGURATION ##
abs_path = r'https://raw.githubusercontent.com/nehat312/exoplanet-explorer/main'
exoplanet_path = abs_path + '/data/NASA_Exoplanets-8-7-22.csv'

## DATA IMPORT ##
exoplanets = pd.read_csv(exoplanet_path, header=0, index_col='loc_rowid') #, header=0, index_col='pl_name'#,
exoplanets.sort_values(by='disc_year', inplace=True)

# exoplanets.dropna(inplace=True)

# print(exoplanets.info())
# print(exoplanets.columns)
# print(exoplanets.head())

# pd.to_numeric(exoplanets['disc_year'])
# exoplanets['disc_year'].astype(int)

## FORMAT / STYLE ##
YlOrRd = px.colors.sequential.YlOrRd
Mint = px.colors.sequential.Mint
Electric = px.colors.sequential.Electric
Sunsetdark = px.colors.sequential.Sunsetdark
Sunset = px.colors.sequential.Sunset
Tropic = px.colors.diverging.Tropic
Temps = px.colors.diverging.Temps
Tealrose = px.colors.diverging.Tealrose
Blackbody = px.colors.sequential.Blackbody
Ice = px.colors.sequential.ice
Ice_r = px.colors.sequential.ice_r
Dense = px.colors.sequential.dense


chart_labels = {'pl_name':'PL. NAME',
                'host_name':'ST. NAME',
                'sy_star_count':'SYS. STARS (#)',
                'sy_planet_count':'SYS. PLANETS (#)',
                'disc_method':'DISC. METHOD',
                'disc_year':'DISC. YEAR',
                'disc_facility':'DISC. FACILITY',
                'disc_telescope':'DISC. TELESCOPE',
                'disc_instrument':'DISC. INSTRUMENT',
                'pl_orbper':'ORB. PERIOD',
                'pl_orbeccen':'ORB. ECCENTRICITY',
                'pl_orbsmax':'ORB. SPEED',
                'pl_rade':'PL. RADIUS (E)',
                'pl_radj':'PL. RADIUS (J)',
                'pl_bmasse':'PL. MASS (E)',
                'pl_bmassj':'PL. MASS (J)',
                'st_temp_eff_k':'ST. TEMP. (K)',
                'st_radius':'ST. RADIUS',
                'st_mass':'ST. MASS',
                'st_metallicity':'METALLICITY',
                'st_surf_gravity':'SURFACE GRAVITY',
                'sy_distance_pc':'ST. DISTANCE (PC)',
                'ra':'RIGHT ASCENSION',
                'dec':'DECLINATION',
                'glon':'GALACTIC LONGITUDE',
                'glat':'GALACTIC LATITUDE'
                }

exo_planet_list = list(exoplanets['pl_name'])
exo_star_list = list(exoplanets['host_name'])
disc_telescope_list = list(exoplanets['disc_telescope'])
disc_method_list = list(exoplanets['disc_method'])
disc_facility_list = list(exoplanets['disc_facility'])
disc_year_list = list(exoplanets['disc_year'])

# print(exoplanets.disc_method.unique())

exo_drop_na = exoplanets.dropna()
exo_with_temp = exoplanets[['st_temp_eff_k']].dropna()
exo_with_dist = exoplanets[['sy_distance_pc']].dropna()


# print(len(exo_drop_na))
# print(len(exo_with_temp))
# print(len(exo_with_dist))

# mean_year = 2022
# exoplanets['disc_year'].fillna(mean_year, inplace=True)
# print(exoplanets['disc_year'].unique())

# disc_method_time = exoplanets.groupby(['disc_method']).count() #, 'disc_year'
# print(disc_method_time[:30])
# #%%
# print(disc_method_time.disc_year)



#####################
### STREAMLIT APP ###
#####################

## CONFIGURATION ##
st.set_page_config(page_title='EXOPLANET EXPLORER', layout='wide', initial_sidebar_state='auto') #, page_icon=":smirk:"

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)


## SIDEBAR ##
# st.sidebar.xyz


## HEADER ##
st.container()

st.title('EXOPLANET EXPLORER')
st.subheader('*Sourced from NASA-CalTECH mission archives*')



scatter_3d_1 = px.scatter_3d(exo_drop_na,
                             x=exo_drop_na['dec'],
                             y=exo_drop_na['ra'],
                             z=exo_drop_na['sy_distance_pc'],
                             color=exo_drop_na['st_temp_eff_k'],
                             color_discrete_sequence=Ice_r,
                             color_continuous_scale=Ice_r,
                             size=exo_drop_na['pl_rade'],
                             size_max=50,
                             # symbol=exo_drop_na['disc_year'],
                             hover_name=exo_drop_na['pl_name'],
                             hover_data=exo_drop_na[['host_name', 'disc_facility', 'disc_telescope']],
                             title='EXOPLANET POPULATION --- RIGHT ASCENSION / DECLINATION / DISTANCE',
                             labels=chart_labels,
                             # range_x=[0,360],
                             # range_y=[-50,50],
                             range_z=[0,2500],
                             # range_color=Sunsetdark,
                             opacity=.8,
                             height=800,
                             width=1600,
                             )

disc_year_1 = px.bar(exoplanets,
                     # x=exoplanets['disc_year'],
                     y=exoplanets['disc_method'],
                     color=exoplanets['disc_method'],
                     color_discrete_sequence=Temps,
                     color_continuous_scale=Temps,
                     hover_name=exoplanets['pl_name'],
                     hover_data=exoplanets[['host_name', 'disc_telescope', 'disc_facility']],
                     # barmode='group',
                     # animation_frame=exoplanets['disc_year'],
                     title='EXOPLANET DISCOVERY METHOD',
                     labels=chart_labels,
                     range_x=[0, 4000],
                     # range_y=disc_method_list,
                     # height=800,
                     width=800,
                     orientation='h',
                     )



disc_info_1 = px.histogram(exoplanets,
                           x=exoplanets['disc_method'],
                           color=exoplanets['disc_facility'],
                           color_discrete_sequence=Temps,
                           hover_name=exoplanets['pl_name'],
                           hover_data=exoplanets[['host_name', 'disc_facility', 'disc_telescope', 'sy_star_count', 'sy_planet_count']],
                           title='EXOPLANET DISCOVERY METHOD / FACILITY',
                           labels=chart_labels,
                           )

density_map_1 = px.density_contour(exoplanets,
                                   x=exoplanets['ra'],
                                   y=exoplanets['dec'],
                                   z=exoplanets['sy_distance_pc'],
                                   color=exoplanets['disc_method'],
                                   color_discrete_sequence=Temps,
                                   hover_name=exoplanets['pl_name'],
                                   hover_data=exoplanets[['host_name', 'disc_facility', 'disc_telescope', 'sy_star_count', 'sy_planet_count']],
                                   title='EXOPLANET RIGHT ASCENSION / DECLINATION',
                                   labels=chart_labels,
                                   )


# exo_map_1 = px.scatter_geo(exoplanets,
#                         lat=[['glat']],
#                         lon=[['glon']],
#                         title='EXOPLANET GLAT / GLON',
#                         labels=chart_labels,
#                         )

# exo_select_1 = px.(exoplanet_selection,
#                                  dimensions=exoplanets['pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_orbeccen'], #, 'pl_orbsmax'
#                                      # color=exoplanets['st_temp_eff_k'],
#                                      color_continuous_scale=Temps,
#                                      color_discrete_sequence=Temps,
#                                      hover_name=exoplanets['pl_name'],
#                                      hover_data=exoplanets[['host_name', 'sy_star_count', 'sy_planet_count']],
#                                      title='EXOPLANET ATTRIBUTES',
#                                      labels=chart_labels,
#                                      )

exo_matrix_1 = px.scatter_matrix(exoplanets,
                                     dimensions=['pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_orbeccen'], #, 'pl_orbsmax'
                                     color=exoplanets['st_temp_eff_k'],
                                     color_continuous_scale=Ice_r,
                                     color_discrete_sequence=Ice_r,
                                     hover_name=exoplanets['pl_name'],
                                     hover_data=exoplanets[['host_name', 'sy_star_count', 'sy_planet_count']],
                                     title='EXOPLANET ATTRIBUTES',
                                     labels=chart_labels,
                                 height=800,
                                 # width=800,
                                 )

star_matrix_1 = px.scatter_matrix(exoplanets,
                                     dimensions=['st_radius', 'st_mass', 'st_metallicity', 'st_surf_gravity'],
                                     color=exoplanets['st_temp_eff_k'],
                                     color_continuous_scale=Ice_r,
                                     color_discrete_sequence=Ice_r,
                                     hover_name=exoplanets['pl_name'],
                                     hover_data=exoplanets[['host_name', 'sy_star_count', 'sy_planet_count']],
                                     title='STAR ATTRIBUTES',
                                     labels=chart_labels,
                                  height=800,
                                  # width=800,
                                  )

exo_scatter_1 = px.scatter(exoplanets,
                         x=exoplanets['pl_rade'],
                         y=exoplanets['pl_bmasse'],
                         color=exoplanets['st_temp_eff_k'],
                         color_continuous_scale=Temps,
                         color_discrete_sequence=Temps,
                         hover_name=exoplanets['pl_name'],
                         hover_data=exoplanets[['host_name', 'disc_facility', 'disc_telescope', 'sy_star_count', 'sy_planet_count']],
                         title='EXOPLANET ATTRIBUTES',
                         labels=chart_labels,
                         )

star_scatter_1 = px.scatter(exoplanets,
                         x=exoplanets['st_radius'],
                         y=exoplanets['st_mass'],
                         color=exoplanets['st_temp_eff_k'],
                         color_continuous_scale=Temps,
                         color_discrete_sequence=Temps,
                         hover_name=exoplanets['host_name'],
                         hover_data=exoplanets[['disc_facility', 'disc_telescope', 'sy_star_count', 'sy_planet_count']],
                         title='HOST STAR ATTRIBUTES',
                         labels=chart_labels,
                         )

## SUBPLOTS ##
# subplots = make_subplots(rows=1, cols=2)
# subplots.add_trace(scatter_3d_1, row=1, col=1)
# subplots.add_trace(scatter_3d_1, row=1, col=2)
#

st.plotly_chart(scatter_3d_1, use_container_width=False, sharing="streamlit") #

left_col_1, right_col_1 = st.columns(2)
left_col_1.plotly_chart(exo_matrix_1, use_container_width=False, sharing="streamlit")
right_col_1.plotly_chart(star_matrix_1, use_container_width=False, sharing="streamlit")

st.plotly_chart(disc_year_1, use_container_width=False, sharing="streamlit")
st.plotly_chart(disc_info_1, use_container_width=False, sharing="streamlit")
st.plotly_chart(density_map_1, use_container_width=False, sharing="streamlit")


# st.plotly_chart(exo_scatter_1, use_container_width=False, sharing="streamlit")
# st.plotly_chart(star_scatter_1, use_container_width=False, sharing="streamlit")


exo_star_prompt = st.subheader('SELECT STAR:')
exo_star_selection = st.selectbox('EXO-STARS:', (exo_star_list))

exoplanet_prompt = st.subheader('SELECT EXOPLANET:')
exoplanet_selection = st.selectbox('EXOPLANETS:', (exo_planet_list))




# with st.form('PARAMS FORM'):
#     if sector == "MULTIFAMILY":
#         prop_size = st.number_input('*TOTAL MF UNITS [25-1,000 UNITS]', min_value=25, max_value=500, step=25, value=100) #list(range(25,750,25)))
#         min_prop_price = st.number_input('*MINIMUM VALUATION [$0MM-$100MM]', min_value=0, max_value=100, value=10, step=5)
#         prop_qual = st.selectbox('*PROPERTY QUALITY [1-5]:', list(range(1, 6, 1)))
#
#
#     params_submit = st.form_submit_button('FORM SUBMIT')
#
#     @st.cache(persist=True, allow_output_mutation=True)
#     def filter_buyers(sector, prop_size, min_prop_price, prop_qual):
#       if sector == 'MULTIFAMILY':
#         for investors in all_investor_idx:
#           mf_size_filter = all_investor_idx[all_investor_idx.MF_UNITS_PROP >= prop_size]
#           mf_min_price_filter = mf_size_filter[mf_size_filter.MF_AVG_PRICE_MM >= min_prop_price]
#           mf_qual_filter = mf_min_price_filter[(mf_min_price_filter.MF_QUALITY >= (prop_qual-1)) & (mf_min_price_filter.MF_QUALITY <= (prop_qual+1))]
#           mf_buyer_recs = mf_qual_filter.sort_values(by = 'MF_VOL_RANK', ascending = True)[:50]
#           mf_buyer_recs = pd.DataFrame(data = mf_buyer_recs, columns = mf_cols)
#         return mf_buyer_recs
#       elif sector == 'STRIP CENTER':
#         for investors in all_investor_idx:
#           sc_size_filter = all_investor_idx[all_investor_idx['SC_SF_PROP'] >= prop_size]
#           sc_min_price_filter = sc_size_filter[sc_size_filter['SC_AVG_PRICE_MM'] >= min_prop_price]
#           sc_qual_filter = sc_min_price_filter[(sc_min_price_filter['SC_QUALITY'] >= (prop_qual-1)) & (sc_min_price_filter['SC_QUALITY'] <= (prop_qual+1))]
#           sc_buyer_recs = sc_qual_filter.sort_values(by = 'SC_VOL_RANK', ascending = True)[:50]
#           sc_buyer_recs = pd.DataFrame(data = sc_buyer_recs, columns = sc_cols)
#         return sc_buyer_recs
#
#
# ## USER PARAMS DATAFRAME ##
#     if params_submit:
#         buyer_rec_df = filter_buyers(sector, prop_size, min_prop_price, prop_qual)

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




## VALUATION METRICS ##
        # if sector == 'MULTIFAMILY':
        #     per_unit_valuation = round(buyer_rec_df['MF_AVG_PPU'].mean())
        #     prop_valuation = per_unit_valuation * prop_size
        #     st.write(f'ESTIMATED PROPERTY VALUATION: ${(prop_valuation / 1_000_000):.2f}MM or {per_unit_valuation:.0f}/UNIT')
        #     # st.metric('ESTIMATED PROPERTY VALUATION: $', (prop_valuation / 1_000_000))
        #     # st.metric('ESTIMATED PROPERTY VALUATION: $/UNIT', per_unit_valuation)
        #     st.write("TARGETED INVESTOR POOL:")
        #     st.dataframe(buyer_rec_df)


#######################
## TABLEAU EMBEDDING ##
#######################

# def main():
#     html_temp = """<div class='tableauPlaceholder' id='viz1659419844202' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;MS&#47;MS874Y84Y&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;MS874Y84Y' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;MS&#47;MS874Y84Y&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1659419844202');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
#     components.html(html_temp, height=600) #width=400,
#
# if __name__ == "__main__":
#     main()

## IMAGE EMBEDDING ##
jwst_img_1 = Image.open('JWST-1.png')
st.image(jwst_img_1)



## EXTERNAL LINKS ##

github_link = '[GITHUB REPOSITORY](https://github.com/nehat312/exoplanet-explorer/)'
nasa_caltech_link = '[NASA ARCHIVES](https://exoplanetarchive.ipac.caltech.edu/)'

left_column, right_column = st.columns(2)
left_button = left_column.markdown(github_link, unsafe_allow_html=True)
right_button = right_column.markdown(nasa_caltech_link, unsafe_allow_html=True)

# left_button = left_column.button('GITHUB REPOSITORY')
# right_button = right_column.button('NASA ARCHIVES')
# if left_button:
#     # left_column.write('https://github.com/nehat312/exoplanet-explorer')
# if right_button:
    # right_column.write('https://exoplanetarchive.ipac.caltech.edu/')

    # st.markdown(github_link, unsafe_allow_html=True)
    # st.markdown(nasa_caltech_link, unsafe_allow_html=True)

# st.success('')
# st.warning('')

st.stop()


### INTERPRETATION ###

# Declination (DEC) is the celestial sphere's equivalent of latitude and it is expressed in degrees, as is latitude.
# For DEC, + and - refer to north and south, respectively.
# The celestial equator is 0° DEC, and the poles are +90° and -90°.

# Right ascension (RA) is the celestial equivalent of longitude.
# RA can be expressed in degrees, but it is more common to specify it in hours, minutes, and seconds of time:
    # the sky appears to turn 360° in 24 hours, or 15° in one hour.
    # So an hour of RA equals 15° of sky rotation.



### SCRATCH NOTES


## FONTS ##

# t = st.radio("Toggle to see font change", [True, False])
#
# if t:
#     st.markdown(
#         """
#         <style>
# @font-face {
#   font-family: 'Tangerine';
#   font-style: normal;
#   font-weight: 400;
#   src: url(https://fonts.gstatic.com/s/tangerine/v12/IurY6Y5j_oScZZow4VOxCZZM.woff2) format('woff2');
#   unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
# }
#
#     html, body, [class*="css"]  {
#     font-family: 'Tangerine';
#     font-size: 48px;
#     }
#     </style>
#
#     """,
#         unsafe_allow_html=True,
#     )
#
# "# Hello"
#
# """This font will look different, based on your choice of radio button"""

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

#pattern_shape = "nation", pattern_shape_sequence = [".", "x", "+"]

            # fig = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
            #        category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})

            # fig = px.scatter_matrix(df, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")

            # fig = px.parallel_categories(df, color="size", color_continuous_scale=px.colors.sequential.Inferno)

            # fig = px.parallel_coordinates(df, color="species_id", labels={"species_id": "Species",
            #                   "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
            #                   "petal_width": "Petal Width", "petal_length": "Petal Length", },
            #                     color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)


#st.spinner()
#with st.spinner(text='CONNECTING'):
#    time.sleep(5)
#    st.success('LIVE')

#streamlit. slider ( label , min_value=None , max_value=None , value=None , step=None , format=None , key=None )
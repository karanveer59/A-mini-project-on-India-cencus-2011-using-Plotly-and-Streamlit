print("Jai Hanuman")

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide',page_title='India Cencus 2011')
final_df = pd.read_csv('C:/Users/DELL/AppData/Local/Programs/Python/Python312/Data/Plotly/india_cencus.csv')

# final_df.rename(columns={'sex_ratio':'Sex Ratio', 'literact_rate':'Literacy Rate'})

class Main:
    def __init__(self):
        self.final_df = final_df
        self.list_of_state = ['Overall India'] + sorted(final_df['State'].unique())
        self.state_df = None

    def front_page(self):
        st.sidebar.title("India Census 2011")
        
        self.selected_state = st.sidebar.selectbox("Select a State", self.list_of_state)
        self.selected_primary = st.sidebar.selectbox("Primary Parameter", self.final_df.columns[5:])
        self.selected_secondary = st.sidebar.selectbox("Secondary Parameter", self.final_df.columns[5:])

        if "show_plot" not in st.session_state:
            st.session_state.show_plot = False

        if st.sidebar.button("Plot Graph"):
            st.session_state.show_plot = True


        if st.session_state.show_plot:
            st.text(f"Size represents: {self.selected_primary}")
            st.text(f"Color represents: {self.selected_secondary}")

            if self.selected_state == "Overall India":
                self.show_overall_analysis()
            else:
                self.show_state_analysis()

    def show_overall_analysis(self):
        fig = px.scatter_mapbox(self.final_df, lat="Latitude", lon="Longitude", hover_name="District",size=self.selected_primary, color=self.selected_secondary, zoom=3.5, color_continuous_scale="Plasma",mapbox_style="carto-positron", width=1400, height=700,title="Overall India Analysis")
        st.plotly_chart(fig, use_container_width=True)

        columns = ["District", self.selected_primary]
        if self.selected_primary != self.selected_secondary:
            columns.append(self.selected_secondary)
        st.dataframe(self.final_df[columns])
        
        options = [self.selected_primary, self.selected_secondary]#,f"Top 5 States in {self.selected_primary}", f"Top 5 States in {self.selected_secondary}"]
        selected_ana = st.selectbox("Select For Analysis", options)


        if selected_ana == self.selected_primary:
            st.plotly_chart(go.Figure([go.Bar(x=self.final_df["State"], y=self.final_df[self.selected_primary])]))
        elif selected_ana == self.selected_secondary:
            st.plotly_chart(px.bar(self.final_df, x="State", y=self.selected_secondary))

    def show_state_analysis(self):
        self.state_df = self.final_df[self.final_df["State"] == self.selected_state]

        fig = px.scatter_mapbox(self.state_df, lat="Latitude", lon="Longitude", hover_name="District",size=self.selected_primary, color=self.selected_primary, zoom=6, color_continuous_scale="Plasma",mapbox_style="carto-positron", width=1400, height=700,title=self.selected_state)
        st.plotly_chart(fig, use_container_width=True)

        columns = ["District", self.selected_primary]
        if self.selected_primary != self.selected_secondary:
            columns.append(self.selected_secondary)
        st.dataframe(self.state_df[columns])

        options = [self.selected_primary, self.selected_secondary,f"Top 5 District in {self.selected_primary}", f"Top 5 District in {self.selected_secondary}"]
        selected_ana = st.selectbox("Select For Analysis", options)

        # Always run analysis logic (no button required)
        if selected_ana == self.selected_primary:
            st.plotly_chart(go.Figure([go.Bar(x=self.state_df["District"], y=self.state_df[self.selected_primary])]))
        elif selected_ana == self.selected_secondary:
            st.plotly_chart(px.bar(self.state_df, x="District", y=self.selected_secondary))
        elif selected_ana == f"Top 5 District in {self.selected_primary}":
            top_df = self.state_df.sort_values(by=self.selected_primary, ascending=False).head(5)
            st.bar_chart(top_df.set_index("District")[self.selected_primary])
        elif selected_ana == f"Top 5 District in {self.selected_secondary}":
            top_df = self.state_df.sort_values(by=self.selected_secondary, ascending=False).head(5)
            st.bar_chart(top_df.set_index("District")[self.selected_secondary])

site = Main()
site.front_page()
"""
Name: Mohammad Hussnain
Class: CS230 Section 5
Assignment: Final Project
DataSet: Boston Building Violations
URL:

Description: This program will build charts and maps based on user selected cities.
When they first open up the project on streamlit, it will give them the option to choose cities.
It will then generate a map with only violations in those cities. It will also display a pie chart
that gives a percentage of total violations. It will then also display a bar chart that counts the status
of violations in those cities. Lastly, it will ask the user to set a minimum number of violations with a slider
and then display a bar chart with that criteria.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk


#This was an inital function I used that would read the data from the csv file,and have it start with
#the case no. This way I could see what was being read

def set_data():
    return pd.read_csv("boston_building_violations.csv").set_index("case_no")


#This was a crucial function I needed in order to filter the data the user picks. Since the data
#I used was for violation cities, I filtered it by that to make sure the user had correct data.

def filter_data(city_choice):
    data = set_data()
    data = data.loc[data['violation_city'].isin(city_choice)]

    return data


#This was the function I used to develop my pie chart. For the pie chart, I wanted to get a
#percentage of which cities had the highest number of violations. This function incorporates the
#previous filter data function, to make sure only the cities selected have data. I edited all the labels
#and the look of the chart from this function. In order to create the chart, I used matplotlib.
#It allowed me to edit things like the title, labels and how I displayed the chart

def pie_chart(sel_cities):
    pie_data = filter_data(sel_cities)
    city_lst = [pie_data.loc[pie_data['violation_city'].isin([violation_city])].shape[0] for violation_city in sel_cities]

    plt.figure()
    plt.pie(city_lst,labels=sel_cities, autopct="%.2f")
    plt.title(f"Percent of all building violations per city: {', '.join(sel_cities)}")
    return plt


#This was my first bar chart function. I continued using matplotlib . For the bar chart,
#I wanted to be able to count how many times
#each violation happened in the set cities. However, since there was so many violation types , I needed
#to filter it using a user selection. This allowed the user to choose what the minimum number of
#violations was and then get a bar chart with this data. I edited the size of the chart using figsize.
#I played around with this for a bit until a found one that fit the page how I liked.

def bar_chart(sel_cities, user_selection):
    bar_data = filter_data(sel_cities)
    violation_counts = bar_data['description'].value_counts()

    violations_above_threshold = violation_counts[violation_counts > user_selection]

    plt.figure(figsize=(11, 7))
    violations_above_threshold.plot(kind='bar', color= 'red')
    plt.title(f'Number of Total Violation Types where:  (Total > {user_selection})')
    plt.xlabel('Violation Desciption')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt


#This was my second bar chart. It had a very similair layout as my first but had a different purpose.
#For this bar chart, I wanted to see how many of the violations in the selected cities from the user
#where either open or closed. Not mentioned in the previous one, but I changed the color of the bars
#using color and I set it equal to whatever I wanted. I could have done rgb as well, but since I wanted
#the bar chart to be vibrant, I went with a standard color.

def bar_chart_2(sel_cities):
    bar_data = filter_data(sel_cities)
    violation_counts = bar_data['status'].value_counts()

    plt.figure(figsize=(11, 7))
    violation_counts.plot(kind='bar', color='blue')
    plt.title('Count of Violation Status in chosen Cities')
    plt.xlabel('Violation Status')
    plt.ylabel('Number')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt


#This function creates a map based on the user selection. It gets the selected cities, and generates a
#map. I changed the color in this function using rgb. I tried using standard color, but for some reason,
#it didn't show on the map properly and gave this rainbow effect. So I found the rgb code for sky blue
#and just used that. The tool tip allows that when the user hovers over the the dots on the map, they can
#see the violation ID number of the violation. I also made the map in this function rather than waiting
#for the main function.

def create_map(mapdata):
    map_df = mapdata.filter(['sam_id', 'latitude', 'longitude'])
    view_state = pdk.ViewState(latitude=map_df["latitude"].mean(), longitude=map_df["longitude"].mean(), zoom=11)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[longitude, latitude]', get_radius=70, get_color= [135,206,235], pickable=True, auto_highlight=True)
    tool_tip = {'html': 'Building Violation ID Number:<br/> <b>{sam_id}</b>', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer], tooltip=tool_tip)

    st.pydeck_chart(map)


#This function allows the user to see all the cities as options on the dropdown menu.
#Whatever the user selects gets added to the list. It will also add back the city if the user
#decides to remove it

def display_options():
    user_data = set_data()
    cities = []
    for ind, row in user_data.iterrows():
        if row['violation_city'] not in cities:
            cities.append(row['violation_city'])

    return cities


#This is my main function. I made most of the app on this function. I used some streamlit tools
#as well on this. The .title method allowed me to set the title of the app. I was also able to add my name
#I then used sidebar.write to give a title for the drop down menu. I then used my previous function display
#options() to give the user all the cities. I then used sidebar.slider to set a slider for the user.
#This was needed so the user could choose the data for the bar chart. I edited the numbers a couple of times
#but found these numbers below worked best for the data set. Min and max gave the ends of the slider
#and step was how much it increased by as you slid down. The value I set to 0 to it starts at the very
#start of the slider. I then added an if function, that just runs all my charts and maps as long as the user selects
#a city intially.

def main():
    st.title("Boston Building Violations")
    st.write("Mohammad Hussnain")
    st.sidebar.write("Choose which cities you want data for")

    main_cities = st.sidebar.multiselect("Choose City: ", display_options())
    user_count_pref = st.sidebar.slider('Choose the minimum number of violation type for Bar Chart Data: ', min_value=0, max_value=5000, step=150, value=0)
    map_data = filter_data(main_cities)

    if len(main_cities) > 0:
        create_map(map_data)

        st.pyplot(pie_chart(main_cities))
        st.pyplot(bar_chart_2(main_cities))
        st.pyplot(bar_chart(main_cities, user_count_pref))



main()
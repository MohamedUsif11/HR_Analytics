import streamlit as st

# Create navigation in the sidebar
selected_page = st.sidebar.radio("Navigate", ["Introduction", "Categorical Features Distribution","Numerical Features Distribution" ,"Findings & Observations"])
#import the requried libraries
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Read the CSV file
csv_file_path = r'Uncleaned_employees_final_dataset (1).csv'
df = pd.read_csv(csv_file_path)

image_path = os.path.join(os.path.dirname(__file__), 'Employee_data.PNG')
st.image(image_path)
# Replace values in the 'gender' column
df['gender'] = df['gender'].replace(['m', 'f'], ['Male', 'Female'])

if selected_page == 'Introduction':


    st.title(':blue[EDA] for _Employee Data_')
    st.write('Data source: [Kaggle](https://www.kaggle.com/datasets/sanjanchaudhari/employees-performance-for-hr-analytics)', unsafe_allow_html=False)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Get the columns and data dimensions

    with col1:
        columns_of_data = df.columns
        num_columns = len(columns_of_data)
        num_rows = len(df)
        st.write("Columns in the data:", columns_of_data)
        st.write()


    # Display information about the columns and data dimensions
    with col2:
        
        st.write("Number of columns in the data:", num_columns)
        st.write("Number of rows in the data:", num_rows)
 
        # Streamlit app
        st.write('Data Types Information')

        # Display the data types of each column
        data_types = df.dtypes
        st.write(data_types)
        
    st.header('Data Description')
    Data_Describe = df.describe().T
    st.write('**Data Description Numerical**', Data_Describe)
 
    Data_Describe_Cat = df.describe(include='object').T
    st.write('**Data Description Categorical**', Data_Describe_Cat)

    # Display a sample of the data

    sample_size = 10
    sample_df = df.head(sample_size)
    st.header("Sample of the data:")
    st.write(sample_df)

    # Calculate the percentage of missing values for each column
    missing_percentage = (df.isnull().mean() * 100).round(2)

    # Display missing percentage using Streamlit
    st.header("Percentage of Missing Data for Each Feature:")
    missing_percentage_table = pd.DataFrame({'Column': missing_percentage.index, 'Missing Percentage': missing_percentage.values})
    missing_percentage_table['Missing Percentage'] = missing_percentage_table['Missing Percentage'].astype(str) + '%'
    st.table(missing_percentage_table)

    # Streamlit app
    st.header("Review and Remove Duplicate Rows")

    # Display the number of duplicate rows
    duplicate_count = df.duplicated().sum()
    st.write("Number of Duplicate Rows:", duplicate_count)

    # Display the duplicate rows
    duplicate_rows = df[df.duplicated()]
    st.write("Duplicate Rows:")
    st.dataframe(duplicate_rows)

    # Remove the duplicate rows
    df.drop_duplicates(inplace=True)
    st.write("New DataFrame Shape, after removing duplicate rows:", df.shape)

    # Streamlit app
    st.header("Feature Engineering for 'gender' Column")

    # Replace values in the 'gender' column
    df['gender'] = df['gender'].replace(['m', 'f'], ['Male', 'Female'])

    # Display the value counts of the 'gender' column
    gender_value_counts = df['gender'].value_counts().reset_index()
    gender_value_counts.columns = ['Gender', 'Count']
    st.write("Value Counts of 'gender' Column:")
    st.dataframe(gender_value_counts)
elif selected_page == 'Categorical Features Distribution':    
    # Streamlit app
    st.header("Categorical Features Distribution")

    # Get categorical features
    categorical_features = df.select_dtypes(include=['object']).columns

    # Loop to create histograms for categorical features
    for feature in categorical_features:
    
        graph = px.histogram(df, x=feature, title=f"{feature} Distribution", color='gender')
        st.plotly_chart(graph)

    observation_notes_Categorical = """
    ## Observations for Categorical Features Distribution


    #### **Department Distribution:**
    - The department distribution reveals the distribution of employees across different departments.
    - It's noticeable that some departments have significantly more employees than others, which could indicate variations in team sizes.

    #### **Education Distribution:**
    - The education distribution displays the levels of education attained by employees.

    #### **Region Distribution:**
    - The region distribution provides insights into the geographical distribution of employees.
    - Concentrations of employees in specific regions like "region 2" & "region 22".

    #### **Gender Distribution:**
    - The gender distribution highlights the representation of male and female employees.

    #### **Recruitment Channel Distribution:**
    - The distribution of recruitment channels used to hire employees.

    ##### *These observations provide initial insights into the data distribution and potential areas for further investigation. It's important to dig deeper into these trends to gain a comprehensive understanding of the underlying factors influencing these patterns.*

    """
       # Display the observation notes using markdown
    st.markdown(observation_notes_Categorical)

elif selected_page == 'Numerical Features Distribution':

    # Streamlit app
    st.header("Numerical Features Box Plots")

    # Get numerical features
    numerical_features = df.select_dtypes(include=['int64', 'float64']).columns

    # Loop to create box plots for numerical features
    for feature in numerical_features:
        if feature != 'employee_id':
            graph = px.box(df, x='department', y=feature, title=f"{feature} Distribution by Department")
            st.plotly_chart(graph)
        
    # Streamlit app
    st.header("Observation Notes")

    # Observation notes as markdown
    observation_notes = """
    #### **Age Distribution:**
    - The age distribution shows outliers above the age of 54. Further investigation is needed to understand the reasons behind this outlier group. 
    - It could be related to retirement patterns, and we should analyze the distribution for each department.

    #### **No. of Training Distribution:**
    - The distribution of the number of training occurrences requires deeper analysis. 
    - The variation in training occurrences might indicate specific patterns related to different departments or job roles.

    #### **Rating Distribution:**
    - The distribution of ratings from the previous year falls predominantly between 3 and 4. 
    - This suggests that most employees received moderate to high ratings in the previous year's performance assessment.

    #### **Length of Service:**
    - The distribution of length of service reveals outliers for employees with over 13 years of service. 
    - We should examine the rate of occurrence for each department and region to determine if there are any specific patterns associated with long-serving employees.

     ##### *These observations provide initial insights into the data distribution and potential areas for further investigation. It's important to dig deeper into these trends to gain a comprehensive understanding of the underlying factors influencing these patterns.*


    """
    # Display the observation notes using markdown
    st.markdown(observation_notes)
elif selected_page == 'Findings & Observations':

    # Streamlit app
    st.title("Exploring No. of Training and Employee")
    df['employee_id'] = df['employee_id'].astype(str)

    # Total number of trainings in the organization
    total_trainings = df['no_of_trainings'].sum()
    st.write("Total number of trainings in the organization:", total_trainings)

    # Bar chart for number of trainings per department
    chart_no_of_trainings = df.groupby('department')['no_of_trainings'].sum().reset_index(name='no_of_trainings').sort_values(by='no_of_trainings', ascending=False)
    st.write("## Number of Trainings per Department")
    Bar_chart_no_of_trainings = px.bar(chart_no_of_trainings, x='department', y='no_of_trainings', color='department', title="Number of Trainings Per Department")
    st.plotly_chart(Bar_chart_no_of_trainings)
    
    # Create two columns for layout
    T1, T2 = st.columns(2)
    with T1:

        # Observations on number of trainings
        st.write("#### *Observations on Number of Trainings*")

            # Distribution_of_trainings__ = st.checkbox("Distribution of Trainings")
        Distribution_of_Trainings = df['no_of_trainings'].value_counts()
        st.write(Distribution_of_Trainings)
        with T2:
        # Average training per employee
            mean_of_trainings = df.groupby('length_of_service')['no_of_trainings'].mean()
            st.write("#### *Average Training per Employee based on the length in service (YOS)*")
            st.write(mean_of_trainings)

 


    # Investigate the number of trainings for almost 10 employees with the maximum training occurrence.
    high_trainings_count = (df['no_of_trainings'] > 6).sum()
    st.write(f"The number of employees with more than 6 trainings: {high_trainings_count}")

    # Pattern of employees with high trainings
    st.write("#### *Employees with High Trainings and Department Pattern*")
    # Check the employee data to show the pattern
    high_trainings_employees = df[df['no_of_trainings'] > 6].sort_values(by='no_of_trainings', ascending=False)
    st.write(high_trainings_employees)

    # Observation notes as markdown
    Training_Observations_notes = """

    #### Summary of Observations on Training and Employee Data Exploration

       - It's imperative to delve into the training frequencies of approximately 10 employees who have exhibited the highest training engagement. 
       - Notably, these employees are primarily situated in the **Procurement** & **Sales & Marketing Department** within **regions 2 & 22**. 
       - Their training occurrences typically range from 7 to 9 sessions. Remarkably, when considering employees with less than 4 years of service (YOS), 
       - The average training per employee across the organization stands at approximately 1 training. 
       - This information underlines the distinctive training dynamics within these specific contexts.
       """
    
    #Extra_Notes_not_viewed 
    
    #### **Average Training per Employee based on YOS:**
    #- The average number of trainings per employee was calculated based on the length of service (Years of Service, YOS). This insight helps identify whether training patterns change over an employee's tenure.

    #### **Employees with High Trainings:**
    #- Employees with more than 6 training occurrences were identified and the count was displayed. This allows for the identification of a subset of employees who undergo frequent training.

    #### **Pattern of Employees with High Trainings:**
    #- A table was presented that showcases employees with high training occurrences (more than 6 trainings). The data was sorted to highlight the employees with the most frequent training experiences.
    
    st.write(Training_Observations_notes)



    # Streamlit app
    st.title("Exploring Age Distribution and Employee Analysis")

    # Draw a histogram to check the distribution of age
    Age_Diagram = px.histogram(df, 'age')
    st.plotly_chart(Age_Diagram)

    st.title("Employee Age Analysis")

    # Filter out employees above 54 years old
    filtered_data_above_54_age = df[df['age'] >= 54]
    # Number of employees above 54 years old
    num_employees_above_54 = len(filtered_data_above_54_age)
    st.write("Number of employees above 54 years old:", num_employees_above_54)

    # Calculate the percentage of employees above 54 years old
    percentage_above_54 = round((num_employees_above_54 / len(df)) * 100)
    st.write("% of employees above 54 years old:", f"{percentage_above_54}%")




    # Calculate the average age across the organization
    average_age = df['age'].mean()
    st.write("Average age across the organization:", average_age)

    A1, A2 = st.columns(2)

    with A1:
        # Calculate the min, average, and max age for each department
        Min_Mean_Max_age_per_Department = df.groupby('department')['age'].agg(['min', 'mean', 'max'])
        st.write("Min, Mean, and Max Age per Department:")
        st.write(Min_Mean_Max_age_per_Department)

    with A2:
        
        # Calculate the min, average, and max age for each department
        Min_Mean_Max_age_per_Department = df.groupby('department')['age'].agg(['min', 'mean', 'max']).reset_index()

        # Create a box plot using Plotly Express
        box_plot = px.box(
            Min_Mean_Max_age_per_Department,
            x='department',
            y=['min', 'mean', 'max'],
            labels={'variable': 'Age Statistic'},
            title="Age range by Department"
        )

        # Display the box plot
        st.plotly_chart(box_plot)

    C1, C2 = st.columns(2)

    with C1:
        
        # Count the number of employees above 59 years old for each department
        Employee_Above_59 = df[df['age'] > 59]
        Employee_Above_59_Count = Employee_Above_59.groupby(['department'])['age'].count().sort_values(ascending=False)
        st.write("Number of Employees Above 59 Years Old per Department:")
        st.write(Employee_Above_59_Count)

    with C2:

        # Calculate the percentage of high tenure employees per department
        filtered_length_of_service_per_department_above_95 = df[df['length_of_service'] > df['length_of_service'].quantile(0.95)]
        percentage_of_high_tenure_employees_per_department = round(filtered_length_of_service_per_department_above_95['department'].value_counts() / df['department'].value_counts() * 100).sort_values(ascending=False)

        st.write("Percentage of high tenure employees per department:")
        st.write(percentage_of_high_tenure_employees_per_department)
    
    Age_Observations_notes = """
    #### *Age Observation Notes*:
    - After carefully looking into the data, we noticed something interesting. 
    - Around 785 employees, which is about 4% of the total workforce, have been with the company for a long time. 
    - Among them, the highest percentage comes from the Technology department with 5%, followed by Procurement with 4.8%, HR with 4%, and Sales & Marketing with 3.9%.
    -  This sheds light on how long employees stay in different departments and highlights departments where people tend to stay longer.
       """
    st.write(Age_Observations_notes)

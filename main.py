
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Function to plot pie chart
def plot_pie_chart(data, column):
    # Aggregate data
    data_count = data[column].value_counts()
    
    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(data_count, labels=data_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)

# Function to plot line chart
def plot_line_chart(data, x_col, y_col):
    fig, ax = plt.subplots()
    ax.plot(data[x_col], data[y_col], marker='o')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f'Line Chart of {y_col} vs {x_col}')

    st.pyplot(fig)

# Function to plot histogram
def plot_histogram(data, column):
    fig, ax = plt.subplots()
    ax.hist(data[column], bins=30, edgecolor='k')
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Histogram of {column}')

    st.pyplot(fig)

# Function to plot scatter plot
def plot_scatter_plot(data, x_col, y_col):
    fig, ax = plt.subplots()
    ax.scatter(data[x_col], data[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f'Scatter Plot of {y_col} vs {x_col}')

    st.pyplot(fig)

# Function to plot bar chart
def plot_bar_chart(data, column):
    # Aggregate data
    data_count = data[column].value_counts()
    
    # Plot bar chart
    fig, ax = plt.subplots()
    ax.bar(data_count.index, data_count)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Bar Chart of {column}')

    st.pyplot(fig)

# Function to plot heatmap
def plot_heatmap(data):
    # Compute the correlation matrix
    corr = data.corr()

    # Plot heatmap
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Heatmap of Correlations')

    st.pyplot(fig)

st.title("Enhanced Data Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Select an option", ["Home", "Data", "Upload Notebook", "Settings"])

if option == "Home":
    st.write("Welcome to the enhanced data dashboard!")

elif option == "Data":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Display data and summary
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Data Preview")
            st.write(df.head())

        with col2:
            st.subheader("Data Summary")
            st.write(df.describe())

        # Filter data
        st.subheader("Filter Data")
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter by", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)

        # Plot data
        st.subheader("Plot Data")
        plot_type = st.selectbox("Select plot type", ["Line Chart", "Pie Chart", "Histogram", "Scatter Plot", "Bar Chart", "Heatmap"])

        if plot_type == "Line Chart":
            x_column = st.selectbox("Select x-axis column", columns)
            y_column = st.selectbox("Select y-axis column", columns)
            if st.button("Generate Line Chart"):
                plot_line_chart(filtered_df, x_column, y_column)
        
        elif plot_type == "Pie Chart":
            pie_column = st.selectbox("Select column for Pie Chart", columns)
            if st.button("Generate Pie Chart"):
                plot_pie_chart(filtered_df, pie_column)

        elif plot_type == "Histogram":
            hist_column = st.selectbox("Select column for Histogram", columns)
            if st.button("Generate Histogram"):
                plot_histogram(filtered_df, hist_column)

        elif plot_type == "Scatter Plot":
            x_column = st.selectbox("Select x-axis column for Scatter Plot", columns)
            y_column = st.selectbox("Select y-axis column for Scatter Plot", columns)
            if st.button("Generate Scatter Plot"):
                plot_scatter_plot(filtered_df, x_column, y_column)

        elif plot_type == "Bar Chart":
            bar_column = st.selectbox("Select column for Bar Chart", columns)
            if st.button("Generate Bar Chart"):
                plot_bar_chart(filtered_df, bar_column)

        elif plot_type == "Heatmap":
            if st.button("Generate Heatmap"):
                plot_heatmap(filtered_df)
    
elif option == "Upload Notebook":
    uploaded_notebook = st.file_uploader("Choose a Jupyter Notebook file", type="ipynb")

    if uploaded_notebook is not None:
        notebook_content = uploaded_notebook.read()
        nb = nbformat.reads(notebook_content, as_version=4)

        # Extract code cells from notebook
        code_cells = [cell['source'] for cell in nb.cells if cell.cell_type == 'code']
        code_content = "\n".join(code_cells)

        st.subheader("Notebook Code")
        st.code(code_content, language='python')

        # Optionally, execute code or extract data
        try:
            from nbconvert import PythonExporter
            python_exporter = PythonExporter()
            python_code, _ = python_exporter.from_notebook_node(nb)

            exec(python_code, globals())  # Be cautious with exec() and user code
            
            st.subheader("Executed Code Output")
            st.write("Code executed successfully.")
        except Exception as e:
            st.error(f"An error occurred while executing the code: {e}")

elif option == "Settings":
    st.write("Settings options will be available here.")
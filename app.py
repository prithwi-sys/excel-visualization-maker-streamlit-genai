import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Excel Data Visualizer", layout="wide")

st.title("Excel Data Visualizer")
st.markdown("Upload an Excel file to explore and visualize your data")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully!")
        
        with st.expander("View Raw Data"):
            st.dataframe(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Summary")
            st.write(f"**Rows:** {df.shape[0]}")
            st.write(f"**Columns:** {df.shape[1]}")
            st.write("**Column Types:**")
            st.write(df.dtypes)
        
        with col2:
            st.subheader("Missing Values")
            st.write(df.isnull().sum())
        
        st.divider()
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if numeric_cols:
            st.subheader("Visualizations")
            
            viz_type = st.selectbox("Select Visualization Type", 
                ["Histogram", "Scatter Plot", "Box Plot", "Line Chart", "Bar Chart", "Pie Chart"])
            
            if viz_type == "Histogram":
                col_to_plot = st.selectbox("Select Column", numeric_cols)
                bins = st.slider("Number of Bins", 5, 50, 20)
                fig = px.histogram(df, x=col_to_plot, nbins=bins, title=f"Distribution of {col_to_plot}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Scatter Plot":
                if len(numeric_cols) >= 2:
                    x_col = st.selectbox("X Axis", numeric_cols, index=0)
                    y_col = st.selectbox("Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                    color_col = st.selectbox("Color (optional)", [None] + categorical_cols)
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Need at least 2 numeric columns for scatter plot")
                    
            elif viz_type == "Box Plot":
                col_to_plot = st.selectbox("Select Column", numeric_cols)
                color_col = st.selectbox("Group By (optional)", [None] + categorical_cols)
                fig = px.box(df, y=col_to_plot, color=color_col, title=f"Box Plot of {col_to_plot}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Line Chart":
                if categorical_cols:
                    x_col = st.selectbox("X Axis", categorical_cols)
                else:
                    x_col = st.selectbox("X Axis", df.columns)
                y_col = st.selectbox("Y Axis", numeric_cols)
                fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {y_col} over {x_col}")
                st.plotly_chart(fig, use_container_width=True)
                
            elif viz_type == "Bar Chart":
                if categorical_cols:
                    x_col = st.selectbox("Select Category", categorical_cols)
                    agg_func = st.selectbox("Aggregation", ["sum", "mean", "count", "min", "max"])
                    if agg_func == "sum":
                        aggregated = df.groupby(x_col)[numeric_cols].sum().reset_index()
                    elif agg_func == "mean":
                        aggregated = df.groupby(x_col)[numeric_cols].mean().reset_index()
                    elif agg_func == "count":
                        aggregated = df.groupby(x_col).size().reset_index(name='count')
                    elif agg_func == "min":
                        aggregated = df.groupby(x_col)[numeric_cols].min().reset_index()
                    else:
                        aggregated = df.groupby(x_col)[numeric_cols].max().reset_index()
                    
                    y_col = st.selectbox("Select Value Column", aggregated.select_dtypes(include=['number']).columns)
                    fig = px.bar(aggregated, x=x_col, y=y_col, title=f"Bar Chart: {y_col} by {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Need at least one categorical column for bar chart")
                    
            elif viz_type == "Pie Chart":
                if categorical_cols:
                    name_col = st.selectbox("Select Category", categorical_cols)
                    value_col = st.selectbox("Select Value", numeric_cols)
                    fig = px.pie(df, names=name_col, values=value_col, title=f"Pie Chart: {value_col} by {name_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Need at least one categorical column for pie chart")
        
        if categorical_cols:
            st.subheader("Category Distribution")
            cat_col = st.selectbox("Select Column to View Distribution", categorical_cols)
            value_counts = df[cat_col].value_counts().reset_index()
            value_counts.columns = [cat_col, 'Count']
            fig = px.bar(value_counts, x=cat_col, y='Count', title=f"Distribution of {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload an Excel file to get started")

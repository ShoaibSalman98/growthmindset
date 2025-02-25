import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper",layout="centered")

st.title("Data Sweeper generate by Shaoib Salman")
st.write("This tool helps you quickly and easily clean and organize your data.")

# custome CSS.

st.markdown(
    """
    <style>
    .stapp {
        font-size: 14px;
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
        margin-bottom: 20px;
        background-color: black;
        colour: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tittle and Description,



# File uploader.
uploaded_files = st.file_uploader ("Upload your file here", type=["xlsx","csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df= pd.read_excel(file)
        else:
            st.error(f"File format not supported. Please upload a CSV or Excel file: {file_ext}") 
            continue

        # Displye information about the File.
        st.write(f"** File Name ** {file.name}")
        st.write(f"** File Size ** {file.size/1024}")
        
        # Show 5 Rows of our Data Frame
        st.write("Preview the Head of Data")
        st.dataframe(df.head())

        # Data cleaning options.
        st.subheader("Data Cleaning")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 =st.columns(2)

            with col1:
                # Drop rows with missing values.
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully.")
                    
                with col2:
                        if st.button(f"fill missing value for : {file.name}"):
                            numeric_cols= df.select_dtypes(include=["number"]).columns
                            df[numeric_cols] =df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("Missing values filled successfully.")
                            
                    # Choose specefic columns to keep or convert

    st.subheader('Select Columns to Show')
    columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
    df= df[columns]

                    # Data Visulization.
    st.subheader("Data Visualization")
    if st.checkbox(f"show Visulization for {file.name}"):
                        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


                        # Conversion Options.
                        st.subheader("Conversion Options")
                        conversion_type=st.radio(f"Convert {file.name} to:", ["CSV","Excel"], key=file.name)
                        if st.button(f"Convert{file.name}"):
                            buffer= BytesIO()
                            if conversion_type == "CSV":
                                 df.to_csv(buffer,index=False)
                                 file_name = file.name.replace(file_ext,".csv")
                                 mime_type= "text/csv" 
                            elif conversion_type == 'Excel':
                                df.to_excel(buffer, index=False)
                                file_name = file.name.replace(file_ext,".xlsx")
                                mime_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                buffer.seek(0)
                                
                                # Download Button
                                st.download_button(
                                    label=f"Download {file.name} as {conversion_type}",
                                    date=buffer,
                                    filename=file_name,
                                    mime=mime_type
    
                                )
                                st.success("Your File Processed Succesfully")

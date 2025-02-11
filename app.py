import streamlit as st
import pymongo
import pandas as pd

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://alexisniyonkuru1984:27QTKU1WksDOkpCe@cluster0.9wl5s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['job_data']  # Database name
collection = db['job_listings']  # Collection name

# Function to add data to MongoDB
def add_data(id, user, job_title, company, jd_url, status):
    document = {
        "user": user,
        "job_title": job_title,
        "company": company,
        "jd_url": jd_url,
        "status": status
    }
    collection.insert_one(document)

# Function to fetch all data
def fetch_data():
    data = collection.find()
    df = pd.DataFrame(list(data))
    return df

# Function to search data by user
def search_data(query):
    data = collection.find({"user": {"$regex": query, "$options": "i"}})
    df = pd.DataFrame(list(data))
    return df

# Streamlit UI
st.title("Job Data Streamlit App")

# Add Data Section
st.header("Add Job Listing")
user = st.text_input("User")
job_title = st.text_input("Job Title")
company = st.text_input("Company")
jd_url = st.text_input("JD URL")
status = st.selectbox("Status", ["Applied", "Interview", "Offered", "Rejected"])

if st.button("Add Data"):
    if id and user and job_title and company and jd_url and status:
        add_data(id, user, job_title, company, jd_url, status)
        st.success("Data added successfully!")
    else:
        st.error("Please fill all fields")

# View All Data Section
st.header("View All Job Listings")
df = fetch_data()
if not df.empty:
    st.dataframe(df[['user', 'job_title', 'company', 'jd_url', 'status']])
else:
    st.write("No data available.")

# Search Section
st.header("Search Job Listings by User")
search_query = st.text_input("Search by User")
if search_query:
    search_results = search_data(search_query)
    if not search_results.empty:
        st.dataframe(search_results[['user', 'job_title', 'company', 'jd_url', 'status']])
    else:
        st.write("No results found.")

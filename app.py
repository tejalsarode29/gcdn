import streamlit as st
import boto3
import os
from botocore.exceptions import NoCredentialsError

st.set_page_config(layout="wide")

# Streamlit UI for AWS Credentials and S3 Bucket Name
st.title("📂 Upload File to AWS S3")
aws_access_key = st.text_input("Enter AWS Access Key", value="AKIA6K5V7XWWJZYMB5NN")
aws_secret_key = st.text_input("Enter AWS Secret Key", type="password", value="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")
s3_bucket_name = "upload-vault-2810"

# Initialize S3 client
if aws_access_key and aws_secret_key and s3_bucket_name:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    def upload_to_s3(file, bucket_name, file_name):
        try:
            s3.upload_fileobj(file, bucket_name, file_name)
            return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        except NoCredentialsError:
            return "AWS credentials not available."

    # Streamlit UI for file upload
    uploaded_file = st.file_uploader("Choose a file to upload", type=["png", "jpg", "pdf", "txt", "csv"])

    if uploaded_file:
        file_name = uploaded_file.name
        st.write(f"Uploading `{file_name}` to S3...")

        s3_url = upload_to_s3(uploaded_file, s3_bucket_name, file_name)
        
        if "https://" in s3_url:
            st.success("✅ File uploaded successfully!")
            st.write(f"📎 File URL: [{s3_url}]({s3_url})")
        else:
            st.error("❌ Upload failed. Check AWS credentials and permissions.")
else:
    st.warning("Please enter AWS credentials and S3 bucket name.")

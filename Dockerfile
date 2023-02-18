FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the ODBC library
RUN apt-get update && \
    apt-get install -y gnupg2 curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg && \
    install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/ && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/debian/10/prod buster main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN echo 'TLSv1.2' >> /etc/ssl/openssl.cnf

# Copy the requirements file
COPY requirements.txt .

# Install the requirements
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Expose the port on which the Streamlit app will run
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "main.py"]
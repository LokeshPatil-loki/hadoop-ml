FROM python:3.9

# Install dependencies and Java (required for Spark)
RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository "deb http://security.debian.org/debian-security buster/updates main" && \
  add-apt-repository "deb http://deb.debian.org/debian unstable main non-free contrib" && \
  apt-get update && \
  apt-get install -y openjdk-11-jdk curl && \
  apt-get clean

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Download and install Apache Spark
RUN curl -L https://archive.apache.org/dist/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz | tar xz -C /opt/

# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark-3.4.0-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]

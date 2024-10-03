# Hadoop Diabetes Prediction

A distributed machine learning system for diabetes prediction using Hadoop, Spark, and Flask. This project implements a scalable architecture for training a diabetes prediction model on HDFS and serving predictions through a web interface.

## System Architecture

The system consists of several containerized components:
- Hadoop cluster (HDFS + YARN)
- Spark cluster (Master + Worker)
- Flask prediction server

## Prerequisites

- Vagrant
- VirtualBox
- Docker and Docker Compose
- Git

## Setup Instructions
### Clone Repository
```bash
git clone https://github.com/LokeshPatil-loki/hadoop-ml.git
```

### 2. Virtual Machine Setup

```bash

# Initialize Vagrant
vagrant init

# Start the VM
vagrant up

# SSH into the VM
vagrant ssh

# Navigate to the shared directory
cd /vagrant/hadoop-docker
```

### 3. Start the containers:
```bash
docker-compose up -d
```

### 4. Dataset Preparation
1. Upload the dataset to HDFS:
```bash
# Access NameNode container
docker exec -it namenode /bin/bash

# Create HDFS directory
hdfs dfs -mkdir -p /input/diabetes

# Upload dataset
hdfs dfs -put diabetes.csv /input/diabetes/
```

### 5. Model Training

1. Install Python dependencies in Spark containers:
```bash
# For Spark Master
docker exec -it spark-master /bin/sh
pip install pyspark numpy pandas

# For Spark Worker
docker exec -it spark-worker /bin/sh
pip install pyspark numpy pandas
```

2. Copy and run the training script:
```bash
cp diabetes_spark_mllib.py spark-master:/opt/spark/work-dir/
docker exec -it spark-master /bin/sh
# Run training script inside container
```

### 5. Prediction Server

1. Build and start the Flask application:
```bash
docker-compose up flask-app
```

2. Access the web interface at `http://localhost:5000`

## Project Structure

```
hadoop-docker/
├── docker-compose.yml
├── hadoop.env
├── flask_server/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── templates/
│       └── index.html
└── diabetes_spark_mllib.py
```

## API Endpoints

### Prediction Endpoint
- **URL:** `/predict`
- **Method:** POST
- **Request Body:**
```json
{
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
}
```
- **Response:**
```json
{
    "features": [...],
    "prediction": 1
}
```

## Web Interface

The project includes a user-friendly web interface for making predictions. Access it at `http://localhost:5000` after starting the Flask application.

## Container Management

### Start all services
```bash
docker-compose up -d
```

### Stop all services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

## Monitoring

- Hadoop NameNode UI: `http://localhost:9870`
- Spark Master UI: `http://localhost:8080`

## Troubleshooting

1. If containers fail to start, check logs:
```bash
docker-compose logs [service-name]
```

2. To restart a specific service:
```bash
docker-compose restart [service-name]
```

3. If HDFS is unavailable, ensure the NameNode is healthy:
```bash
docker exec -it namenode hdfs dfsadmin -report
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

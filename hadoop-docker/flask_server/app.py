from flask import Flask, request, jsonify, render_template
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import VectorAssembler

app = Flask(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DiabetesPredictionAPI") \
    .getOrCreate()

# Load the trained model from HDFS
model = LogisticRegressionModel.load("hdfs://namenode:9000/models/logistic_regression_model")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the 
    data = request.json

    input_data = spark.createDataFrame([data])

    # Prepare features using the same feature vectorization process
    assembler = VectorAssembler(
        inputCols=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
        outputCol="features"
    )
    input_data = assembler.transform(input_data)

    predictions = model.transform(input_data)
    result = predictions.select("features", "prediction").first()

    # Convert DenseVector to a list for JSON serialization
    features_list = result.features.toArray().tolist()

    return jsonify({"features": features_list, "prediction": int(result.prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

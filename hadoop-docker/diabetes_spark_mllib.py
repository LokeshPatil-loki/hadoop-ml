from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import logging

# Set logging level to ERROR
logging.getLogger("org").setLevel(logging.ERROR)
logging.getLogger("akka").setLevel(logging.ERROR)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DiabetesPrediction") \
    .getOrCreate()

# Load dataset from HDFS
df = spark.read.csv("hdfs://namenode:9000/input/diabetes/diabetes.csv", header=True, inferSchema=True)

# Show the first few rows of the dataframe
df.show()

# Prepare features and label
assembler = VectorAssembler(
    inputCols=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
    outputCol="features"
)

data = assembler.transform(df)
data = data.withColumnRenamed("Outcome", "label")

# Split the dataset into training and testing sets
train, test = data.randomSplit([0.7, 0.3])

# Initialize and train the Logistic Regression model
lr = LogisticRegression(featuresCol="features", labelCol="label")
model = lr.fit(train)

# Make predictions on the test set
predictions = model.transform(test)
predictions.select("features", "label", "prediction").show()

# Evaluate the model
evaluator = BinaryClassificationEvaluator()
accuracy = evaluator.evaluate(predictions)
print(f"Test accuracy: {accuracy:.2f}")

# Save the trained model to HDFS
model.save("hdfs://namenode:9000/models/logistic_regression_model")

spark.stop()

import pandas as pd
import glob
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


def load_data(file_path, file_format):
	if file_format == 'csv':
		data = pd.read_csv(file_path)
	elif file_format == 'excel':
		data = pd.read_excel(file_path)
	elif file_format == 'sql':
		db_url = "mysql+pymysql://username:password@hostname/dbname"
		engine = create_engine(db_url)
		query = "SELECT * FROM table_name"
		data = pd.read_sql(query, engine)
	else:
		raise ValueError("Invalid file format!")
	return data


def merge_csv_files(input_pattern, output_file):
	file_paths = glob.glob(input_pattern)
	merged_data = pd.concat(map(pd.read_csv, file_paths))
	merged_data.to_csv(output_file, index=False)
	print("Merged CSV files successfully!")

def preprocess_data(data):
	# Handle missing values in numerical columns
	numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
	imputer = SimpleImputer(strategy='mean')
	data[numerical_cols] = imputer.fit_transform(data[numerical_cols])

	# Handle categorical columns with one-hot encoding
	categorical_cols = data.select_dtypes(include=['object']).columns
	data = pd.get_dummies(data, columns=categorical_cols)

	return data


def load_data(file_path, file_format):
	if file_format == 'csv':
		data = pd.read_csv(file_path)
	elif file_format == 'excel':
		data = pd.read_excel(file_path)
	elif file_format == 'sql':
		# I don't know how to handle it yet
		pass
	else:
		raise ValueError("Invalid file format!")
	return data

def generate_visualizations(data):
	for col in data.columns:
		plt.figure()
		if data[col].dtype in ['int64', 'float64']:
			sns.histplot(data[col])
			plt.title(f'Histogram of {col}')
			plt.show()
			plt.close()  # Close the current plot

if __name__ == '__main__':
	files = "./archive/*.csv"
	output_file = "merged.csv"
	# merge_csv_files(files, output_file)

	data = load_data("./merged.csv", "csv")

	data = preprocess_data(data)
	generate_visualizations(data)

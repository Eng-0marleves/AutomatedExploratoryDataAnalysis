import pandas as pd
import glob
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns


def merge_csv_files(input_pattern, output_file):
	file_paths = glob.glob(input_pattern)

	merged_data = pd.DataFrame()

	for file_path in file_paths:
		df = pd.read_csv(file_path)
		merged_data = pd.concat([merged_data, df])

	merged_data.to_csv(output_file, index=False)

	print("Merged CSV files successfully!")


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


def preprocess_data(data):
	# Handle missing values in numerical columns
	numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
	imputer = SimpleImputer(strategy='mean')
	data[numerical_cols] = imputer.fit_transform(data[numerical_cols])

	# Handle missing values in categorical columns
	categorical_cols = data.select_dtypes(include=['object']).columns
	imputer = SimpleImputer(strategy='constant', fill_value='Unknown')
	data[categorical_cols] = imputer.fit_transform(data[categorical_cols])

	return data

def generate_visualizations(data):
	for col in data.columns:
		plt.figure()
		if data[col].dtype in ['int64', 'float64']:
			sns.histplot(data[col])
			plt.title(f'Histogram of {col}')
		elif data[col].dtype == 'object' and col != 'data_dte':
			sns.countplot(data[col])
			plt.title(f'Countplot of {col}')
		elif data[col].dtype == 'datetime64[ns]':
			sns.lineplot(data=data, x=col, y='Total')
			plt.title(f'{col} vs Total')
			# Add more conditions and corresponding plots for different column types if needed
		plt.show()

files = "./archive/*.csv"
output_file = "merged.csv"
merge_csv_files(files, output_file)

data = load_data("./merged.csv", "csv")
print(data)

data = preprocess_data(data)
generate_visualizations(data)
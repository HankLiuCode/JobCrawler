import pandas

filepath = "../Data/jobs104_20190819_金融軟體人員_parsed.xlsx"
df = pandas.read_excel(io=filepath)
print(df.describe())
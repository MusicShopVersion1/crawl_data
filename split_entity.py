import pandas as pd
import numpy as np

df = pd.read_csv('product.csv', sep='\t', encoding='utf-8', index_col=[0], skipinitialspace=True)

df.columns = df.columns.str.replace('Thunbnail', 'Thumbnail')

# df.to_csv('product1.csv', sep='\t', encoding='utf-8')

#						                               1-n	    n-n     n-n     n-n     n-n    n-n
# Name, Price, Thumbnail, Description, Year, Quality, Category, Brand, Country, Format, Genre, Style


# Product: Name, Price, Thumbnail, Description, Year, Quality
df_Product = df[['Name', 'Price', 'Thumbnail', 'Description', 'Year', 'Quality', 'Category', 'Brand']]
# Replace "[;];'" -> null
df_Product['Category'] = df_Product['Category'].str.replace('[', '')
df_Product['Category'] = df_Product['Category'].str.replace(']', '')
df_Product['Category'] = df_Product['Category'].str.replace("'", '')

# Drop null; ''
df_Product.fillna('NULL', inplace=True)
df_Product.fillna(0, inplace=True)
df_Product.replace(to_replace='', value='NULL', inplace=True)
# Drop special character at First, Last elements
df_Product['Brand'] = df_Product['Brand'].apply(lambda x: x.strip("*&%,"))

# Save
df_Product.to_excel("product/product.xlsx", index=False, encoding='utf-8')

# df_Product = df_Product.applymap(lambda x: '"' + str(x) + '"' if isinstance(x, (int, str)) else x)
#
# df_Product.to_csv('product/product.csv', sep='\t', encoding='utf-8', index=False)


# # Category        1-n
# df_Category = df[['Name', 'Category']]
# dffinal_Category = pd.DataFrame(columns=['Name', 'Category'])
# for index, row in df_Category.iterrows():
#     list_curr_Category = row['Category'].replace('[', '').replace(']', '').replace('', '').replace("'", '').split(',')
#     # print(list_curr_Category)
#     for Category in list_curr_Category:
#         # print(row['Name'], Category)
#         dffinal_Category = dffinal_Category.append({'Name': row['Name'], 'Category': Category}, ignore_index=True)
#
# dffinal_Category.to_csv('product/category.csv', sep='\t', encoding='utf-8', index=False)
#
#
# # Brand          n-n
# df_Brand = df[['Name', 'Brand']]
# df_Brand = df_Brand.fillna('')
# df_Product_Brand = pd.DataFrame(columns=['Name', 'Brand'])
# for index, row in df_Brand.iterrows():
#     list_curr_Brand = row['Brand'].split(',')
#     for Brand in list_curr_Brand:
#         df_Product_Brand = df_Product_Brand.append({'Name': row['Name'], 'Brand': Brand}, ignore_index=True)
#
# # Product_Brand
# df_Product_Brand['Brand'] = df_Product_Brand['Brand'].str.strip()
# df_Product_Brand.to_csv('product/product_brand.csv', sep='\t', encoding='utf-8', index=False)
# # Brand
# Brand_series = df_Product_Brand['Brand'].drop_duplicates()
# Brand_series = Brand_series.replace({'': np.nan})
# Brand_series = Brand_series.dropna()
# Brand_series = Brand_series.reset_index(drop=True)
# Brand_series.to_csv('product/brand.csv', sep='\t', encoding='utf-8', index=False)

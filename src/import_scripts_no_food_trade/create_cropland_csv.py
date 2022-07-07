import pandas as pd
import numpy as np
import os

CROPLAND_CSV = '../../data/no_food_trade/FAOSTAT_cropland_2019.csv'

HA_TO_M2 = 10000

# Why are those here @Morgan? They are already in the file when it is downloaded
countries = ["AFG","ALB","DZA","AGO","ARG","ARM","AUS","AZE","BHR","BGD","BRB","BLR","BEN","BTN","BOL","BIH","BWA","BRA","BRN","BFA","MMR","BDI","CPV","KHM","CMR","CAN","CAF","TCD","CHL","CHN","COL","COD","COG","CRI","CIV","CUB","DJI","DOM","ECU","EGY","SLV","ERI","SWZ","ETH","F5707","GBR","FJI","GAB","GMB","GEO","GHA","GTM","GIN","GNB","GUY","HTI","HND","IND","IDN","IRN","IRQ","ISR","JAM","JPN","JOR","KAZ","KEN","KOR","PRK","KWT","KGZ","LAO","LBN","LSO","LBR","LBY","MDG","MWI","MYS","MLI","MRT","MUS","MEX","MDA","MNG","MAR","MOZ","NAM","NPL","NZL","NIC","NER","NGA","MKD","NOR","OMN","PAK","PAN","PNG","PRY","PER","PHL","QAT","RUS","RWA","SAU","SEN","SRB","SLE","SGP","SOM","ZAF","SSD","LKA","SDN","SUR","CHE","SYR","TWN","TJK","TZA","THA","TGO","TTO","TUN","TUR","TKM","UGA","UKR","ARE","USA","URY","UZB","VEN","VNM","YEM","ZMB","ZWE"]

country_names = ["Afghanistan","Albania","Algeria","Angola","Argentina","Armenia","Australia","Azerbaijan","Bahrain","Bangladesh","Barbados","Belarus","Benin","Bhutan","Bolivia (Plurinational State of)","Bosnia and Herzegovina","Botswana","Brazil","Brunei Darussalam","Burkina Faso","Myanmar","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic","Chad","Chile","China","Colombia","Congo","Democratic Republic of the Congo","Costa Rica","C?te d'Ivoire","Cuba","Djibouti","Dominican Republic","Ecuador","Egypt","El Salvador","Eritrea","Eswatini","Ethiopia","European Union (27) + UK","UK","Fiji","Gabon","Gambia","Georgia","Ghana","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","India","Indonesia","Iran (Islamic Republic of)","Iraq","Israel","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Democratic People's Republic of Korea","Republic of Korea","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Lebanon","Lesotho","Liberia","Libya","Madagascar","Malawi","Malaysia","Mali","Mauritania","Mauritius","Mexico","Republic of Moldova","Mongolia","Morocco","Mozambique","Namibia","Nepal","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Qatar","Russian Federation","Rwanda","Saudi Arabia","Senegal","Serbia","Sierra Leone","Singapore","Somalia","South Africa","South Sudan","Sri Lanka","Sudan","Suriname","Switzerland","Syrian Arab Republic","Taiwan","Tajikistan","United Republic of Tanzania","Thailand","Togo","Trinidad and Tobago","Tunisia","Turkiye","Turkmenistan","Uganda","Ukraine","United Arab Emirates","United States of America","Uruguay","Uzbekistan","Venezuela (Bolivarian Republic of)","Viet Nam","Yemen","Zambia","Zimbabwe"]

df_cropland = pd.read_csv(CROPLAND_CSV)[['Area Code (ISO3)',"Area", 'Value']]

#Rename columns
df_cropland.columns = ["ISO3 Country Code", "Country", "Cropland Area in 2019 (m2)"]

# Convert 1000 ha to m²
df_cropland["Cropland Area in 2019 (m2)"] = df_cropland["Cropland Area in 2019 (m2)"] * 1000 * HA_TO_M2

#add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
area_combined= df_cropland[df_cropland["ISO3 Country Code"] == "GBR"]["Cropland Area in 2019 (m2)"] + df_cropland[df_cropland["ISO3 Country Code"] == "F5707"]["Cropland Area in 2019 (m2)"]
df_cropland.loc[len(df_cropland.index)] = ['F5707+GBR', "European Union (27) + UK", area_combined] 

# and delete GBR
i = df_cropland[df_cropland["ISO3 Country Code"] == "GBR"].index
df_cropland.drop(i)


print("Cropland")
print(df_cropland.head())
df_cropland.to_csv('../../data/no_food_trade/cropland_csv.csv',sep=",")
# np.savetxt('../../data/no_food_trade/meat_csv.csv',meat_csv,delimiter=",",fmt='%s')

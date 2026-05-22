import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Initialize an empty list instead of an empty DataFrame
df_list = []

for j in range(1, 11):
   # Fix the variable name bug (webpage vs web_data)
   webpage = requests.get("https://ambitionbox.com{}".format(j), headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}).text
   soup = BeautifulSoup(webpage, "html.parser") 
   company = soup.find_all("div", class_="companyCardWrapper__primaryInformation")
   
   name = []
   rating = []
   reviews = []
   ctype = []
   hq = []

   for i in company:
      name.append(i.find("h2").text.strip())
      rating.append(i.find("div", class_="rating_text rating_text--md").text.strip())
      reviews.append(i.find("span", class_="companyCardWrapper__companyRatingCount").text.strip())
    
      meta = i.find("span", class_="companyCardWrapper__interLinking").text.strip()

      # Safe splitting logic to prevent IndexErrors
      meta_parts = meta.split("|")
      ctype.append(meta_parts[0].strip() if len(meta_parts) > 0 else "Unknown")
      
      if len(meta_parts) > 1:
         hq.append(meta_parts[1].split("+")[0].strip())
      else:
         hq.append("Unknown")

   d = {"Name": name, "Rating": rating, "Reviews": reviews, "Company_type": ctype, "HQ": hq}
   df = pd.DataFrame(d)

   # 2. Append the dataframe to your list
   df_list.append(df)

# 3. Combine all dataframes at the very end
final = pd.concat(df_list, ignore_index=True)

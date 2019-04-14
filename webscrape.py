from bs4 import BeautifulSoup
import requests 
import pandas as pd


url = "https://www.programmableweb.com/apis/directory"


api_info={}
count=0
while True:
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	table = soup.find('table',{'class':'views-table cols-4 table'})
	table_body=table.find('tbody')
	rows=table_body.find_all('tr')	
	for row in rows:
		api_name=row.find('td',{'class':'views-field views-field-title col-md-3'})
		api_url=api_name.find('a').get('href')
		api_name=api_name.text if api_name else "N/A"
		api_description=row.find('td', {'class':'views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8'})
		api_description=api_description.text if api_description else "N/A"
		api_category=row.find('td',{'class':'views-field views-field-field-article-primary-category'})
		api_category=api_category.text if api_category else "N/A"
		api_info[count]=[api_name,api_url,api_category,api_description]
		count+=1


	if soup.find('a',{'title':'Go to next page'}):
		url_tag = soup.find('a',{'title':'Go to next page'})
		if url_tag.get('href'):
		    url='https://www.programmableweb.com' + url_tag.get('href')
		    print(url)
		else:
		    break
	else:
		break

api_df= pd.DataFrame.from_dict(api_info, orient = 'index', columns = ['API Name','API Url','API Category', 'API Description'])
api_df.to_csv('api_info.csv',sep='\t',encoding='utf-8')








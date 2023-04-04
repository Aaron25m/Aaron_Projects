#!/usr/bin/env python
# coding: utf-8

# # Finding the optimal product using Amazon and Flipkart Web Scraping

# We will first be Scraping Amazon for products based on user entry, then appending the products based on price and rating for Amazon and Flipkart respectively. We will then concatenate both the dataframes and deduce the most optimal choice.

# Concepts applied: Pandas, BeautifulSoup, Lists , Try and Except Exception Handling.

# In[174]:


url='https://www.amazon.in/gp/bestsellers/books/'
response = requests.get(url)
page_content=response.text
response.status_code


# In[175]:


page_content[0:500]


# In[176]:


from bs4 import BeautifulSoup
doc = BeautifulSoup(page_content, 'html.parser')
selection_class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"
books_title_tag=doc.find_all('div',{ 'class':selection_class})

def get_topic_titles(doc):
    selection_class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"
    books_title_tag=doc.find_all('div',{ 'class':selection_class})
    topic_titles = []
    for tag in books_title_tag:
        topic_titles.append(tag.text)
    return topic_titles
get_topic_titles(doc)


# In[177]:


books_url='https://www.amazon.in/gp/bestsellers/books/1318158031'
response=requests.get(books_url)
books_doc = BeautifulSoup(response.text, 'html.parser')
div_tags= books_doc.find_all('div',{'class':"zg-grid-general-faceout"})
#div_tags


# In[178]:



books_doc = BeautifulSoup(response.text, 'html.parser')
books_dict={
        'Book_Name':[],
        'Author_Name':[],
        'Book_URL':[],
        'Edition_Type':[],
        'Price':[],
        'Star_Rating':[],
        'Reviews':[]
    }    

def get_topic_page(books_urls):
    # download the page
    books_url='https://www.amazon.in/gp/bestsellers/books/1318158031'
    # check sucessful response
    response=requests.get(books_urls)
    
    if response.status_code!=200:
        raise Exception('failed to load page{}'.format(books_urls))
    # parse using BeautifulSoup
    topic_doc=BeautifulSoup(response.text, 'html.parser')
    #div_tags= books_doc.find_all('div',{'class':"zg-grid-general-faceout"})
    return topic_doc


def books_details(div_tags):
    #extracting book names
    Book_Name_tags =div_tags.find('span')
    #extracting author name of books 
    Author_Name_tags = div_tags.find('a', class_ = 'a-size-small a-link-child')
    #extracting books urls
    Book_URL = 'https://amazon.in' + div_tags.find('a', class_ = 'a-link-normal')['href']
    #extracting edition type of books
    Edition_Type_tags = div_tags.find('span', class_ = 'a-size-small a-color-secondary a-text-normal')
    #extracting price tag of book 
    Price_tags = div_tags.find('span', class_ = 'p13n-sc-price')
    #extracting star rating of books
    Star_Rating_tags = div_tags.find('span', class_ = 'a-icon-alt')
    #extracting review of books
    Reviews_tags = div_tags.find('span', class_ = 'a-size-small')
    return Book_Name_tags, Author_Name_tags, Book_URL, Edition_Type_tags, Price_tags, Star_Rating_tags, Reviews_tags

def get_books(books_doc):
    div_selection_class = 'zg-grid-general-faceout'
    div_tags = books_doc.find_all('div', class_ = div_selection_class ) # creating a dictionary   
    for i in range(0, len(div_tags)):
        books_info = books_details(div_tags[i])
        book_name(books_info)
        author_name(books_info)
        book_url(books_info)
        edition_type(books_info)
        book_price(books_info)
        star_rating(books_info)
        book_reviews(books_info)  
    return pd.DataFrame(books_dict)

    
def book_name(books_info):
    if books_info[0] is not None:
        books_dict['Book_Name'].append(books_info[0].text)
    else:
        books_dict['Book_Name'].append('Missing')
    return books_dict

def author_name(books_info):
    if books_info[1] is not None:
        books_dict['Author_Name'].append(books_info[1].text)
    else:
        books_dict['Author_Name'].append('Missing')
    return books_dict

def book_url(books_info):
    if books_info[2] is not None:
        books_dict['Book_URL'].append(books_info[2])
    else:
        books_dict['Book_URL'].append('Missing')
    return books_dict

def edition_type(books_info) :   
    if books_info[3] is not None:
        books_dict['Edition_Type'].append(books_info[3].text)
    else:
        books_dict['Edition_Type'].append('Missing')
    return books_dict 


def book_price(books_info):     
    if books_info[4] is not None:
        return books_dict['Price'].append(books_info[4].text)
    else:
        return books_dict['Price'].append('Missing')
    return books_dict
          
def star_rating(books_info):
    if books_info[5] is not None:
        books_dict['Star_Rating'].append(books_info[5].text)
    else:
        books_dict['Star_Rating'].append('Missing') 
    return books_dict   

def book_reviews(books_info):
    if books_info[6] is not None:
        books_dict['Reviews'].append(books_info[6].text)
    else:
        books_dict['Reviews'].append('Missing')
    return books_dict


# In[180]:


df.head()


# In[152]:


df=get_books(books_doc)
df['Reviews'] = df['Reviews'].str.replace(',', '').astype(str)
df['Reviews'] = pd.to_numeric(df['Reviews'],errors="coerce").fillna(0)
df['Rating'] = df['Star_Rating'].str.split().str[0]
df["Rating"]=pd.to_numeric(df['Rating'],errors="coerce").fillna(0)
del df['Star_Rating']
df["Price"]=df['Price'].str.replace(',', '').str.replace('₹', '').astype(float)
df.head()


# In[153]:


df["Edition_Type"].unique()


# In[161]:


data=df[df["Edition_Type"]=="Hardcover"]
data = data.sort_values(["Reviews"], axis=0, ascending=False)[:20]
data=data.sort_values(["Rating"],axis=0,ascending=False)[:20]
data= data.drop_duplicates(subset="Author_Name", keep="first")
data.head(1)


# In[160]:


data=df[df["Edition_Type"]=="Audible Audiobook"]
data = data.sort_values(["Reviews"], axis=0, ascending=False)[:20]
data=data.sort_values(["Rating"],axis=0,ascending=False)[:20]
data= data.drop_duplicates(subset="Author_Name", keep="first")
data.head(1)


# In[159]:


data=df[df["Edition_Type"]=="Paperback"]
data = data.sort_values(["Reviews"], axis=0, ascending=False)[:20]
data=data.sort_values(["Rating"],axis=0,ascending=False)[:20]
data= data.drop_duplicates(subset="Author_Name", keep="first")
data.head(1)


# In[158]:


data=df[df["Edition_Type"]=="Kindle Edition"]
data = data.sort_values(["Reviews"], axis=0, ascending=False)[:20]
data=data.sort_values(["Rating"],axis=0,ascending=False)[:20]
data= data.drop_duplicates(subset="Author_Name", keep="first")
data.head(1)


# In[142]:


plt.scatter(data[""])


# In[98]:


import matplotlib.pyplot as plt
plt.bar(df["Author_Name"],df["Price"])
plt.show()


# In[8]:


print(list1)
df=pd.DataFrame(list1,columns=["Product Name"])


# # We will now upload the data to a pandas dataframe

# In[14]:


df = pd.DataFrame(list(zip(list1, list2,list3,list4,list5)),columns =['Title', 'Price','Rating','Review count','Availability'])
df.drop(df[df['Title'] == "NA"].index, inplace = True)
sorted=df.sort_values(by=['Rating'], ascending=False)
sorted


# # Sorting Based on Max Ratings

# In[15]:


maxClm = df.max()['Rating']
maxClm
df_new = sorted[sorted['Rating'] == maxClm]
df_new=df_new.reset_index(drop=True)
df_new


# # Final Verdict 

# In[16]:


best_product_price=sorted.iloc[0]['Title']
if (len(df_new)>1):
    print("You can choose from the following!")
    print(df_new[['Title', 'Price','Rating']])
else:
    print("The {} with highest rating is {} ".format(your_keyword,best_product_price))


# # Flipkart Web Scraping

# In[27]:


listA=[]
listR=[]
listP=[]
listC=[]
listT=[]

def main(URL):
    # opening our output file in append mode
   

    # specifying user agent, You can use other user agents
    # available on the internet
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # retrieving product title
    try:
        # Outer Tag Object
        title=soup.find("span",attrs={"class": 'B_NuCI'})

        # Inner NavigableString Object
        title_value=title.string

        # Title as a string value
        title_string=title_value.strip().replace(',', '')

    except AttributeError:
        title_string = "NA"
   
    #appending the title in list title
   
    listT.append(title_string)
    # saving the title in the file
    #File.write(f"{title_string},")

    # retrieving price
    try:
        price = soup.find("div", attrs={'class': '_30jeq3 _16Jk6d'}).string.strip().replace(',', '').replace("₹", "")
       
    except:
        price = "NA"
   
    listP.append(price)

    # saving
    #File.write(f"{price},")

    # retrieving product rating
    try:
        rating = soup.find("div", attrs={'class': '_2d4LTz'}).string.strip().replace(',', '')

    except AttributeError:

        try:
            rating = soup.find("div", attrs={'class': '_3LWZlk'}).string.strip().replace(',', '')
        except:
            rating = "NA"
    rating=rating[:4]
   
    listR.append(rating)

    #File.write(f"{rating},")

    try:
        review_count = soup.find("div", attrs={'class': 'col-12-12'}).string.strip().replace(',', '')

    except AttributeError:
        review_count = "NA"
       
   
    listC.append(review_count)
    #File.write(f"{review_count},")


#The find_all() function returns an iterable object containing multiple Tag objects.
#we pick each Tag object and pluck out the link stored as a value for href attribute.
user=str(input("Enter the name of product: "))

url="https://www.flipkart.com/search?q={}".format(user)
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

webpages2 = requests.get(url, headers=HEADERS)
# Soup Object containing all data
soup = BeautifulSoup(webpages2.content, "lxml")

links = soup.find_all("a", attrs={'class':'_1fQZEK'})
links_list = []
for link in links:
    links_list.append(link.get('href'))


# iterating over the urls
for link in links_list:
    url2="https://www.flipkart.com" + link
    main(url2)


# # Appending the data to a dataframe

# In[28]:


print(listT)
df1=pd.DataFrame(listT,columns=["Product Name"])
df1 = pd.DataFrame(list(zip(listT, listP,listR,listC)),columns =['Title', 'Price','Rating','Review count'])
df1.drop(df1[df1['Title'] == "NA"].index, inplace = True)
sorted1=df1.sort_values(by=['Rating'], ascending=False)
sorted1


# # Sorting based on Rating and Price

# In[34]:


maxClm1 = df1.max()['Rating']
maxClm1
df_new1 = sorted1[sorted1['Rating'] == maxClm1]
df_new1=df_new1.reset_index(drop=True)
df_new1
lowest_price1=df_new1["Price"]
low1=lowest_price1.min()
low1
df1.loc[df1["Price"]==low1]
best_product_price=sorted.iloc[0]['Title']
if (len(df_new1)>1):
    print("You can choose from the following!")
    print(df_new1[['Title', 'Price','Rating']])
else:
    print("I pick ".format(your_keyword,best_product_price))


# # Optimal Product Considering both the Amazon and Flipkart selections:

# In[43]:


final=[df_new,df_new1]
final_df=pd.concat(final)
final_df = final_df.drop('Review count', axis=1)
final_df = final_df.drop('Availability', axis=1)
lowest_price1=final_df["Price"]
low1=lowest_price1.min()
low1
final_df.loc[final_df["Price"]==low1]
if (len(final_df)>1):
    print("You can choose from the following!")
    print(final_df[['Title', 'Price','Rating']])
    choice=input("Do you want us to pick for you? (Yes/No)")
    if choice=="Yes":
      print("Our choice is: ")
      print(final_df.sample())
else:
    print("I pick ".format(your_keyword,best_product_price))


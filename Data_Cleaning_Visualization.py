from accessing_database import *
import matplotlib.pyplot as plt
import seaborn as sns


# check na value
def check_na(dataset):
    print(dataset.isna().sum().sort_values(ascending=False)[:] * 100 / len(dataset))


# check_na(max_sold_item)
# found some NA values, need to be converted to 0
max_sold_item.fillna(0, inplace=True)

# check_na(max_sold_category)
# found some NA values, need to be removed
max_sold_category = max_sold_category.dropna()

# check_na(max_order_customer)
# check_na(max_customer_city)
# check_na(max_customer_state)
# check_na(max_seller_city)
# check_na(max_seller_state)
# didn't found any NA values, all good

# check if description length or number of photos has anything to do with how much product is sold
# fig, axes = plt.subplots(1, 2, sharey=True)
# phot = sns.scatterplot(data=max_sold_item.head(100), x="product_photos_qty", y="total_sold_qty", ax=axes[0])
# phot.set_title('Total Sold vs Photos Qty', fontdict={'weight': 'bold'})
# phot.set_xlabel('Photos Qty')
# phot.set_ylabel('Total Sold Qty')
# desc = sns.scatterplot(data=max_sold_item.head(100), x="product_description_lenght", y="total_sold_qty", ax=axes[1])
# desc.set_title('Total Sold vs Description Length', fontdict={'weight': 'bold'})
# desc.set_xlabel('Description Length')
# plt.show()

# check which product categories are the best selling ones
# chart = sns.barplot(x="total_qty", y="product_category_name_english", data = max_sold_category.head(10), palette='colorblind')
# chart.set_title('Top Ten Sold Product Category', fontdict={'size': 20, 'weight': 'bold'})
# chart.set_xlabel('Total Products Sold')
# chart.set_ylabel(None)
# plt.show()

# Compare number of customer with only 1 order vs more than 1 order using pie chart
ord_per_cust_table = {
    'More than 1 order': len(max_order_customer[max_order_customer["order_count"] > 1]),
    'Only 1 order': len(max_order_customer[max_order_customer["order_count"] == 1])
}

# plt.title('Number of Order per Customer', fontweight='bold')
# plt.pie(list(ord_per_cust_table.values()), labels=list(ord_per_cust_table.keys()), colors=sns.color_palette('colorblind'), autopct='%.2f%%')
# plt.show()

# Compile list of cities and states with the highest number of customer order
# fig, axes = plt.subplots(1, 2)
# cust1 = sns.barplot(x="order_count", y="customer_city", data = max_customer_city.head(10), palette='colorblind', ax=axes[0])
# cust1.set_title('City', fontdict={'weight': 'bold'})
# cust1.set_xlabel('Number of Orders')
# cust1.set_ylabel('')
# cust2 = sns.barplot(x="order_count", y="customer_state", data = max_customer_state.head(10), palette='colorblind', ax=axes[1])
# cust2.set_title('State', fontdict={'weight': 'bold'})
# cust2.set_xlabel('Number of Orders')
# cust2.set_ylabel('')
# fig.suptitle('Cities and States with Maximum Customer Order', weight= 'bold', fontsize=20)
# plt.show()

# Compile list of cities and states with the highest number of customer order
fig, axes = plt.subplots(1, 2)
sell1 = sns.barplot(x="total_item_sold", y="seller_city", data = max_seller_city.head(10), palette='colorblind', ax=axes[0])
sell1.set_title('City', fontdict={'weight': 'bold'})
sell1.set_xlabel('Product Qty Sold')
sell1.set_ylabel('')
sell2 = sns.barplot(x="total_item_sold", y="seller_state", data = max_seller_state.head(10), palette='colorblind', ax=axes[1])
sell2.set_title('State', fontdict={'weight': 'bold'})
sell2.set_xlabel('Product Qty Sold')
sell2.set_ylabel('')
fig.suptitle('Cities and States with Maximum Products Sold', weight= 'bold', fontsize=20)
plt.show()

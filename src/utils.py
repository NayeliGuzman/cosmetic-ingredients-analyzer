import re
import numpy as np
import pandas as pd

def clean(df):
    df = df.replace('\*','',regex=True).astype(str)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    num_ingredients = []

    for _, row in df.iterrows():
        row['Ingredients'] = row['Ingredients'].upper()
        #row['Ingredients'] = row['Ingredients'].split(", ") #make a list
        row['Ingredients'] = re.split(r",\s*|\|\s*", row['Ingredients'])
        aqua_list = ['AQUA/', "AQUA ", "WATER", "EAU"]
        for item in aqua_list:
            if row['Ingredients'][0].startswith(item):
                row['Ingredients'][0] = row['Ingredients'][0].replace(row['Ingredients'][0], "AQUA")
                break
        num_ingredients.append(len(row['Ingredients']))

    df['# of Ingredients'] = num_ingredients #add number of ingredients
    return df


def find_actives(df):
    df['Actives'] = ''
    df['Properties'] = [[] for _ in range(len(df))]
    df['Caution'] = [[] for _ in range(len(df))]
    vitamin_c = ['SODIUM ASCORBYL PHOSPHATE','ASCORBYL PALMITATE','ASCORBYL GLUCOSIDE','MAGNESIUM ASCORBYL PHOSPHATE','TETRAHEXYLDECYL ASCORBATE','ASCORBIC ACID', 'ETHYL ASCORBIC ACID','L-ASCORBIC ACID', 'ASCORBATE']
    retinols = ['RETINOL','VITAMIN A','RETINYL ACETATE','RETINYL PALMITATE','RETINOIC ACID','ALL-TRANS RETINOIC ACID','TRETINOIN']
    aha = ['AHA', 'ALPHA-HYDROXY ACID','GLYCOLIC ACID','PHYTIC ACID','LACTIC ACID','POLYHYDROXY ACID','TARTARIC ACID', 'MANDELIC ACID','MALIC ACID','CITRIC ACID', 'HYDROXYCAPRYLIC ACID', 'HYDROXYCAPRIC ACID']
    bha = ['BHA', 'BETA-HYDROXY ACID','SALICYLIC ACID','HYDROXYBUTANOIC ACID','TRETHOCANIC ACID','TROPIC ACID','WILLOW EXTRACT','TRETHOCANIC ACID','BETA-HYDROXYBUTANOIC ACID', 'BENZOYL PEROXIDE'] 
    cautionary_ingredients = ['BENZOYL PEROXIDE']
    humectant = ['HYALURONIC ACID','HYDROLYZED HYALURONIC ACID','SODIUM HYALURONATE','SODIUM HYALURONATE CROSSPOLYMER','SODIUM ACETYLATED HYALURONATE', 'GLYCERIN', 'GLYCEROL']
    niacinamide = ['NICOTINAMIDE','NICOTINIC ACID AMIDE','3-PYRIDINECARBOXAMIDE','NIACINAMIDE', 'VITAMIN B3']
    actives = [vitamin_c, retinols, aha, bha, cautionary_ingredients, humectant, niacinamide]
    for ind, row in df.iterrows():
        list_ = []
        for category in actives:
            #find common items that match any substring
            common_items = [x for x in category if any(x in ingredient for ingredient in row['Ingredients'])]
            if len(common_items)!=0:
                list_.append(common_items)
                if category==vitamin_c:
                    df.at[ind,'Properties'].append('vitamin c')
                    df.at[ind, 'Caution'].append('DO NOT use with AHA/BHA')
                if category == retinols:
                    df.at[ind, 'Properties'].append('retinol')
                    df.at[ind, 'Caution'].append('DO NOT use with benzoyl peroxide')
                if category == aha:
                    df.at[ind, 'Properties'].append('aha-exfoliant')
                    df.at[ind, 'Caution'].append('DO NOT use with vit C')
                if category == bha:
                    df.at[ind, 'Properties'].append('bha-deep exfoliant')
                    df.at[ind, 'Caution'].append('DO NOT use with retinol, vitC')
                if category == humectant:
                    df.at[ind, 'Properties'].append('humectant')
                if category == niacinamide:
                    df.at[ind, 'Properties'].append('niacinamide')
                    df.at[ind, 'Caution'].append('DO NOT use with AHA/BHA')
        df.at[ind, 'Actives'] = list_ 
    return df
           
def find_peptides(df):
    '''
    Finds Peptides in an ingredient list
    Parameters: 
        df: DataFrame containing a list of products
    Output:
        df containing the upated Properties
    '''
    for ind, row in df.iterrows():
        list_ = []
        common_items = [ingredient for ingredient in row['Ingredients'] if 'PEPTIDE' in ingredient]
        if common_items:
            df.at[ind, 'Actives'].extend(common_items)  # Extend the existing list with new peptides
            df.at[ind,'Properties'].append('peptides')
    
    return df

def find_ceramides(df):
    '''
    Finds Ceramides in an ingredient list
    Parameters: 
        df: DataFrame containing a list of products
    Output:
        df containing the upated Properties
    '''
    for ind, row in df.iterrows():
        list_ = []
        common_items = [ingredient for ingredient in row['Ingredients'] if 'CERAMIDE' in ingredient]
        if common_items:
            df.at[ind, 'Actives'].extend(common_items)  # Extend the existing list with new ceramides
            df.at[ind,'Properties'].append('ceramides')
    
    return df
    

def compare_two(df, products):
    '''   
    Compare two products and show key info along with shared ingredients.
    
    Parameters:
        df: DataFrame containing product info
        products (list): list of two product names to compare
        
    Output:
        Display of product info and shared ingredients
    '''
    ind_1=df[df['Product']==products[0]].index[0]
    ind_2=df[df['Product']==products[1]].index[0]
    list1 = df.iloc[ind_1]['Ingredients']
    list2 = df.iloc[ind_2]['Ingredients']
    df_batch = df.iloc[[ind_1, ind_2]]
    shared_ingredients = sorted(set(list1) & set(list2))
    
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    
    intersection = len(set(list1) & set(list2))
    union = len(set(list1) | set(list2))
    similarity = (intersection / union) * 100
    list3 = df.iloc[ind_1]['Caution']
    list4 = df.iloc[ind_2]['Caution']
    if len(list3)==0 or len(list4)==0:
        caution = 0
    elif list3[0]==list4[0]: #same elements
        caution = 0
    elif list3[0]!=list4[0]: #different elements
        caution = 1

    # --- Display ---
    print("\n=== Product Comparison ===\n")
    display(df_batch[['Product', '# of Ingredients', 'Actives', 'Properties']])
    
    print("\nShared Ingredients ({}):".format(len(shared_ingredients)))
    if shared_ingredients:
        print(", ".join(shared_ingredients))
    else:
        print("None")
    
    print(f"\nSimilarity: {similarity:.2f}%")
    
    if caution==1:
        print("These products may not be used together!")
    else:
        print("No caution flags detected.")
    
    print("\n==========================\n")    
    return result, df_batch, similarity, caution


def compute_similarity(df, product1, product2):
    '''
    Jaccard Similarity used to compute the similarity between two ingredients lists
    0->completely different, 100->identical 
    Parameters:
        df - DataFrame containing the two products
        product1, product2 - two strings, the name of the products to compute similarity for
    Output:
        the similarity score as a value
    '''
    ind_1=df[df['Product']==product1].index[0] #extract ingredients list
    ind_2=df[df['Product']==product2].index[0]
    list1 = df.iloc[ind_1]['Ingredients']
    list2 = df.iloc[ind_2]['Ingredients']
    intersection = len(set(list1) & set(list2)) #count overlap/shared (intersection)
    union = len(set(list1) | set(list2)) #count total unique (union)
    similarity = (intersection / union) * 100
    return similarity
    
def most_similar(df, target_product):
    
    products = df['Product'].tolist()

    # List to hold the product pairs and their similarity scores
    similarity_scores = []

    # Generate all possible pairs of products using combinations (no repeats)
    for p1, p2 in itertools.combinations(products, 2):
        score = compute_similarity(df, p1, p2)
        # Store the pair and their similarity score
        similarity_scores.append({'Product1': p1, 'Product2': p2, 'SimilarityScore': score})

    # Filter the similarity scores to include only pairs where one of the products is the target product
    filtered_scores = [score for score in similarity_scores if target_product in [score['Product1'], score['Product2']]]

    # Sort the similarity scores in descending order to find the most similar product
    sorted_scores = sorted(filtered_scores, key=lambda x: x['SimilarityScore'], reverse=True)

    # Get the product most similar to the target product
    most_similar_product = None
    if sorted_scores:
        most_similar_product = sorted_scores[0]
        
    return most_similar_product

        
def add_most_similar_column(df):
    '''
    Adds Columns to a DataFrame containing the most similar product and similarity score
    Parameters: 
        df - DataFrame
    Output:
        df - updated DataFrame 
    '''
    most_similar_products = []
    most_similar_scores = [] 
    
    # Get the list of products
    products = df['Product'].tolist()
    
    # Iterate through each product in the DataFrame
    for product in products:
        # List to hold similarity scores for the current product
        similarity_scores = []
        
        # Compare the product with every other product
        for other_product in products:
            if product != other_product:  # Skip comparing the product to itself
                score = compute_similarity(df, product, other_product)
                similarity_scores.append({'Product': other_product, 'Similarity Score': score})
            elif product == other_product:
                #if comparing the product to itself
                similarity_scores.append({'Product': other_product, 'Similarity Score': 0})
        
        # Sort the similarity scores in descending order to find the most similar product
        most_similar_product = max(similarity_scores, key=lambda x: x['Similarity Score'])

        # Append the most similar product to the list
        most_similar_products.append(most_similar_product['Product'])
        most_similar_scores.append(most_similar_product['Similarity Score']) 
    
    df['Most Similar'] = most_similar_products
    df['Similarity Score'] = most_similar_scores

    return df

def show_properties(df):
    '''
    Displays the entire list of products and their properties
    '''
    return df[['Product','# of Ingredients','Actives','Properties', 'Caution', 'Most Similar']]

def show_most_similar(df):
    '''
    Displays the entire list of products with their most similar product and similarity scores
    '''
    value = df[['Similarity Score']]
    return df[['Product','Most Similar', 'Similarity Score']]
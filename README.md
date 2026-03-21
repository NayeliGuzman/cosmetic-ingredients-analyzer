# Skincare Ingredients Analyzer

## Description:
A data-driven tool for analyzing skincare products based on their ingredient lists. This tool could help a user avoid using incompatible products which would lead to irritation or a compromised skin barrier. It could also be used as a consumer tool to compare luxury vs drug store products with similar claims. This tool does not compare packaging (experiential) or marketing features of products and focuses on skin care actives. 

## Features:

- Analyze ingredient lists for skincare products
- Compares two products and identifies shared ingredients
- Compute similarity scores using Jaccard similarity
- Find the most similar products for each item in the dataset
- Flag potential incompatibilities between products

## Environment:
- Python 3.9.20
- Install dependencies with:
 
pip install -r requirements.txt


## Usage:

1. Run the notebook:

bash

jupyter notebook

2. Open:

ingredient-analyzer.ipynb

## Future Improvements:

- Make the ingredients detection more robust to percentages and variations of the same ingredient
- Add a more robust incompatibility detection
- Include SPF detection and specify type (mineral or chemical)
- Build a simple web interface

### Author
Nayeli Guzman


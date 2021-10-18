#https://fr.openfoodfacts.org/data
from flask import redirect
import openfoodfacts


def keyword_search(keywords):
    search_result = openfoodfacts.products.advanced_search({
     "search_terms": keywords,
     "page_size": "50"})
    return search_result


def barcode_search(barcode):
    return "https://world.openfoodfacts.org/api/v0/product/" + barcode + ".json"

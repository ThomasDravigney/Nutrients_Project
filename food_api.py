import openfoodfacts


def search(keywords):
    search_result = openfoodfacts.products.advanced_search({
     "search_terms": keywords,
     "page_size": "50"})
    return search_result

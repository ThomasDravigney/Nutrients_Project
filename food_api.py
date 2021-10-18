import openfoodfacts


def search(keywords):
    search_result = openfoodfacts.products.advanced_search({
     "search_terms": keywords,
     "countries": "fr",
     "page_size": "20"})
    return search_result

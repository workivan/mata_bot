with open('filter.txt', 'r', encoding='utf-8') as file:
    FILTER_LIST = file.read().splitlines()
   
print(FILTER_LIST)

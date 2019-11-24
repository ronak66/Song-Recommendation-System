import json, csv
data = []
with open('final.txt') as f:
    for line in f:
        data.append(json.loads(line))

data = data[0]

d = []
for key, value in data.items():
    for values in value:
        values.update({"label": key})
        d.append(values)

# with open('mycsvfile.csv', 'w') as f:
#     w = csv.DictWriter(f, my_dict.keys())
#     w.writeheader()
#     w.writerow(my_dict)



f = open('data.csv','w')
w = csv.DictWriter(f,d[0].keys())
w.writeheader()
w.writerows(d)
f.close()
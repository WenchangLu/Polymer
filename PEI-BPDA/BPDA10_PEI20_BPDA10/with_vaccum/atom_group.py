groups =[]

num_groups = 8
num_each = 2208//num_groups
for i in range(num_groups):
    groups.append([i * num_each +1, (i+1) * num_each +1])
print(groups)    
temperature = 300.0
dt = 0.1e-15 *20

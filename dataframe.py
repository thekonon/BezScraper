import pandas as pd

a = (1,1,3,4,5)
b = ('a', 'b', 'c', 'd','e')
c = (3,-5,3,4,5)

my_dict = {"A val": a, 'B val': b, 'C val': c}
my_frame = pd.DataFrame(my_dict).to_excel("Myexc.xlsx")
print(my_frame)
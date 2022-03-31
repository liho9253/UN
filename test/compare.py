# -*- coding: utf-8 -*-
import pandas as pd

df1 = pd.read_csv("two.txt", encoding='utf-8').rename(columns={'course_title':'name'})


df2 = pd.read_csv("two.txt", encoding='utf-8')

result = df1.merge(df2, how='inner')
print(df2)




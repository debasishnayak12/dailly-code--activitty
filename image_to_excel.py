from ExtractTable import *
et_sess = ExtractTable(api_key='luXjriM4H1SJHwMUhDPCFh3QT4mH1ZBBIjIVJPvM')    # Replace your VALID API Key here
print(et_sess.check_usage())                    # Validates API Key & show credits usage 
table_data = et_sess.process_file(filepath="C:\\Users\madhu\\Desktop\\school_contacts\\21img.jpg", output_format="df")

import pandas as pd
import numpy as np
print("Dtype of table :",type(table_data))
df=pd.DataFrame([table_data])
df.to_excel("C:\\Users\madhu\\Desktop\\school_contacts\\21img_excel.xlsx")
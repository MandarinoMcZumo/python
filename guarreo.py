
for i in range(0, len(categoricas), 7):
    g1 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i], type='nominal'),
                                   alt.Y(categoricas[i], type='nominal', aggregate='count')).interactive()
    g2 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 1], type='nominal'),
                                   alt.Y(categoricas[i + 1], type='nominal', aggregate='count')).interactive()
    g3 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 2], type='nominal'),
                                   alt.Y(categoricas[i + 2], type='nominal', aggregate='count')).interactive()  
    g4 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 3], type='nominal'),
                                   alt.Y(categoricas[i + 3], type='nominal', aggregate='count')).interactive()
    g5 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 4], type='nominal'),
                                   alt.Y(categoricas[i + 4], type='nominal', aggregate='count')).interactive()
    g6 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 5], type='nominal'),
                                   alt.Y(categoricas[i + 5], type='nominal', aggregate='count')).interactive()
    g7 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 6], type='nominal'),
                                   alt.Y(categoricas[i + 6], type='nominal', aggregate='count')).interactive()
    
    alt.hconcat(g1, g2, g3, g4, g5, g6).display()


result = {}
rep = []
for i in dt_cat:
    result.update({i: dt_cat[i].value_counts()/len(dt_cat)})

for key in result:
    for cc, i in enumerate(result[key]):
        if i>0.05:
            rep.append([key, result[key].keys()[cc], result[key][cc]])
            
rep = pd.DataFrame(rep)
rep.columns = ['var', 'value', '%']
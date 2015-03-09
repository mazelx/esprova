for r in a.race_list:
    s = (r.get('discipline', None), r.get('format', None))
    i = 0
    try:
        i = [s.get('sport') for s in sports].index(s)
    except ValueError:
        sports.append({'sport':s, 'count':1})
        continue
    sports[i]['count'] +=1


 json.dumps(sorted(sports, key= lambda x: (x['sport'])))
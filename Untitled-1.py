# for element in elements:
    #     try:
    #         timer = time.strptime(code, "%Y-%m-%d %H:%M:%S")
    #         timer = time.strftime("%Y-%m-%d %H:%M:%S", timer)
    #         bound.append(timer)
    #     except:
    #         if(code in places):
    #             new_places.append(element)
    # if(len(bound)==1):
    #     sources_data = sources_data[sources_data['jzsj']<=bound[0]]
    # if(len(bound)>1):
    #     sources_data = sources_data[(sources_data['jzsj']>=bound[0])&(sources_data['jzsj']<=bound[1])]
    # if(len(new_places)>0):
    #     sources_data = sources_data[sources_data['srd'] in new_places]
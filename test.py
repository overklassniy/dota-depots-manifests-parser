from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime as dt
from static import depot_URLs, month_dict

web = webdriver.Chrome()

patch_url = 'https://steamdb.info/patchnotes/6625855/'
patch_id = patch_url.split('/')[-2]
search_url = '/patchnotes/' + patch_id + '/'
web.get('https://steamdb.info/app/570/patchnotes/')
bs_patch = BeautifulSoup(web.page_source, 'html.parser')
bs_patches = bs_patch.find_all('a', href=True)
bs_patch_el = ''
for element in bs_patches:
    # print(element)
    # print(type(element.text))
    # print(element.text)
    # print()
    # print(str(element))
    # print()
    selement = str(element)
    if search_url in selement:
        bs_patch_el = element
        break
bs_patch_el_parent = bs_patch_el.parent
bs_patch_el_parent_parent = bs_patch_el_parent.parent
# print(str(bs_patch_el_parent_parent).split('\n')[0])
patch_timestamp = dt.fromtimestamp(float(str(bs_patch_el_parent_parent).split('\n')[0].split('"')[-2])-10800)
print(patch_timestamp)
# find all previous там найдешь tr с таймштампом и получишь дату далее пройдешься по депотам и вуаля

# web.get(depot_URLs[0])
# bs_depot = BeautifulSoup(web.page_source, "html.parser")
# dates_depot = bs_depot.find_all(class_='text-right')
# manifests_depot = bs_depot.find_all(class_='tabular-nums')
# print(manifests_depot)
# for i_date in range(len(dates_depot)):
#     date, time = dates_depot[i_date].text.split(' – ')
#     day, month, year = date.split()
#     t_month = month_dict[month]
#     t_date = ' '.join([str(day), str(t_month), str(year)])
#     t_time = time.split()[0]
#     t_datetime = t_date + ' ' + t_time
#     dt_date = dt.strptime(t_datetime, '%d %m %Y %H:%M:%S')
#     print(dt_date)
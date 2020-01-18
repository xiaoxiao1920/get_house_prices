#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @file: get_guangzhou_house_prices.py
# @author: xulinzhou
# @date  : 2020/1/16

import requests
from bs4 import BeautifulSoup
import re

headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"no-cache",
    "cookie":"sessid=6AF6DFCD-6388-FAEF-0CB3-CD14DA0A4090; aQQ_ajkguid=9C7AEAE4-7B90-8D6A-1FE2-7C7B6CBB418E; lps=http%3A%2F%2Fwww.anjuke.com%2Ffangjia%2Fguangzhou2015%2F%7C; twe=2; 58tj_uuid=7daeead0-f0d8-4fa3-b083-72479504d1ae; init_refer=; new_uv=1; als=0; wmda_uuid=8135416bd9db5477bee2d66f79833d30; wmda_new_uuid=1; wmda_session_id_6289197098934=1579143504700-7560225b-1361-647d; wmda_visited_projects=%3B6289197098934; new_session=0; __xsptplusUT_8=1; xzfzqtoken=77eBerhFOQT0ymUqf51oYYomGuGoRLr%2BxyIrvFOKUaIFodp8Lm8%2BMEePaHr38frLin35brBb%2F%2FeSODvMgkQULA%3D%3D; __xsptplus8=8.1.1579143504.1579144494.6%234%7C%7C%7C%7C%7C%23%23NEUvEKR17rMnWCES083wbSm22MLWPZmC%23",
    "pragma":"no-cache",
    "sec-fetch-mode":"navigate",
    "sec-fetch-site":"cross-site",
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

# 获取某个城市某一年的12个月的房价，返回一个list，包含12个int类型房价
def get_year_prices_list(url):
    s = requests.get(url=url, headers=headers)
    # print(s.text)
    s.encoding = "utf-8"
    soup = BeautifulSoup(str(s.text), 'html.parser')
    all_temp = str(soup.find_all(href=re.compile("javascript")))

    r = re.compile("\d*元")
    res_list = re.findall(r, all_temp)
    year_prices_list = []  # 用于存储获取到的各个月份房价值
    for p in res_list:
        year_prices_list.append(int(p[:-1]))
    # 有的城市每年数据不够12个月的，补0
    year_prices_list_len = len(year_prices_list)
    if year_prices_list_len < 12 and year_prices_list_len >0:
        for i in range(12-year_prices_list_len):
            year_prices_list.append(0)
    year_prices_list.reverse() # 获取到的year_prices_list是12月到1月的房价，需要反转一下，变成排序从1月到12月
    # print(year_prices_list)
    return year_prices_list



# 拼接出按年月串联的字符串，返回一个list
def get_year_month(year_list, month_list):
    year_month_list = []
    for y in year_list:
        for m in month_list:
            year_month_list.append(str(y)+m)
    return year_month_list


year_list = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
# year_list = [2015, 2016, 2017, 2018, 2019]
month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
first_city_list = ["beijing", "shanghai", "guangzhou", "shenzhen"]
first_city_chinese_list = ["北京", "上海", "广州", "深圳"]
new_first_city_list = ["chengdu", "hangzhou", "chongqing", "wuhan", "xa", "suzhou", "tianjin", "nanjing", "cs", "zhengzhou", "dg", "qd", "sy", "nb", "km"]
new_first_city_chinese_list = ["成都", "杭州", "重庆", "武汉", "西安", "苏州", "天津", "南京", "长沙", "郑州", "东莞", "青岛", "沈阳", "宁波", "昆明"]
year_month_list = get_year_month(year_list, month_list)


# 获取所有给定城市的房价指定年份的所有房价数据，全部存储在一个list中
def get_all_city_prices_dict(city_list, year_list):
    all_city_house_price_list = []
    for city in city_list:
        any_city_all_year_prices_list = []
        for year in year_list:
            url = "https://www.anjuke.com/fangjia/" + str(city) + str(year) # 拼接访问的url
            any_year_prices_list = get_year_prices_list(url) # 获取得某个城市某一年的房价数据
            for a in any_year_prices_list:
                any_city_all_year_prices_list.append(a)
        all_city_house_price_list.append(any_city_all_year_prices_list)
    # print(all_city_house_price_list)
    return all_city_house_price_list


# 通过调用安居客网站的接口，获取对应房价数据（需要更新数据时使用）
all_first_city_house_price_list = get_all_city_prices_dict(first_city_list, year_list)
all_new_first_city_house_price_list = get_all_city_prices_dict(new_first_city_list, year_list)
print("https://www.anjuke.com/fangjia/beijing2019")
print(all_first_city_house_price_list)
print(all_new_first_city_house_price_list)

# 2015-2019的房价数据
# all_first_city_house_price_list = [[37261, 37732, 37876, 38231, 38716, 38850, 39691, 40168, 40448, 40702, 40851, 39437, 39620, 40042, 42083, 44387, 44752, 44854, 45797, 47135, 50136, 53552, 56059, 57597, 58064, 59531, 61613, 54704, 53049, 51155, 51382, 53921, 58931, 58077, 57662, 57768, 57523, 57557, 57717, 57839, 57931, 58166, 58355, 59376, 59913, 59943, 59602, 59868, 60017, 60125, 60487, 59993, 59809, 60142, 60061, 59888, 59590, 59126, 58540, 58568], [30826, 31198, 31198, 31136, 31607, 32030, 32592, 32713, 33073, 33470, 34167, 35237, 36665, 37795, 43840, 45397, 45484, 45411, 45338, 46271, 48009, 49765, 51292, 52142, 52640, 53228, 52146, 51791, 53919, 53343, 52805, 50674, 50922, 50760, 49998, 50017, 50619, 51873, 51935, 50461, 50365, 50801, 50697, 50667, 50512, 50439, 50189, 49446, 49264, 49550, 49500, 49588, 49752, 50122, 50174, 50461, 50913, 51023, 50982, 50945], [18792, 18851, 19024, 19417, 19562, 19902, 20014, 19997, 19988, 19921, 19996, 20016, 20623, 20643, 20811, 21133, 21107, 21144, 21264, 21553, 21720, 22242, 22590, 22926, 23744, 24427, 25131, 25369, 26061, 27329, 28196, 28508, 28814, 28254, 28009, 28578, 28602, 29683, 30413, 31044, 31472, 32021, 32670, 33289, 33455, 32936, 32225, 32088, 32758, 32791, 32467, 32047, 32055, 32086, 32295, 31951, 31305, 31243, 31194, 31692], [28993, 29110, 29436, 30791, 33384, 36762, 39900, 39972, 40230, 40118, 39451, 41494, 45024, 47345, 48829, 46989, 45851, 44600, 44704, 45453, 45764, 45143, 44982, 43289, 46049, 46500, 47512, 49037, 49367, 49709, 50077, 50477, 50777, 51077, 51277, 51477, 51732, 52077, 52240, 52685, 52850, 53350, 53850, 54233, 54199, 53768, 53716, 53205, 53678, 53763, 53853, 54336, 54018, 53816, 54116, 54180, 54333, 54398, 54709, 54790]]
# all_new_first_city_house_price_list = [[8273, 8250, 8239, 8225, 8245, 8246, 8232, 8246, 8250, 8240, 8230, 8213, 8238, 8212, 8251, 8246, 8262, 8392, 8206, 8143, 8183, 8271, 8524, 8591, 8674, 8698, 9024, 9403, 9636, 9839, 9992, 10185, 10562, 11068, 11617, 12034, 12375, 12542, 12825, 13036, 13147, 13114, 14102, 14597, 14281, 13919, 13575, 13173, 13039, 13213, 13213, 13262, 13420, 13528, 13335, 13389, 13288, 13181, 13033, 13132], [16807, 16494, 16312, 16040, 16025, 16240, 16376, 16461, 16413, 16194, 16195, 16080, 17271, 17552, 17943, 18254, 18089, 18131, 18243, 18644, 19048, 20691, 21187, 21655, 23733, 24222, 25111, 25509, 25726, 25543, 26392, 27105, 27680, 28261, 28562, 28540, 28541, 28554, 28571, 28694, 28748, 29074, 29255, 29200, 29116, 29034, 28836, 28651, 28224, 28195, 27986, 27600, 28058, 28422, 28768, 28398, 28054, 27471, 27155, 27002], [6434, 6449, 6436, 6423, 6434, 6471, 6435, 6423, 6395, 6360, 6337, 6289, 7106, 7099, 7067, 7112, 7179, 6961, 6949, 6966, 7019, 7059, 7132, 7493, 7604, 7762, 7960, 8443, 8802, 9133, 9332, 9466, 9634, 9762, 9856, 9925, 10851, 11514, 10302, 10542, 11089, 12075, 12678, 12966, 12859, 12592, 12294, 12080, 11843, 11845, 11889, 11805, 11866, 11971, 12035, 12017, 11922, 11703, 11486, 11187], [9262, 9278, 9330, 9409, 9436, 9443, 9555, 9711, 9820, 9926, 10010, 10000, 10000, 10000, 10223, 10477, 10759, 11101, 11268, 11428, 11734, 12563, 13475, 13875, 13986, 14116, 14679, 15023, 15275, 15492, 15778, 15941, 16068, 16154, 16244, 16259, 16254, 16263, 16402, 16483, 16523, 16589, 16736, 16855, 17061, 17256, 17874, 17586, 17519, 17470, 17464, 17397, 17313, 17220, 17218, 17327, 17335, 17166, 17017, 16818], [6799, 6810, 6785, 6770, 6795, 6757, 6683, 6618, 6609, 6548, 6491, 6450, 6450, 6549, 6541, 6504, 6448, 6361, 6315, 6286, 6308, 6381, 6358, 6514, 6557, 6574, 6665, 6940, 7219, 7626, 7794, 7957, 8032, 8192, 8681, 8880, 8988, 9212, 9507, 10317, 11355, 11981, 12248, 12408, 12423, 12338, 12241, 12207, 12410, 12639, 12509, 12508, 12498, 12553, 12656, 12637, 12635, 12573, 12443, 12446], [10935, 10914, 10964, 10995, 11033, 11123, 11209, 11308, 11457, 11603, 11903, 12251, 12251, 12550, 14707, 15754, 16077, 16147, 15542, 15509, 15575, 16081, 16152, 16181, 15950, 16009, 16107, 15969, 15805, 15549, 15414, 15344, 15425, 15362, 15348, 15320, 15301, 15338, 15485, 15595, 15698, 15910, 15999, 16116, 16330, 16530, 16721, 16943, 17150, 17379, 17606, 17835, 18080, 18325, 18600, 18810, 19015, 19265, 19444, 19568], [14717, 14932, 14685, 14843, 14889, 15064, 15104, 15137, 15231, 15425, 15477, 15553, 15553, 15557, 16138, 16948, 17405, 17713, 17795, 18415, 19764, 22659, 22922, 23220, 23290, 23468, 24561, 25048, 25183, 24941, 24802, 24242, 23852, 23382, 22706, 22205, 21899, 21751, 21784, 21586, 21461, 21734, 22819, 23391, 23283, 22826, 22591, 22188, 22308, 22056, 21993, 22381, 22395, 22263, 22208, 22047, 21713, 21376, 21057, 20952], [18295, 18231, 18131, 18264, 18473, 18522, 18502, 18446, 18436, 18596, 18594, 18697, 18968, 19009, 19686, 20190, 20690, 21455, 21352, 21500, 22091, 23647, 24715, 24867, 25000, 25057, 25471, 25700, 25887, 25914, 25995, 26036, 26004, 25877, 25768, 25733, 25757, 25691, 25844, 25839, 25889, 25953, 26191, 26386, 27117, 27129, 27335, 27568, 27751, 28581, 29039, 29047, 29177, 28776, 28829, 28945, 28913, 28840, 28810, 28526], [6354, 6329, 6334, 6320, 6353, 6341, 6351, 6385, 6417, 6414, 6427, 6448, 6448, 6450, 6475, 6524, 6581, 6648, 6687, 6743, 6820, 7058, 7260, 7601, 7815, 7880, 8216, 8714, 8994, 9277, 9240, 9296, 9411, 9537, 9763, 9873, 9910, 9983, 10011, 10234, 10494, 10822, 10990, 11064, 11027, 10926, 10786, 10627, 10581, 10645, 10510, 10466, 10388, 10418, 10382, 10365, 10350, 10182, 10077, 10078], [8483, 8472, 8526, 8566, 8625, 8688, 8715, 8749, 8775, 8765, 8888, 8790, 8790, 8822, 8965, 9071, 9190, 9297, 9354, 9561, 10048, 11262, 11770, 12091, 12128, 12145, 12463, 12750, 12911, 12948, 12993, 12985, 12968, 12956, 12928, 12859, 12773, 12708, 12763, 12731, 12666, 12612, 12762, 12855, 13483, 13867, 13713, 13582, 13574, 13687, 13660, 13746, 13782, 13804, 13843, 13732, 13585, 13491, 13382, 13266], [8045, 8425, 8626, 8603, 8688, 8811, 8849, 8863, 8775, 8542, 8411, 8371, 8500, 8844, 9638, 10048, 9985, 9495, 9534, 9833, 10196, 11146, 11091, 11651, 11774, 11733, 11642, 12032, 12290, 13013, 12929, 12961, 13053, 13145, 13763, 13913, 13947, 14180, 14122, 14333, 14550, 14964, 15241, 15021, 15028, 15010, 14956, 14813, 15038, 15431, 15575, 15586, 15387, 15551, 15742, 15739, 15666, 15697, 15920, 16105], [12290, 12412, 12333, 12015, 12342, 12397, 12425, 12509, 12368, 12556, 12374, 12384, 12525, 12536, 12700, 12527, 12447, 12349, 12346, 12379, 12432, 13034, 13380, 13523, 13940, 14273, 15759, 17033, 16991, 17073, 17217, 17352, 17559, 17724, 17925, 18142, 18564, 19169, 19947, 20697, 20898, 20480, 20338, 20992, 20696, 20128, 19632, 18788, 18375, 18386, 18352, 18204, 18045, 18040, 17617, 17389, 17049, 16808, 16521, 16340], [7486, 7427, 7439, 7420, 7458, 7514, 7434, 7495, 7459, 7333, 7198, 7242, 7242, 7271, 7410, 7366, 7318, 7247, 7234, 7223, 7230, 7293, 7177, 7242, 7274, 7351, 7367, 7428, 7493, 7635, 7588, 7572, 7623, 7704, 7972, 7999, 8013, 8026, 8141, 8190, 8303, 8470, 8597, 8786, 8898, 8990, 9017, 9005, 9049, 9169, 9176, 9285, 9384, 9427, 9511, 9588, 9634, 9715, 9763, 9817], [12569, 12320, 12299, 12171, 12209, 12063, 11855, 11694, 12093, 12150, 12273, 12250, 12250, 12274, 12352, 12698, 12508, 12956, 13069, 13082, 13116, 13321, 13509, 13857, 14018, 14229, 14595, 15023, 15316, 15705, 16102, 16418, 16377, 16309, 16714, 17037, 17137, 17444, 17723, 18196, 18773, 19600, 20091, 20436, 20438, 20528, 20445, 20313, 20245, 20386, 20599, 20787, 20857, 21059, 21480, 21828, 22090, 22294, 22454, 22814], [8002, 7982, 7911, 7989, 8036, 8022, 8048, 8094, 8178, 8232, 8051, 8202, 8202, 8205, 8234, 8344, 8415, 8391, 8410, 8396, 8429, 8407, 8445, 8485, 8469, 8551, 8643, 8732, 8841, 9014, 9116, 9289, 9461, 9564, 9659, 9771, 9914, 10000, 10117, 10401, 10705, 11018, 11382, 11735, 11936, 12166, 12336, 12298, 12285, 12261, 12304, 12328, 12342, 12471, 12611, 12697, 12839, 12896, 12983, 13117]]


# # 2011-2019的房价数据
# all_first_city_house_price_list = [[25329, 25940, 26550, 26630, 26578, 26533, 26363, 26165, 26104, 25964, 25599, 25166, 24593, 24308, 24932, 25413, 25588, 25948, 26579, 27199, 28392, 29071, 29522, 30158, 31258, 32300, 34623, 37077, 37840, 38131, 38502, 38877, 39598, 40054, 40230, 40342, 40428, 40592, 40554, 39812, 39429, 39378, 37716, 37323, 36722, 36994, 37128, 37294, 37261, 37732, 37876, 38231, 38716, 38850, 39691, 40168, 40448, 40702, 40851, 39437, 39620, 40042, 42083, 44387, 44752, 44854, 45797, 47135, 50136, 53552, 56059, 57597, 58064, 59531, 61613, 54704, 53049, 51155, 51382, 53921, 58931, 58077, 57662, 57768, 57523, 57557, 57717, 57839, 57931, 58166, 58355, 59376, 59913, 59943, 59602, 59868, 60017, 60125, 60487, 59993, 59809, 60142, 60061, 59888, 59590, 59126, 58540, 58568], [23058, 23421, 23548, 23570, 23679, 23849, 23940, 23950, 23883, 23720, 23288, 22665, 22082, 21804, 22063, 22160, 22198, 22348, 22516, 22663, 22833, 22929, 23105, 23428, 23920, 24514, 25690, 26493, 26759, 26923, 27169, 27510, 28048, 28751, 29593, 29978, 30096, 30331, 30547, 30813, 30987, 30642, 30573, 30532, 30576, 30435, 30491, 30522, 30826, 31198, 31198, 31136, 31607, 32030, 32592, 32713, 33073, 33470, 34167, 35237, 36665, 37795, 43840, 45397, 45484, 45411, 45338, 46271, 48009, 49765, 51292, 52142, 52640, 53228, 52146, 51791, 53919, 53343, 52805, 50674, 50922, 50760, 49998, 50017, 50619, 51873, 51935, 50461, 50365, 50801, 50697, 50667, 50512, 50439, 50189, 49446, 49264, 49550, 49500, 49588, 49752, 50122, 50174, 50461, 50913, 51023, 50982, 50945], [13535, 14114, 14680, 14998, 14977, 14938, 14855, 14654, 14547, 14521, 14677, 14762, 14993, 15194, 15215, 15203, 15148, 15152, 15246, 15467, 15754, 15886, 16207, 16555, 17003, 17423, 17665, 17651, 17304, 17515, 17759, 18293, 19011, 19445, 19589, 19208, 18893, 18977, 19460, 19040, 18757, 18440, 17764, 17450, 17312, 17338, 18081, 18564, 18792, 18851, 19024, 19417, 19562, 19902, 20014, 19997, 19988, 19921, 19996, 20016, 20623, 20643, 20811, 21133, 21107, 21144, 21264, 21553, 21720, 22242, 22590, 22926, 23744, 24427, 25131, 25369, 26061, 27329, 28196, 28508, 28814, 28254, 28009, 28578, 28602, 29683, 30413, 31044, 31472, 32021, 32670, 33289, 33455, 32936, 32225, 32088, 32758, 32791, 32467, 32047, 32055, 32086, 32295, 31951, 31305, 31243, 31194, 31692], [17467, 18225, 18926, 19070, 19040, 19085, 18941, 18778, 18613, 18338, 18018, 17428, 17100, 16926, 17457, 17831, 17844, 17953, 18255, 18636, 18836, 18979, 19144, 19298, 19550, 19915, 20796, 21584, 21690, 21181, 21434, 22734, 24192, 24560, 24718, 24910, 24881, 25147, 25611, 26084, 26090, 25498, 26688, 26570, 26570, 27658, 28123, 28117, 28993, 29110, 29436, 30791, 33384, 36762, 39900, 39972, 40230, 40118, 39451, 41494, 45024, 47345, 48829, 46989, 45851, 44600, 44704, 45453, 45764, 45143, 44982, 43289, 46049, 46500, 47512, 49037, 49367, 49709, 50077, 50477, 50777, 51077, 51277, 51477, 51732, 52077, 52240, 52685, 52850, 53350, 53850, 54233, 54199, 53768, 53716, 53205, 53678, 53763, 53853, 54336, 54018, 53816, 54116, 54180, 54333, 54398, 54709, 54790]]
# all_new_first_city_house_price_list = [[8211, 8378, 8588, 8706, 8758, 8784, 8769, 8720, 8679, 8637, 8562, 8477, 8343, 8320, 8333, 8341, 8358, 8345, 8370, 8385, 8426, 8431, 8422, 8450, 8488, 8535, 8605, 8595, 8594, 8591, 8619, 8657, 8665, 8645, 8621, 8597, 8596, 8608, 8606, 8556, 8488, 8408, 8419, 8371, 8268, 8259, 8288, 8277, 8273, 8250, 8239, 8225, 8245, 8246, 8232, 8246, 8250, 8240, 8230, 8213, 8238, 8212, 8251, 8246, 8262, 8392, 8206, 8143, 8183, 8271, 8524, 8591, 8674, 8698, 9024, 9403, 9636, 9839, 9992, 10185, 10562, 11068, 11617, 12034, 12375, 12542, 12825, 13036, 13147, 13114, 14102, 14597, 14281, 13919, 13575, 13173, 13039, 13213, 13213, 13262, 13420, 13528, 13335, 13389, 13288, 13181, 13033, 13132], [22159, 22506, 22992, 23082, 22965, 22810, 22637, 22404, 21872, 21208, 20532, 19721, 19157, 18883, 18868, 18487, 18257, 18277, 18465, 18617, 18665, 18516, 18388, 18713, 19101, 19325, 19756, 19781, 19709, 19783, 19909, 19816, 19889, 19651, 19456, 19131, 18973, 18843, 18592, 18453, 18147, 17623, 17293, 17051, 16933, 16923, 16946, 16984, 16807, 16494, 16312, 16040, 16025, 16240, 16376, 16461, 16413, 16194, 16195, 16080, 17271, 17552, 17943, 18254, 18089, 18131, 18243, 18644, 19048, 20691, 21187, 21655, 23733, 24222, 25111, 25509, 25726, 25543, 26392, 27105, 27680, 28261, 28562, 28540, 28541, 28554, 28571, 28694, 28748, 29074, 29255, 29200, 29116, 29034, 28836, 28651, 28224, 28195, 27986, 27600, 28058, 28422, 28768, 28398, 28054, 27471, 27155, 27002], [6187, 6286, 6591, 6779, 6815, 6839, 6841, 6811, 6773, 6728, 6657, 6583, 6504, 6445, 6463, 6474, 6457, 6452, 6464, 6474, 6476, 6498, 6535, 6550, 6603, 6678, 6731, 6726, 6695, 6671, 6740, 6771, 6811, 6858, 6896, 6896, 6902, 6932, 6931, 6972, 6993, 6950, 6887, 6800, 6775, 6731, 6733, 6718, 6434, 6449, 6436, 6423, 6434, 6471, 6435, 6423, 6395, 6360, 6337, 6289, 7106, 7099, 7067, 7112, 7179, 6961, 6949, 6966, 7019, 7059, 7132, 7493, 7604, 7762, 7960, 8443, 8802, 9133, 9332, 9466, 9634, 9762, 9856, 9925, 10851, 11514, 10302, 10542, 11089, 12075, 12678, 12966, 12859, 12592, 12294, 12080, 11843, 11845, 11889, 11805, 11866, 11971, 12035, 12017, 11922, 11703, 11486, 11187], [7101, 7282, 7559, 7708, 7731, 7760, 7792, 7810, 7855, 7907, 7890, 7854, 7813, 7756, 7748, 7774, 7768, 7766, 7793, 7845, 7893, 7934, 7959, 7998, 8044, 8090, 8167, 8257, 8251, 8298, 8382, 8469, 8516, 8606, 8708, 8825, 8893, 8947, 9054, 9173, 9248, 9211, 9146, 9137, 9127, 9178, 9227, 9239, 9262, 9278, 9330, 9409, 9436, 9443, 9555, 9711, 9820, 9926, 10010, 10000, 10000, 10000, 10223, 10477, 10759, 11101, 11268, 11428, 11734, 12563, 13475, 13875, 13986, 14116, 14679, 15023, 15275, 15492, 15778, 15941, 16068, 16154, 16244, 16259, 16254, 16263, 16402, 16483, 16523, 16589, 16736, 16855, 17061, 17256, 17874, 17586, 17519, 17470, 17464, 17397, 17313, 17220, 17218, 17327, 17335, 17166, 17017, 16818], [6984, 7042, 6936, 6925, 6930, 6900, 6921, 6987, 7087, 7175, 7157, 7184, 7152, 7179, 7101, 6982, 6963, 6921, 6878, 6841, 6778, 6759, 6691, 6704, 6751, 6791, 6794, 6825, 6832, 6890, 6903, 6920, 6959, 6940, 6877, 6792, 6832, 6883, 6909, 6890, 6945, 6966, 6957, 6992, 6843, 6950, 7016, 6994, 6799, 6810, 6785, 6770, 6795, 6757, 6683, 6618, 6609, 6548, 6491, 6450, 6450, 6549, 6541, 6504, 6448, 6361, 6315, 6286, 6308, 6381, 6358, 6514, 6557, 6574, 6665, 6940, 7219, 7626, 7794, 7957, 8032, 8192, 8681, 8880, 8988, 9212, 9507, 10317, 11355, 11981, 12248, 12408, 12423, 12338, 12241, 12207, 12410, 12639, 12509, 12508, 12498, 12553, 12656, 12637, 12635, 12573, 12443, 12446], [9058, 9185, 9408, 9911, 10050, 10149, 10206, 10175, 10029, 10000, 10000, 10000, 9941, 9894, 9897, 9838, 9837, 9892, 9961, 9940, 9998, 10007, 10024, 10089, 10153, 10217, 10373, 10454, 10502, 10542, 10585, 10612, 10664, 10818, 10912, 10941, 10939, 10956, 11008, 11010, 10974, 10914, 10990, 10979, 10963, 10868, 10885, 10980, 10935, 10914, 10964, 10995, 11033, 11123, 11209, 11308, 11457, 11603, 11903, 12251, 12251, 12550, 14707, 15754, 16077, 16147, 15542, 15509, 15575, 16081, 16152, 16181, 15950, 16009, 16107, 15969, 15805, 15549, 15414, 15344, 15425, 15362, 15348, 15320, 15301, 15338, 15485, 15595, 15698, 15910, 15999, 16116, 16330, 16530, 16721, 16943, 17150, 17379, 17606, 17835, 18080, 18325, 18600, 18810, 19015, 19265, 19444, 19568], [12504, 12755, 13064, 13230, 13271, 13311, 13322, 13330, 13249, 13083, 12952, 12732, 12510, 12363, 12379, 12488, 12491, 12426, 12490, 12517, 12638, 12645, 12654, 12793, 12941, 13097, 13304, 13433, 13386, 13370, 13603, 13778, 13945, 14059, 14207, 14519, 14752, 14906, 15012, 15176, 15223, 15263, 15335, 15268, 15005, 14960, 14921, 14961, 14717, 14932, 14685, 14843, 14889, 15064, 15104, 15137, 15231, 15425, 15477, 15553, 15553, 15557, 16138, 16948, 17405, 17713, 17795, 18415, 19764, 22659, 22922, 23220, 23290, 23468, 24561, 25048, 25183, 24941, 24802, 24242, 23852, 23382, 22706, 22205, 21899, 21751, 21784, 21586, 21461, 21734, 22819, 23391, 23283, 22826, 22591, 22188, 22308, 22056, 21993, 22381, 22395, 22263, 22208, 22047, 21713, 21376, 21057, 20952], [14275, 14491, 14873, 15016, 15017, 15017, 15000, 14981, 14902, 14776, 14624, 14442, 14253, 14156, 14254, 14222, 14138, 14213, 14281, 14395, 14460, 14562, 14624, 14750, 14815, 14852, 15021, 15274, 15537, 15800, 16144, 16425, 16694, 16852, 17084, 17313, 17472, 17675, 17929, 17984, 18056, 17989, 18002, 18001, 17985, 17982, 18043, 18099, 18295, 18231, 18131, 18264, 18473, 18522, 18502, 18446, 18436, 18596, 18594, 18697, 18968, 19009, 19686, 20190, 20690, 21455, 21352, 21500, 22091, 23647, 24715, 24867, 25000, 25057, 25471, 25700, 25887, 25914, 25995, 26036, 26004, 25877, 25768, 25733, 25757, 25691, 25844, 25839, 25889, 25953, 26191, 26386, 27117, 27129, 27335, 27568, 27751, 28581, 29039, 29047, 29177, 28776, 28829, 28945, 28913, 28840, 28810, 28526], [6144, 6237, 6325, 6380, 6441, 6496, 6609, 6723, 6795, 6885, 6874, 6781, 6654, 6634, 6600, 6570, 6523, 6494, 6526, 6533, 6548, 6507, 6506, 6539, 6521, 6494, 6466, 6534, 6610, 6665, 6678, 6627, 6556, 6538, 6571, 6519, 6515, 6503, 6504, 6519, 6518, 6442, 6439, 6411, 6389, 6367, 6374, 6401, 6354, 6329, 6334, 6320, 6353, 6341, 6351, 6385, 6417, 6414, 6427, 6448, 6448, 6450, 6475, 6524, 6581, 6648, 6687, 6743, 6820, 7058, 7260, 7601, 7815, 7880, 8216, 8714, 8994, 9277, 9240, 9296, 9411, 9537, 9763, 9873, 9910, 9983, 10011, 10234, 10494, 10822, 10990, 11064, 11027, 10926, 10786, 10627, 10581, 10645, 10510, 10466, 10388, 10418, 10382, 10365, 10350, 10182, 10077, 10078], [5920, 6041, 6217, 6357, 6466, 6520, 6549, 6546, 6604, 6641, 6627, 6566, 6489, 6462, 6450, 6446, 6439, 6470, 6540, 6602, 6709, 6798, 6880, 6937, 7003, 7070, 7166, 7294, 7387, 7545, 7669, 7851, 7978, 8086, 8155, 8229, 8297, 8352, 8445, 8507, 8496, 8440, 8406, 8443, 8490, 8511, 8515, 8503, 8483, 8472, 8526, 8566, 8625, 8688, 8715, 8749, 8775, 8765, 8888, 8790, 8790, 8822, 8965, 9071, 9190, 9297, 9354, 9561, 10048, 11262, 11770, 12091, 12128, 12145, 12463, 12750, 12911, 12948, 12993, 12985, 12968, 12956, 12928, 12859, 12773, 12708, 12763, 12731, 12666, 12612, 12762, 12855, 13483, 13867, 13713, 13582, 13574, 13687, 13660, 13746, 13782, 13804, 13843, 13732, 13585, 13491, 13382, 13266], [0, 0, 0, 0, 0, 0, 6141, 6691, 7055, 6809, 6618, 6525, 6464, 6456, 6661, 6757, 6782, 6757, 6660, 6643, 6701, 6718, 6777, 6731, 6822, 6931, 7070, 7241, 7362, 7423, 7575, 7426, 7445, 7515, 7515, 7611, 7687, 7922, 7789, 7916, 8294, 8413, 8384, 8298, 7954, 7961, 7863, 7926, 8045, 8425, 8626, 8603, 8688, 8811, 8849, 8863, 8775, 8542, 8411, 8371, 8500, 8844, 9638, 10048, 9985, 9495, 9534, 9833, 10196, 11146, 11091, 11651, 11774, 11733, 11642, 12032, 12290, 13013, 12929, 12961, 13053, 13145, 13763, 13913, 13947, 14180, 14122, 14333, 14550, 14964, 15241, 15021, 15028, 15010, 14956, 14813, 15038, 15431, 15575, 15586, 15387, 15551, 15742, 15739, 15666, 15697, 15920, 16105], [15243, 15339, 14027, 13057, 12889, 13016, 13206, 13454, 13465, 13126, 12792, 12752, 12744, 12768, 12420, 12200, 12163, 12108, 11874, 11954, 11918, 12051, 11919, 11743, 11789, 12046, 12304, 12112, 12033, 12006, 12142, 12259, 12367, 12616, 12931, 12822, 12941, 13006, 12972, 12852, 12792, 12756, 12284, 12280, 12411, 12190, 12024, 12286, 12290, 12412, 12333, 12015, 12342, 12397, 12425, 12509, 12368, 12556, 12374, 12384, 12525, 12536, 12700, 12527, 12447, 12349, 12346, 12379, 12432, 13034, 13380, 13523, 13940, 14273, 15759, 17033, 16991, 17073, 17217, 17352, 17559, 17724, 17925, 18142, 18564, 19169, 19947, 20697, 20898, 20480, 20338, 20992, 20696, 20128, 19632, 18788, 18375, 18386, 18352, 18204, 18045, 18040, 17617, 17389, 17049, 16808, 16521, 16340], [0, 0, 0, 8674, 7625, 7581, 7872, 7943, 7938, 7991, 8071, 8105, 8129, 8158, 8215, 8210, 8131, 8062, 8112, 8098, 8060, 8043, 8064, 8030, 8057, 8086, 8145, 8193, 8168, 8149, 8137, 8169, 8256, 8265, 8314, 8270, 8274, 8257, 8245, 8242, 8345, 8325, 8289, 8272, 8290, 8167, 8031, 7991, 7486, 7427, 7439, 7420, 7458, 7514, 7434, 7495, 7459, 7333, 7198, 7242, 7242, 7271, 7410, 7366, 7318, 7247, 7234, 7223, 7230, 7293, 7177, 7242, 7274, 7351, 7367, 7428, 7493, 7635, 7588, 7572, 7623, 7704, 7972, 7999, 8013, 8026, 8141, 8190, 8303, 8470, 8597, 8786, 8898, 8990, 9017, 9005, 9049, 9169, 9176, 9285, 9384, 9427, 9511, 9588, 9634, 9715, 9763, 9817], [0, 0, 0, 0, 15503, 15628, 16301, 16268, 16277, 16227, 15706, 15458, 15288, 15228, 15277, 15063, 14996, 14975, 15366, 15587, 15531, 15363, 15337, 15342, 15322, 15512, 15441, 15554, 15600, 15674, 15841, 15700, 15636, 15690, 15536, 15461, 15335, 15114, 15049, 14829, 15026, 14904, 14332, 14346, 14498, 14592, 14332, 14350, 12569, 12320, 12299, 12171, 12209, 12063, 11855, 11694, 12093, 12150, 12273, 12250, 12250, 12274, 12352, 12698, 12508, 12956, 13069, 13082, 13116, 13321, 13509, 13857, 14018, 14229, 14595, 15023, 15316, 15705, 16102, 16418, 16377, 16309, 16714, 17037, 17137, 17444, 17723, 18196, 18773, 19600, 20091, 20436, 20438, 20528, 20445, 20313, 20245, 20386, 20599, 20787, 20857, 21059, 21480, 21828, 22090, 22294, 22454, 22814], [0, 0, 0, 0, 8671, 8655, 8788, 9104, 9109, 9060, 8962, 8842, 8758, 8671, 8496, 8381, 8363, 8326, 8368, 8453, 8487, 8501, 8533, 8567, 8630, 8666, 8657, 8672, 8589, 8601, 8593, 8645, 8670, 8649, 8666, 8664, 8682, 8675, 8660, 8581, 8572, 8513, 8499, 8394, 8347, 8198, 8129, 8094, 8002, 7982, 7911, 7989, 8036, 8022, 8048, 8094, 8178, 8232, 8051, 8202, 8202, 8205, 8234, 8344, 8415, 8391, 8410, 8396, 8429, 8407, 8445, 8485, 8469, 8551, 8643, 8732, 8841, 9014, 9116, 9289, 9461, 9564, 9659, 9771, 9914, 10000, 10117, 10401, 10705, 11018, 11382, 11735, 11936, 12166, 12336, 12298, 12285, 12261, 12304, 12328, 12342, 12471, 12611, 12697, 12839, 12896, 12983, 13117]]


# 通过pyecharts画图
# 强制设定x、y轴间隔无效
# 参考：https://blog.csdn.net/miner_zhu/article/details/81949004
# from pyecharts import Line
# line = Line("4个一线城市2011-2019房价均价", '2020-01-17', width=10000, height=1200)
# line.add("北京", year_month_list, all_first_city_house_price_list[0], is_label_show = True, is_smooth=True, xaxis_rotate=90, yaxis_min=15000, yaxis_max=65000)
# line.add("上海", year_month_list, all_first_city_house_price_list[1], is_label_show = True, is_smooth=True, xaxis_rotate=90, yaxis_min=15000, yaxis_max=65000)
# line.add("广州", year_month_list, all_first_city_house_price_list[2], is_label_show = True, is_smooth=True, xaxis_rotate=90, yaxis_min=15000, yaxis_max=65000)
# line.add("深圳", year_month_list, all_first_city_house_price_list[3], is_label_show = True, is_smooth=True, xaxis_rotate=90, yaxis_min=15000, yaxis_max=65000)
# line.show_config()
# line.render()
# new_line = Line("15个新一线城市2011-2019房价均价", '2020-01-18', width=3000, height=1200)
# print(len(new_first_city_chinese_list))
# print(len(year_month_list))
# print(len(all_new_first_city_house_price_list))
# for i in range(len(new_first_city_chinese_list)):
#     new_line.add(new_first_city_chinese_list[i], year_month_list, all_new_first_city_house_price_list[i], is_label_show=True, is_smooth=True, xaxis_rotate=90)
# new_line.show_config()
# new_line.render("new_first_city_house_prices.html")


# # 通过matplotlib画图
# # 待优化：图片太小，横坐标显示不下
# import matplotlib.pyplot as plt
# plt.title('一线城市2015-2019年每月房价均价')
# plt.plot(year_month_list, all_first_city_house_price_list[0], marker='o', mec='r', mfc='w',label='beijing')
# plt.plot(year_month_list, all_first_city_house_price_list[1], marker='*', mec='r', mfc='w',label='shanghai')
# plt.plot(year_month_list, all_first_city_house_price_list[2], marker='o', mec='r', mfc='w',label='guangzhou')
# plt.plot(year_month_list, all_first_city_house_price_list[3], marker='*', mec='r', mfc='w',label='shenzhen')
# plt.legend()
# plt.xlabel("城市名")
# plt.ylabel("房价/元")
# plt.show()



# 写入Excel
import xlwt

def write_excel(excel_name, city_chinese_list, year_month_list, all_city_house_price_list):
    book = xlwt.Workbook() # 新建一个Excel
    sheet = book.add_sheet('sheet1') # 添加一个sheet页
    year_row = 1
    year_col = 0
    for i in year_month_list:
        sheet.write(year_row, year_col, i)
        year_row = year_row + 1
    city_row = 0
    city_col = 1
    for i in city_chinese_list:
        sheet.write(city_row, city_col, i)
        city_col = city_col + 1

    price_col = 1
    for i in all_city_house_price_list:
        price_row = 1
        for j in i:
            sheet.write(price_row, price_col, j)
            price_row = price_row + 1
        price_col = price_col + 1
    book.save(excel_name)

write_excel("first_city_house_prices_2011-2019.xls", first_city_chinese_list, year_month_list, all_first_city_house_price_list)
write_excel("new_first_city_house_prices_2011-2019.xls", new_first_city_chinese_list, year_month_list, all_new_first_city_house_price_list)

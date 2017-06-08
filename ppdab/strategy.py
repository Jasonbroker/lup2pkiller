# LoanInfo
''''
<Amount>14000.0000</Amount>
<CreditCode>B</CreditCode>
<ListingId>48268108</ListingId>
<Months>12</Months>
<PayWay>0</PayWay>
<Rate>18</Rate>
<Title>pdu8****73867\xe7\x9a\x84\xe7\xac\xac1\xe6\xac\xa1\xe5\x80\x9f\xe6\xac\xbe</Title>

策略依据：
https://mp.weixin.qq.com/s?__biz=MzA3MDk4MjE3MA==&mid=402198262&idx=
1&sn=117af8e67fadc9b36e399ee473511eaf&scene=1&srcid=0104njKHlNasq1wuD
aY7JYP8&key=41ecb04b05111003f4f6dfe51191e926f5bbaa1259f7bc4590fb16
0fa4553943538e07460fa8e350550195fc48b51bb8&ascene=1&uin=MTIzODg0NDEwOA
==&devicetype=Windows-QQBrowser&version=61030003&pass_ticket=/xx+Eg+G3
+WP6J71NNkAaUAF8uU11xqfrIMT1BydAuWfgFgc8mzP4nvlrn01HZ0S


'''


# 投标策略

# 1. 最稳策略
'''
直投赔标 12% 年化
这种策略需要分配一定比例，如果追求高收益，不能配置超过50% 否则很难做到平衡最高收益
'''

'''
综合 16% - 20% 年化
这种策略需要分配一定比例，如果追求高收益，不能配置超过50% 否则很难做到平衡最高收益
根据用户群划分。对我们而言abcd 没有太大意义。

策略分为两类：
1. 是非型：是就是，不是就不是，造成绝对性影响。比如性别，规定了是女的就是女的。
2. 
根据筛选出来的初步条件，给予当前用户评分。
高评分的用户可以提前交易，或者提升交易的数额

'''

class Strategy:

    STRATEGY_SAFE_AA = 1
    STRATEGY_BEST_GAIN_16 = 2
    STRATEGY_FEMALE_16 = 3

    MALE = 10       # 男的
    FEMALE = 11     # 女的
    SEXANY = 12     # 任意性别

    CreditCodeA = 17
    CreditCodeB = 18
    CreditCodeC = 19
    CreditCodeD = 20

    def __init__(self, strategy):
        self.phone_validate = 1  # 必须手机认证了，不然说毛线？
        if strategy == Strategy.STRATEGY_SAFE_AA:
            self.max_amount = 10000
            self.sex = Strategy.SEXANY
            self.credit = Strategy.CreditCodeA
        elif strategy == Strategy.STRATEGY_BEST_GAIN_16:
            self.max_amount = 6000
            self.min_amount = 1000
            self.gender = Strategy.FEMALE
            self.credit = Strategy.CreditCodeC
            self.age_from = 18
            self.age_to = 21
            self.mini_rate = 16  # 最小利率
            self.max_fail_count = 2  # 最多流标次数
            self.max_owning = 8000  # 最大待还，如果待还数目太多该人风险太高了
            self.certificate_validate = 0  # 是否需要学历认证
            self.credit_validate = 0  # 征信认证，如果有征信认证，得分相应提升
            self.educate_validate = 0 # 学籍认证
            self.min_last_borrow_interval = 10  # 最小时间间隔，太频繁不好。
            self.min_month = 6  # 最小借几个月
            self.max_month = 12  # 最多借几个月
            self.max_normal_count = 100000000
            self.min_normal_count = 0
            self.max_overdue_less_count = 3  # 最大15天以内逾期
            self.max_overdue_more_count = 0  # 最大15天以上逾期
            self.min_success_count = 0
            self.max_success_count = 20
            self.max_wast_count = 5         # 流标次数不能超过5次







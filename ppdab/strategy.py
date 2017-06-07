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

<Age>23</Age>
<Amount>5250.0000</Amount>
<AmountToReceive>0</AmountToReceive>
<AuditingTime>2017-05-21T15:11:04.25</AuditingTime>  // 成交日期
<BorrowName>pdu7614660027</BorrowName>   // 借款人的用户名
<CancelCount>1</CancelCount>  // 撤标次数
<CertificateValidate>1</CertificateValidate>  学历认证
<CreditCode>B</CreditCode>
<CreditValidate>0</CreditValidate>  // 征信认证
<CurrentRate>18</CurrentRate>
<DeadLineTimeOrRemindTimeStr>2017/5/21</DeadLineTimeOrRemindTimeStr>
<EducateValidate>0</EducateValidate>  学籍认证
<EducationDegree>\xe4\xb8\x93\xe7\xa7\x91</EducationDegree> 学历
<FailedCount>0</FailedCount> liubao
<FirstSuccessBorrowTime>2016-07-06T09:40:56.263</FirstSuccessBorrowTime> // 第一次成功借款
<FistBidTime>2017-05-20T13:42:14.447</FistBidTime>
<Gender>2</Gender>  性别	1 男 2 女 0 未知
<GraduateSchool>\xe4\xb8\xad\xe5\x8d\x97\xe5\xa4\xa7\xe5\xad\xa6</GraduateSchool>
<HighestDebt>17052.7200</HighestDebt>  历史最高负债
<HighestPrincipal>8000.0000</HighestPrincipal>
<LastBidTime>2017-05-21T15:11:03.83</LastBidTime>
<LastSuccessBorrowTime>2017-05-20T13:11:37</LastSuccessBorrowTime>
<LenderCount>64</LenderCount>
<ListingId>48209704</ListingId>
<Months>12</Months>
<NciicIdentityCheck>0</NciicIdentityCheck>  户籍认证
<NormalCount>16</NormalCount>正常还清次数
<OverdueLessCount>3</OverdueLessCount> 逾期(1-15)还清次数
<OverdueMoreCount>0</OverdueMoreCount> 逾期(15天以上)还清次数
<OwingAmount>15909.1500</OwingAmount>  待还金额
<OwingPrincipal>14861.6600</OwingPrincipal>  剩余待还本金
<PhoneValidate>1</PhoneValidate>
<RegisterTime>2016-07-06T07:38:11</RegisterTime>
<RemainFunding>0.0000</RemainFunding> 剩余可投
<StudyStyle>\xe6\x88\x90\xe4\xba\xba</StudyStyle><SuccessCount>5</SuccessCount><TotalPrincipal>25200.0000</TotalPrincipal><VideoValidate>0</VideoValidate><WasteCount>0</WasteCount></LLoanInfoDetail>
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
        if strategy == Strategy.STRATEGY_SAFE_AA:
            self.max_amount = 10000
            self.sex = Strategy.SEXANY
            self.credit = Strategy.CreditCodeA
        elif strategy == Strategy.STRATEGY_BEST_GAIN_16:
            self.max_amount = 6000
            self.min_amount = 1000
            self.sex = Strategy.FEMALE
            self.credit = Strategy.CreditCodeC
            self.age_from = 18
            self.age_to = 21
            self.mini_rate = 16  # 最小利率


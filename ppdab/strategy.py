# LoanInfo
'''
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

FistBidTime DateTime 首次投资时间
LastBidTime DateTime 末笔投资时间
LenderCount Int 投标人数
AuditingTime DateTime 成交日期
RemainFunding Decimal 剩余可投金额
DeadLineTimeOrRemindTimeStr String 2016/11/19或者14天15时57分(剩余时间)截止时间
CreditCode String 标的等级
ListingId Int 列表编号
Amount Decimal 借款金额
Months Int 期限
CurrentRate Double 利率
BorrowName String 借款人的用户名
Gender Int 性别	1 男 2 女 0 未知
EducationDegree String 学历
GraduateSchool String 毕业院校
StudyStyle String 学习形式
Age Int 年龄
SuccessCount Int 成功借款次数
WasteCount Int 流标次数
CancelCount Int 撤标次数
FailedCount Int 失败次数
NormalCount Int 正常还清次数
OverdueLessCount Int 逾期(1-15)还清次数
OverdueMoreCount Int 逾期(15天以上)还清次数
OwingPrincipal Decimal 剩余待还本金
OwingAmount Decimal 待还金额
AmountToReceive Decimal 待收金额
FirstSuccessBorrowTime DateTime 第一次成功借款时间
RegisterTime DateTime 注册时间
CertificateValidate Int 学历认证	0 未认证 1已认证
NciicIdentityCheck Int 户籍认证	0 未认证 1已认证
PhoneValidate Int 手机认证	0 未认证 1已认证
VideoValidate Int 视屏认证	0 未认证 1已认证
CreditValidate Int 征信认证	0 未认证 1已认证
EducateValidate Int 学籍认证	0 未认证 1已认证
LastSuccessBorrowTime DateTime 最后一次成功借款时间
HighestPrincipal Decimal 500.00单笔最高借款金额
HighestDebt Decimal 500.00历史最高负债
TotalPrincipal Decimal 500.00累计借款金额
 示例：
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
<StudyStyle>\xe6\x88\x90\xe4\xba\xba</StudyStyle> 学习形式
<SuccessCount>5</SuccessCount>
<TotalPrincipal>25200.0000</TotalPrincipal>
<VideoValidate>0</VideoValidate>
<WasteCount>0</WasteCount>

'''
# todo 根据官方论坛的大数据分析写策略
class Strategy:

    STRATEGY_SAFE_AA = 1
    STRATEGY_BEST_GAIN_16 = 2
    STRATEGY_FEMALE_16 = 3

    CreditCodeA = 'A'
    CreditCodeB = 'B'
    CreditCodeC = 'C'
    CreditCodeD = 'D'

    def __init__(self, strategy):
        self.phone_validate = 1  # 必须手机认证了，不然说毛线？
        if strategy == Strategy.STRATEGY_SAFE_AA:
            self.max_amount = 10000
            self.sex = 0
            self.credit = Strategy.CreditCodeA
        elif strategy == Strategy.STRATEGY_BEST_GAIN_16:
            self.max_amount = 6000
            self.min_amount = 1000
            self.gender = 2
            self.credit = Strategy.CreditCodeC
            self.age_from = 18
            self.age_to = 28
            self.mini_rate = 16  # 最小利率
            self.max_owning = 8000  # 最大待还，如果待还数目太多该人风险太高了
            self.certificate_validate = 0  # 是否需要学历认证
            self.credit_validate = 0  # 征信认证，如果有征信认证，得分相应提升
            self.educate_validate = 0  # 学籍认证
            self.nciic_identity = 0  # 户籍认证
            self.min_last_borrow_interval = 10  # 最小时间间隔，太频繁不好。
            self.min_month = 6  # 最小借几个月
            self.max_month = 12  # 最多借几个月
            self.max_normal_count = 30
            self.min_normal_count = 0
            self.max_overdue_less_count = 3  # 最大15天以内逾期
            self.max_overdue_more_count = 0  # 最大15天以上逾期
            self.min_success_count = 0
            self.max_success_count = 20
            self.max_wast_count = 3         # 流标次数不能超过5次







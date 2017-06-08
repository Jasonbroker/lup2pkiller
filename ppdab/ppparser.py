import xml

'''
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

class PPParser:

    @staticmethod
    def parse_bid_detail_list(xml_string, strategy):
        dom = xml.dom.minidom.parseString(xml_string)
        root = dom.documentElement

        loan_infos = root.getElementsByTagName("LoanInfos")[0]

        filtered_elements = []
        for element in loan_infos.childNodes:
            # 剩余可借
            remain = element.getElementsByTagName('RemainFunding')[0].childNodes[0].nodeValue
            if float(remain) <= 0:
                continue
            # 看欠钱是不是太多
            own_amount = element.getElementsByTagName('OwingAmount')[0].childNodes[0].nodeValue
            if float(own_amount) > strategy.max_owning:
                continue
            # 要求性别
            gender = element.getElementsByTagName('Gender')[0].childNodes[0].nodeValue
            gender = int(gender)
            if gender != strategy.gender:
                continue
            # 年龄要求
            age = element.getElementsByTagName('Age')[0].childNodes[0].nodeValue
            age = int(age)
            if age > strategy.age_to or age < strategy.age_from:
                continue
            # fail count
            






            # 借款数
            amount = element.getElementsByTagName('Amount')[0].childNodes[0].nodeValue
            print('借款数：' + amount)
            amount = float(amount)
            if amount > strategy.max_amount or amount < strategy.min_amount:
                print('价格不合适')
                continue

            listingId = element.getElementsByTagName('ListingId')[0].childNodes[0].nodeValue
            filtered_elements.append(listingId)
        return filtered_elements

    '''
    返回需要继续取得详情的列表
    '''
    @staticmethod
    def parse_bid_list(xml_string, strategy):

        dom = xml.dom.minidom.parseString(xml_string)
        root = dom.documentElement

        loan_infos = root.getElementsByTagName("LoanInfos")[0]

        filteredElements = []
        for element in loan_infos.childNodes:
            # 借款数
            amount = element.getElementsByTagName('Amount')[0].childNodes[0].nodeValue
            print('借款数：' + amount)
            amount = float(amount)
            if amount > strategy.max_amount or amount < strategy.min_amount:
                print('太贵')
                continue

            listingId = element.getElementsByTagName('ListingId')[0].childNodes[0].nodeValue
            filteredElements.append(listingId)
            if len(filteredElements) == 10:
                break
        return filteredElements

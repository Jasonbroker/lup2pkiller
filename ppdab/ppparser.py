import xml

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
            # 流标次数
            wastcount = element.getElementsByTagName('WasteCount')[0].childNodes[0].nodeValue
            wastcount = int(wastcount)
            failcount = int(element.getElementsByTagName('FailedCount')[0].childNodes[0].nodeValue)
            if wastcount > strategy.max_wast_count or failcount > strategy.max_wast_count:
                continue
            # 正常还款期数
            normalcount = element.getElementsByTagName('NormalCount')[0].childNodes[0].nodeValue
            normalcount = int(normalcount)
            if normalcount > strategy.max_normal_count:
                continue
            # 借款数
            amount = element.getElementsByTagName('Amount')[0].childNodes[0].nodeValue
            print('借款数：' + amount)
            amount = float(amount)
            if amount > strategy.max_amount or amount < strategy.min_amount:
                print('价格不合适')
                continue
            # PhoneValidate 手机验证
            # 至少是个手机验证吧？连个手机验证都没有玩啥？
            phoneValidate = element.getElementsByTagName('PhoneValidate')[0].childNodes[0].nodeValue
            phoneValidate = int(phoneValidate)
            if phoneValidate != 1:
                continue

            # 学历认证
            certificateValidate = element.getElementsByTagName('CertificateValidate')[0].childNodes[0].nodeValue
            certificateValidate = int(certificateValidate)

            # 学籍认证
            nciicIdentityCheck = element.getElementsByTagName('NciicIdentityCheck')[0].childNodes[0].nodeValue
            nciicIdentityCheck = int(nciicIdentityCheck)
            # 征信认证
            certificateValidate = element.getElementsByTagName('CertificateValidate')[0].childNodes[0].nodeValue
            certificateValidate = int(certificateValidate)
            # 15天以内逾期

            # 15天以上逾期

            # 最还款次数












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

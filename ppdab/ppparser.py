import xml

class PPParser:
    debug = True
    @staticmethod
    def debug_print(words):
        if PPParser.debug:
            print(words)

    @staticmethod
    def parse_bid_detail_list(xml_string, strategy, list):
        dom = xml.dom.minidom.parseString(xml_string)
        root = dom.documentElement

        loan_infos = root.getElementsByTagName("LoanInfos")[0]

        for element in loan_infos.childNodes:
            # 剩余可借
            remain = element.getElementsByTagName('RemainFunding')[0].childNodes[0].nodeValue
            if float(remain) <= 0:
                PPParser.debug_print('remain insuficient: ' + remain)
                continue
            # 看欠钱是不是太多
            own_amount = element.getElementsByTagName('OwingAmount')[0].childNodes[0].nodeValue
            if float(own_amount) > strategy.max_owning:
                PPParser.debug_print('own_amount too much: ' + own_amount)
                continue
            # 要求性别
            gender = element.getElementsByTagName('Gender')[0].childNodes[0].nodeValue
            gender = int(gender)
            if gender != strategy.gender:
                PPParser.debug_print('gender wrong %d' % gender)
                continue
            # 年龄要求
            age = element.getElementsByTagName('Age')[0].childNodes[0].nodeValue
            age = int(age)
            if age > strategy.age_to or age < strategy.age_from:
                PPParser.debug_print('age not right: %d' % age)
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
            # 至少是个手机验证。
            phoneValidate = element.getElementsByTagName('PhoneValidate')[0].childNodes[0].nodeValue
            phoneValidate = int(phoneValidate)
            if phoneValidate != 1:
                continue

            # 15天以上逾期
            overdue_more_count = element.getElementsByTagName('OverdueMoreCount')[0].childNodes[0].nodeValue
            overdue_more_count = int(overdue_more_count)
            if overdue_more_count > strategy.max_overdue_more_count:
                continue
            # 15天以内逾期
            overdue_less_count = element.getElementsByTagName('OverdueLessCount')[0].childNodes[0].nodeValue

            overdue_less_count = int(overdue_less_count)
            if overdue_less_count > strategy.max_overdue_less_count:
                continue

            # 学历认证
            certificateValidate = element.getElementsByTagName('CertificateValidate')[0].childNodes[0].nodeValue
            certificateValidate = int(certificateValidate)
            if certificateValidate != strategy.certificate_validate:
                continue
            # 学籍认证
            educate_validate = element.getElementsByTagName('EducateValidate')[0].childNodes[0].nodeValue
            educate_validate = int(educate_validate)
            if educate_validate != strategy.educate_validate:
                continue
            # 征信认证
            creditvalidate = element.getElementsByTagName('CreditValidate')[0].childNodes[0].nodeValue
            creditvalidate = int(creditvalidate)
            if creditvalidate != strategy.credit_validate:
                continue
            # 户籍认证
            nciic_identity = element.getElementsByTagName('CreditValidate')[0].childNodes[0].nodeValue
            nciic_identity = int(nciic_identity)
            if nciic_identity != strategy.nciic_identity:
                continue

            # 最还款次数
            # 征信认证
            creditvalidate = element.getElementsByTagName('CreditValidate')[0].childNodes[0].nodeValue
            creditvalidate = int(creditvalidate)
            if creditvalidate != strategy.credit_validate:
                continue

            # 自考，本科，大专，研究生，博士
            education_degrees = element.getElementsByTagName('EducationDegree')[0].childNodes
            if len(education_degrees) > 0:
                print(education_degrees)
                education_degree = education_degrees[0].nodeValue
                print(education_degree)


            # 毕业院校，有些学校可能需要排除掉
            graduate_schools = element.getElementsByTagName('GraduateSchool')[0].childNodes
            if len(graduate_schools) > 0:
                graduate_school = graduate_schools.nodeValue
                print(graduate_school)

            # 教育形式是自考的需要排除掉


            listingId = element.getElementsByTagName('ListingId')[0].childNodes[0].nodeValue
            list.append(listingId)

            print('通过评分系统：\n', element.toxml())
        return list

    '''
    返回需要继续取得详情的列表
    '''
    @staticmethod
    def parse_bid_list(json, strategy):

        loan_infos = json["LoanInfos"]
        # 用来筛选的
        filteredElements = []
        for element in loan_infos:
            creditCode = element['CreditCode']
            if creditCode > strategy.credit:
                PPParser.debug_print('low credit: ' + creditCode)
                continue
            # 借款数
            amount = element.getElementsByTagName('Amount')[0].childNodes[0].nodeValue
            amount = float(amount)
            if amount > strategy.max_amount or amount < strategy.min_amount:
                print('借款数', amount)
                continue
            rate = element.getElementsByTagName('Rate')[0].childNodes[0].nodeValue

            if float(rate) < strategy.mini_rate:
                print('low rate', rate)
                continue
            listingId = element.getElementsByTagName('ListingId')[0].childNodes[0].nodeValue
            filteredElements.append(listingId)
        print('ratial = ', len(filteredElements), len(loan_infos.childNodes))
        return filteredElements


    @staticmethod
    def parse_AA_bid_list(json, level):

        loan_infos = json["LoanInfos"]
        # 用来筛选的
        filteredElements = []
        filteredHigh = []
        filteredHighest = []

        if level == 1:
            for element in loan_infos:
                creditCode = element['CreditCode']
                if creditCode != 'AA':
                    continue
                rate = element['Rate']
                listingId = element['ListingId']
                if rate >= 14:
                    filteredHighest.append(listingId)
        elif level == 2:
            for element in loan_infos:
                creditCode = element['CreditCode']
                if creditCode != 'AA':
                    continue
                rate = element['Rate']
                if rate < 12.5:
                    continue
                month = element['Months']

                listingId = element['ListingId']
                filteredHigh.append(listingId)
        else:
            for element in loan_infos:
                creditCode = element['CreditCode']
                if creditCode != 'AA':
                    continue
                rate = element['Rate']
                if rate < 12:
                    continue
                month = element['Months']
                if rate < 12.5 and month > 12:
                    continue
                listingId = element['ListingId']
                if rate >= 14:
                    filteredHighest.append(listingId)
                elif rate == 12:
                    filteredElements.append(listingId)
                else:
                    filteredHigh.append(listingId)

        return filteredHighest, filteredHigh, filteredElements

    @staticmethod
    def parse_AA_12d5(json):
        pass
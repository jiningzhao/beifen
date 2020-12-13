import xlrd
# import xlwt
import xlsxwriter
import json
from .interfaceSpider import InterfaceSpider


# 导入需要读取Excel表格的路径
class ReadDoc:
    """
    readdoc()读取Excel表格文件
    writedoc()写入Excel表格文件
    """

    def __init__(self, path):
        self.path = path

        # self.readdoc()

    def readdoc(self):
        data = xlrd.open_workbook(f'demo/{self.path}.xlsx')
        table = data.sheet_by_name(self.path)
        cases = []
        for i in range(1, table.nrows):
            case = {}
            for j in range(5):
                if j == 0:
                    case['detail'] = str(table.cell_value(i, j))
                elif j == 1:
                    case['name'] = str(table.cell_value(i, j))
                elif j == 2:
                    case['data'] = json.loads(table.cell_value(i, j).replace("'", '"'))
                elif j == 3:
                    case['method'] = str(table.cell_value(i, j))
                elif j == 4:
                    case['path'] = str(table.cell_value(i, j))
            if case.get("detail") is not None:
                cases.append(case)
        print(cases)
        return cases

    def writedoc(self):
        workbook = xlsxwriter.Workbook(f'{self.path}.xlsx')
        sheet1 = workbook.add_worksheet(self.path)
        # sheet1 = f.add_worksheet()
        row0 = ["detail", "name", "data", "method", "path"]
        # 写第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        """
        调用爬虫模块，将爬取到的信息写入Excel表格
        interfaceList=[{"detail":"","name":"","data":{}},...]
        """
        interfaceList = InterfaceSpider(self.path).spider()
        for j in range(0, len(interfaceList)):
            sheet1.write(j + 1, 0, interfaceList[j]['detail'])
            sheet1.write(j + 1, 1, interfaceList[j]['name'])
            sheet1.write_string(j + 1, 2, str(interfaceList[j]['data']))
            sheet1.write(j + 1, 3, 'post')
            sheet1.write(j + 1, 4, f"/{self.path}/api")
        workbook.close()

# ReadDoc('passport').writedoc()
# print(ReadDoc('passport').readdoc())

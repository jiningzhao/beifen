import xlrd
import json


# 导入需要读取Excel表格的路径
class ReadDoc:

    def __init__(self):
        data = xlrd.open_workbook(r'test.xlsx')
        self.table = data.sheets()[0]
        self.readdoc()

    def readdoc(self):
        cases = []
        for i in range(self.table.nrows):
            case = {}
            for j in range(5):
                if j == 0:
                    case['no'] = int(self.table.cell_value(i, j))
                elif j == 1:
                    case['name'] = str(self.table.cell_value(i, j))
                elif j == 2:
                    case['data'] = json.loads(self.table.cell_value(i, j))
                elif j == 3:
                    case['method'] = str(self.table.cell_value(i, j))
                elif j == 4:
                    case['path'] = str(self.table.cell_value(i, j))
            cases.append(case)
        return cases

class Pagination():
    def __init__(self,totalCount,currentPage,perPageNum=None,allPageNum=None):
        self.totalCount=int(totalCount)  #数据总个数 total_count

        try:  #前端传入错误
             self.currentPage=int(currentPage )#当前页是那页
        except Exception as e:
            self.currentPage=1  #可以根据这个值去做判断返回错误信息给前端
        self.currentPageNum=int(perPageNum)  #每页后台返回的数据条数
        self.maxPageNum=int(allPageNum)   #最多显示页面数量


    def start(self): #根据当前页取出 列表的索引起始值
        return (self.currentPage-1)*self.currentPageNum


    def  end(self): #根据当前页取出 列表的索引终止值
        return self.currentPage * self.currentPageNum


    def all_page(self):   #计算并返回 当前数据所需要总页数

        a,b=divmod(self.totalCount,self.currentPageNum)
        if b == 0:
            return a
        return a + 1





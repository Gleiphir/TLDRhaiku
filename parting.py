


"""
5-> [ [1,1,1,1,1],
[2,1,1,1]
[2,2,1]
[3,1,1]
[3,2]
[4,1]
[5]
]
"""

def getTable(n):
    L =[]
    def partition(n, startnum, out=()):
        # 递归，从 startnum ,到 n/2 取整 ，range()特性 +1
        # 用 out字符串 来存储前面的数字，outmp是当前式子用的，输出即弃用
        for i in range(startnum, n // 2 + 1):
            outmp = list(out)
            outmp.append(i)
            partition(n - i, i, outmp)

        # 退出条件就是 startnum == n,把前面的 out字符串 输出，然后 n 直接输出在末尾就行
        # 判断是否换行，最后一个没有';'，用是否包含 '+' 取了巧规避了
        # 由于这是最后一位数，所以也能控制 '+' 不会添加在末尾
        if n == startnum:
            O = list(out)
            O.append(n)
            #print(O)
            L.append(O.copy())
            return


        # 最后当然还要输出一个前面没有加和的整数
        # if startnum < n:
        partition(n, n, out)
    partition(n, 1, ())
    return L

if __name__ =='__main__':
    n = int(input())
    print(getTable(n))
import numpy as np
import copy
# 计算价值
def Value(origin,last):
    #深度递归搜索函数，找到一个0的分配方案，让每行每列仅选出一个0
    #找出合适的0元素的位置
    #按行记录每行哪些列是0元素
    pos = []
    m=len(last)
    for i in range(m):
        # [[0, 1, 3], [0, 3, 4], [2, 4], [2, 3], [0, 1, 3]]
        pos.append(list(np.argwhere(last[i,:]==0).squeeze(1)))
    def search(layer,path):
        if len(path) == m:
            return path
        else:
            for i in pos[layer]:
                if i not in path:
                    newpath = copy.deepcopy(path)
                    newpath.append(i)
                    ans = search(layer+1,newpath)
                    if ans is not None:
                        return ans
            return None
    #调用深度递归搜索  
    path = search(0,[])
    value=0
    for i in list(zip(range(m),path)):
        value+=origin[i[0]][i[1]]
    return value
# 找到最小
def find_min(matrix,row,col):
    min_list=[]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if((i not in row) and  (j not in col)):
                min_list.append(matrix[i][j])
    if(len(min_list)!=0):
        min_num=min(min_list)
    else:
        return 0
    return min_num
# 消费矩阵
def Compute_uncovered(matrix,row,col):
    # row 或者 col 表示覆盖的横线和竖线
    # min_j是非覆盖的最小值
    # 处于线交叉点，加非覆盖的最小值
    # 处于没有被划线的地方，减非覆盖的最小值
    # print(matrix)
    min_j=find_min(matrix,row,col)
    if(min_j==0):
        return matrix
    # 未覆盖
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if((i not in row) and  (j not in col)):
                matrix[i][j]-=min_j
    # 全覆盖
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if((i in row) and (j in col)):
                matrix[i][j]+=min_j
    # 其他情况不变
    # 返回矩阵
    return matrix
def Hungary(matrix):
    # 第一步，每行减去列最小值
    matrix=matrix-matrix.min(axis=1).reshape(-1,1)
    # 第二步，每列减去列最小值
    matrix=matrix-matrix.min(axis=0).reshape(1,-1)
    # 第三步，找到最少的线，能将所有的0囊括
    Visited_row=[]
    Visited_col=[]
    line=0
    value=0
    # 阶
    n=len(matrix)
    while(n!=line):
        value=0
        line=0
        Visited_row=[]
        Visited_col=[]
        # 先行后列，找到更多的点就在该行或者列加一条线。
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                # 找到0，然后存入已经有的行之中，并且判断是否访问过
                if(matrix[i][j]==0 and (i not in Visited_row) and (j not in Visited_col)):
                    # 先行
                    row_zero=0
                    for z in range(len(matrix[i])):
                        if(matrix[i][z]==0):
                            row_zero+=1
                    # 后列
                    col_zero=0
                    for zz in range(len(matrix)):
                        if(matrix[zz][j]==0):
                            col_zero+=1
                    # 比较，选多得加一条线，并且保存到Visited判断
                    # 先行后列
                    if(row_zero>=col_zero):
                        line+=1
                        Visited_row.append(i)
                    elif(row_zero<col_zero):
                        line+=1
                        Visited_col.append(j)
                else:
                    continue
        # 计算消防矩阵
        matrix=Compute_uncovered(matrix,Visited_row,Visited_col)
    return matrix
matrix = np.array(
    [[16,14,18,17,20],
    [14,13,16,15,17],
    [18,16,17,19,20],
    [19,17,15,16,19],
    [17,15,19,18,21],]
)
print("origin")
print(matrix)
print("res:")
matrix_=Hungary(matrix)
print(matrix_)
print("value:")
# 原始矩阵
origin=matrix
# 经过匈牙利算法后的矩阵
last=matrix_
print(Value(origin,last))

table = [
                # 2
                [36, [1,1,35], "2"],
                # 3
                [36, [1,18,35], "3a"],
                [36, [18,18,1], "3b"],
                # 4
                [36, [1,2,34],"4"],
                # 5
                [36, [1,18,34],"5a"],
                [36, [17,18,2], "5b"],
                # 6
                [27, [9,1,26], "6a"],
                [27, [9,8,19], "6b"],
                # 7
                [6, [2,3,5], "7a"],
                [6, [4,3,1], "7b"],
                # 8
                [12, [8,4,9], "8a"],
                [12, [4,6,11], "8b"],
                [12, [8,6,7], "8c"],
                [12, [9,6,1], "8d"],
                [12, [9,6,5], "8e"],
                # 9
                [12, [8,8,1], "9a"],
                [12, [8,6,3], "9b"],
                [12, [5,6,9], "9c"],
                # 10
                [18, [11,6,14],"10a"],
                [18, [6,9,16],"10b"],
                [18, [13,9,2],"10c"],
                # 11
                [36, [1,3,33],"11"],
                # 12
                [8, [2,7,1],"12a"],
                [8, [2,4,3],"12b"],
                [8, [1,4,5],"12c"],
                # 13
                [24, [6,8,11],"13a"],
                [24, [6,23,1],"13b"],
                [24, [8,12,5],"13c"],
                [24, [1,12,19],"13d"],
                # 14
                [10, [2,5,4],"14a"],
                [10, [1,5,6],"14b"],
                # 15
                [20, [1,10,17],"15a"],
                [20, [11,10,7],"15b"],
                [20, [8,10,3],"15c"],
                [20, [8,10,13],"15d"],
                # 16
                [30, [17, 10, 9],"16a"],
                [30, [6,7,23],"16b"],
                [30, [10,15,11],"16c"],
                [30, [6,15,19],"16d"],
                # 17
                [14, [9,7,1],"17a"],
                [14, [3,7,13],"17b"]];  

for i in xrange(len(table)):
        file = open('rank2/'+table[i][2]+'.ars', 'w')
        file.write('# Arithmetic root system\n')
        file.write('# Heckenberger, I.\n')
        file.write('# Classification of arithmetic root systems of rank 3, Table 1, p. 6\n')
        file.write('# math.QA/0509145\n')
        file.write('description=\"%s\"\n'%table[i][2])
        file.write('rank=2\n')
        file.write('# order of the primitive root z\n')
        file.write('order=%d\n'%table[i][0])
        file.write('# braid\n')
        file.write('# every element of this matrix q=(q_ij) is of the form z^(q_ij)\n')
        file.write('braid\n')
        file.write('%d,%d\n'%(table[i][1][0],table[i][1][2]))
        file.write('0,%d\n'%table[i][1][1])
        file.close


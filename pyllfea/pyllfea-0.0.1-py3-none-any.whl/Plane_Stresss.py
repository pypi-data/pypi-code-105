import numpy as np


class PlaneStress:

    def __init__(self, geo: dict, material: dict, boundery_condition: dict):
        self.geo = geo
        self.material = material
        self.boundery_condition = boundery_condition

    def get_A(self):
    ##这个函数的作用是获取所有单元的面积，然后把它们存储在一个dict中返回
        geo = self.geo
        dict_A = {}
        units_num = len(geo["units"])
        for i in range(1,units_num+1):
            unit_points=geo["units"][f"unit{i}"]
            A=(geo["points"][f"point{unit_points[0]}"][0]*(geo["points"][f"point{unit_points[1]}"][1]-geo["points"][f"point{unit_points[2]}"][1])+geo["points"][f"point{unit_points[1]}"][0]*(geo["points"][f"point{unit_points[2]}"][1]-geo["points"][f"point{unit_points[0]}"][1])+geo["points"][f"point{unit_points[2]}"][0]*(geo["points"][f"point{unit_points[0]}"][1]-geo["points"][f"point{unit_points[1]}"][1]))/2
            dict_A[f"unit{i}A"] = A

        return dict_A


    def get_B(self):
        geo=self.geo
        dict_B = {}
        for i in range(1,len(geo["units"])+1):
            points = geo["units"][f"unit{i}"]
            B_i = np.array([[geo["points"][f"point{points[1]}"][1]-geo["points"][f"point{points[2]}"][1],0],
                            [0,geo["points"][f"point{points[2]}"][0]-geo["points"][f"point{points[1]}"][0]],
                            [geo["points"][f"point{points[2]}"][0]-geo["points"][f"point{points[1]}"][0],geo["points"][f"point{points[1]}"][1]-geo["points"][f"point{points[2]}"][1]]])
            B_j = np.array([[geo["points"][f"point{points[2]}"][1]-geo["points"][f"point{points[0]}"][1],0],
                            [0,geo["points"][f"point{points[0]}"][0]-geo["points"][f"point{points[2]}"][0]],
                            [geo["points"][f"point{points[0]}"][0]-geo["points"][f"point{points[2]}"][0],geo["points"][f"point{points[2]}"][1]-geo["points"][f"point{points[0]}"][1]]])
            B_m = np.array([[geo["points"][f"point{points[0]}"][1]-geo["points"][f"point{points[1]}"][1],0],
                            [0,geo["points"][f"point{points[1]}"][0]-geo["points"][f"point{points[0]}"][0]],
                            [geo["points"][f"point{points[1]}"][0]-geo["points"][f"point{points[0]}"][0],geo["points"][f"point{points[0]}"][1]-geo["points"][f"point{points[1]}"][1]]])

            dict_B[f"unit{i}B"]=np.concatenate([B_i,B_j,B_m],axis=1)/(2*self.get_A()[f"unit{i}A"])
        
        return dict_B

    def get_D(self):
        Material=self.material
        E = Material["E"]
        v = Material["v"]
        D = np.array([[1, v, 0], [v, 1, 0], [0, 0, (1-v)/2]])*E/(1-v**2)
        return D

    def get_K(self,t:int):

        A=self.get_A()
        B=self.get_B()
        D=self.get_D()
        geo=self.geo
        dict_K = {}
        for i in range(1,len(A)+1):
            dict_K[f"unit{i}K"]=t*A[f"unit{i}A"]*np.mat(B[f"unit{i}B"]).T*np.mat(D)*np.mat(B[f"unit{i}B"])

        K=np.zeros((2*len(geo["points"]),2*len(geo["points"]))) 


        for i in range(1,len(geo["units"])+1):
            a=geo["units"][f"unit{i}"]
            point_set = [[a[0],a[0]],[a[0],a[1]],[a[0],a[2]],[a[1],a[0]],[a[1],a[1]],[a[1],a[2]],[a[2],a[0]],[a[2],a[1]],[a[2],a[2]]]
            for j in range(9):
                    K[2*(point_set[j][0]-1)][2*(point_set[j][1]-1)]+=dict_K[f"unit{i}K"][2*(j//3),2*(j%3)]
                    K[2*(point_set[j][0]-1)][2*(point_set[j][1]-1)+1]+=dict_K[f"unit{i}K"][2*(j//3),2*(j%3)+1]
                    K[2*(point_set[j][0]-1)+1][2*(point_set[j][1]-1)]+=dict_K[f"unit{i}K"][2*(j//3)+1,2*(j%3)]
                    K[2*(point_set[j][0]-1)+1][2*(point_set[j][1]-1)+1]+=dict_K[f"unit{i}K"][2*(j//3)+1,2*(j%3)+1]

        return  K

    def read_boundery_condition(self, axis: str):
        boundery_condition = self.boundery_condition
        if axis == "fboundery":
            f_list = []

            for i in range(1, len(boundery_condition["f_boundery"])//2+1):
                if isinstance(boundery_condition["f_boundery"][f"f{i}x"], (int, float)) or boundery_condition["f_boundery"][f"f{i}x"] == None:
                    f_list.append(boundery_condition["f_boundery"][f"f{i}x"])
                else:
                    print("你的输入有误!"+"力边界条件应该是一个数字或者None")
                if isinstance(boundery_condition["f_boundery"][f"f{i}y"], (int, float)) or boundery_condition["f_boundery"][f"f{i}y"] == None:
                    f_list.append(boundery_condition["f_boundery"][f"f{i}y"])
                else:
                    print("你的输入有误!"+"力边界条件应该是一个数字或者None")

            return f_list
        elif axis == "dboundery":
            d_list = []

            for i in range(1, len(boundery_condition["d_boundery"])//2+1):
                if isinstance(boundery_condition["d_boundery"][f"d{i}x"], (int, float)) or boundery_condition["d_boundery"][f"d{i}x"] == None:
                    d_list.append(boundery_condition["d_boundery"][f"d{i}x"])
                else:
                    print("你的输入有误!"+"位移边界条件应该是一个数字或者None")
                if isinstance(boundery_condition["d_boundery"][f"d{i}y"], (int, float)) or boundery_condition["d_boundery"][f"d{i}y"] == None:
                    d_list.append(boundery_condition["d_boundery"][f"d{i}y"])
                else:
                    print("你的输入有误!"+"位移边界条件应该是一个数字或者None")

            return d_list
        else:
            print("输入边界条件错误")

    def solve(self):
        
        k_mat = self.get_K(1)
        boundery_condition = self.boundery_condition
        f_list = self.read_boundery_condition("fboundery")
        d_list = self.read_boundery_condition("dboundery")
        new_d_list = d_list.copy()
        new_f_list = f_list.copy()
        new_k_mat = k_mat.copy()
        k = 0
        for i in range(len(d_list)):
            if d_list[i] == 0:
                new_k_mat = np.delete(new_k_mat, k, 0)
                new_k_mat = np.delete(new_k_mat, k, 1)
                del new_f_list[k]
                del new_d_list[k]
            else:
                k = k+1
        # new_k_mat_I是调整后的刚度矩阵的逆矩阵
        new_k_mat_I = np.linalg.inv(new_k_mat)
        for i in range(len(new_d_list)):
            new_d_list[i] = 0
            for j in range(len(new_d_list)):
                new_d_list[i] = new_k_mat_I[i][j]*new_f_list[j]+new_d_list[i]

        for i in range(len(d_list)):
            if d_list[i] == None:
                d_list[i] = new_d_list.pop(0)

        for i in range(len(f_list)):
            if f_list[i] == None:
                f_list[i] = 0
                for j in range(len(f_list)):
                    f_list[i] = f_list[i]+k_mat[i][j]*d_list[j]

        new_boundery_conditon = {}
        for i in range(len(f_list)//2):
            new_boundery_conditon[f"f{i+1}x"] = f_list[2*i]
            new_boundery_conditon[f"f{i+1}y"] = f_list[2*i+1]
            new_boundery_conditon[f"d{i+1}x"] = d_list[2*i]
            new_boundery_conditon[f"d{i+1}y"] = d_list[2*i+1]

        return new_boundery_conditon

此程序通过读取一个格式类似于ExampleOPLSAtomTypes.txt（力场原子类型识别规则）的文件，
生成一个格式类似于ExampleOPLSDescription.txt（力场参数描述）文件
所需要的力场信息在文件oplsaa.lt中
主程序入口main.cpp,
通过以下的几个变量：
    string PATH = "../";
    string OPLSAA_LT = PATH+"oplsaa.lt";
    string atomic_weights_file = PATH+"../../Data/atomicweights.csv";
    string atom_type_recognition_file = PATH+"AtomTypes_Input.txt";
    string output_file_name = PATH+"FFDescription_Output.txt";
    string functional_file = PATH+"functional.txt";
来控制输入和输出